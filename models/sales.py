import os
import threading
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import uuid
from decimal import Decimal
from supabase import create_client
from dotenv import load_dotenv



import sys as _sys
import os as _os

def _load_env():
    """Load .env from the correct path whether running as script or frozen exe."""
    from dotenv import load_dotenv
    if getattr(_sys, 'frozen', False):
        base_path = _sys._MEIPASS  # type: ignore
    else:
        base_path = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    load_dotenv(_os.path.join(base_path, '.env'))

class SalesData:
    """
    Manage sales records stored in Supabase.

    Provides functionality to record transactions, search sales data,
    and generate various sales reports.
    """

    def __init__(self, access_token, refresh_token):
        """
        Initialize the SalesData manager with a Supabase session.

        Args:
            access_token (str): Supabase access token from the logged-in session.
            refresh_token (str): Supabase refresh token from the logged-in session.
        """
        # Load environment variables from the .env file
        _load_env()
        # Read Supabase connection credentials from the environment
        self._url = os.getenv("SUPABASE_URL")
        self._key = os.getenv("SUPABASE_KEY")
        # Fail fast if either credential is missing before any DB call is attempted
        if not self._url or not self._key:
            raise ValueError("Missing Supabase credentials in .env file")

        # Store tokens so each thread can authenticate its own Supabase session
        self._access_token  = access_token
        self._refresh_token = refresh_token

        # Thread-local client — same pattern as InventoryData.
        # record_sales and all fetch methods run in worker threads;
        # sharing one httpx HTTP/2 client across threads corrupts the pool.
        self._local = threading.local()

    # -- thread-local client ---------------------------------------------------

    @property
    def supabase(self):
        """Return a thread-local Supabase client, creating one if needed."""
        # Only create a new client if this thread doesn't already have one
        if not hasattr(self._local, 'client'):
            # Instantiate a fresh Supabase client bound to this thread
            client = create_client(self._url, self._key) #type: ignore
            if self._access_token and self._refresh_token:
                try:
                    # Attach the stored session so RLS policies apply correctly
                    client.auth.set_session(self._access_token, self._refresh_token)
                except Exception:
                    # set_session timed out — fall back to directly setting the
                    # Bearer token so RLS-protected queries still work.
                    client.postgrest.auth(self._access_token)
            self._local.client = client
        return self._local.client

    # -- internal helpers ------------------------------------------------------

    def _fetch_sales_as_dicts(self, from_date=None, to_date=None):
        """
        Fetch sales rows from Supabase with product/user joins.

        Returns rows as dicts with display-ready field names:
        Username, SKU, Barcode, Order ID, Item Name, Quantity,
        Unit Price, Discount, Net Price, Line Total, Sale Date.

        Prices are stored as integer cents in the DB and converted to
        formatted dollar strings here (e.g. 999 → "$9.99") so all
        aggregation logic can work with consistent string values.

        Args:
            from_date (date, optional): Include only records on or after this date.
            to_date   (date, optional): Include only records on or before this date (inclusive).

        Returns:
            list of dict: Sales rows newest first.
        """
        query = (
            self.supabase.table("sales")
            .select(
                "order_id, quantity, unit_price, discount, "
                "net_price, line_total, sale_date, "
                "product:product_id(item_name, sku, barcode), "
                "user_info:user_id(username)"
            )
            .order("sale_date", desc=True)
        )

        # Narrow the query to only records on or after from_date
        if from_date is not None:
            query = query.gte("sale_date", from_date.isoformat())
        if to_date is not None:
            # lt the day *after* to_date so the full day is included
            query = query.lt("sale_date", (to_date + timedelta(days=1)).isoformat())

        # Execute the built query and unpack the result
        response = query.execute()
        rows = response.data or []

        # Collect formatted dicts for each sales row
        result = []
        # Flatten joined product/user data and format each field for display
        for row in rows:
            product   = row.get("product")   or {} #type: ignore
            user_info = row.get("user_info") or {} #type: ignore

            # Convert integer cents → formatted dollar string
            def cents_to_str(cents):
                if cents is None:
                    return "$0.00"
                return f"${Decimal(cents) / 100:,.2f}"

            # Convert ISO timestamptz → dd/mm/yyyy HH:MM
            raw_date = row.get("sale_date") or "" #type: ignore
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00")) #type: ignore
                formatted_date = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                formatted_date = ""

            # Barcode is stored as integer in DB — convert to string for display
            barcode = product.get("barcode") #type: ignore
            barcode_str = str(barcode) if barcode is not None else ""

            result.append({
                "Username":   user_info.get("username", ""), #type: ignore
                "SKU":        product.get("sku", ""), #type: ignore
                "Barcode":    barcode_str,
                "Order ID":   row.get("order_id", ""), #type: ignore
                "Item Name":  product.get("item_name", ""), #type: ignore
                "Quantity":   str(row.get("quantity") or 0), #type: ignore
                "Unit Price": cents_to_str(row.get("unit_price")), #type: ignore
                "Discount":   f"{row.get('discount') or 0}%", #type: ignore
                "Net Price":  cents_to_str(row.get("net_price")), #type: ignore
                "Line Total": cents_to_str(row.get("line_total")), #type: ignore
                "Sale Date":  formatted_date,
            })

        return result

    # -- public API ------------------------------------------------------------

    def record_sales(self, checkout_list, user_uuid):
        """
        Insert all items from the checkout list as a new sales transaction.

        Prices are stored as integer cents (e.g. $9.99 → 999).
        product_id is resolved by looking up each item's barcode in the product table.

        Args:
            checkout_list (list of dict): Items sold; each dict contains sale details.
            user_uuid (str):              UUID of the logged-in user (stored as user_id).
        """
        # All items in this checkout share the same generated order ID
        order_id = self.generate_uuid_order_id()

        # Barcodes in checkout_list are strings; the product table stores them
        # as integers. Convert before querying so the IN filter matches correctly.
        # De-duplicate barcodes and cast to int to match the DB column type
        barcodes_int = list({int(item["Barcode"]) for item in checkout_list})
        # Fetch product IDs for all barcodes in a single query instead of one-by-one
        prod_response = (
            self.supabase.table("product")
            .select("id, barcode")
            .in_("barcode", barcodes_int)
            .execute()
        )
        # Key by string barcode so lookup matches checkout_list["Barcode"]
        barcode_to_product_id = {
            str(row["barcode"]): row["id"] #type: ignore
            for row in (prod_response.data or [])
        }

        def dollar_str_to_cents(value):
            """Strip formatting and convert a dollar string to integer cents."""
            return int(Decimal(value.strip("$").replace(",", "")) * 100)

        # Capture the timestamp once so all rows in this order share the same sale time
        now_iso = datetime.now().isoformat()

        # Build the list of rows to batch-insert into the sales table
        rows = []
        # Convert each checkout item into a DB-ready dict
        for item in checkout_list:
            discount_str = item.get("Discount", "0%").replace("%", "").strip()
            try:
                # Guard against non-numeric discount strings
                discount_int = int(discount_str)
            except (ValueError, TypeError):
                discount_int = 0

            rows.append({
                "order_id":   order_id,
                "quantity":   int(item["Quantity"]),
                "unit_price": dollar_str_to_cents(item["Unit Price"]),
                "discount":   discount_int,
                "net_price":  dollar_str_to_cents(item["Net Price"]),
                "line_total": dollar_str_to_cents(item["Line Total"]),
                "product_id": barcode_to_product_id.get(item["Barcode"]),
                "user_id":    user_uuid,
                "sale_date":  now_iso,          # was missing — caused NULL Sale Date
            })

        # Persist all sale rows in a single batch insert
        self.supabase.table("sales").insert(rows).execute()

    def generate_uuid_order_id(self):
        """Create unique transaction ID with prefix."""
        return "ORD-" + str(uuid.uuid4())[:8].upper()

    def search(self, keyword):
        """
        Search sales data for rows where any of the first five fields
        (Username, SKU, Barcode, Order ID, Item Name) start with the keyword.

        Args:
            keyword (str): Search keyword (case-insensitive prefix match).

        Returns:
            list of list: Matching rows as ordered lists for table display.
        """
        # Normalize to lowercase for case-insensitive prefix matching
        keyword = keyword.lower()
        # Fetch all sales records as display-ready dicts
        all_dicts = self._fetch_sales_as_dicts()

        # Define column order to match the UI table layout
        field_order = [
            "Username", "SKU", "Barcode", "Order ID", "Item Name",
            "Quantity", "Unit Price", "Discount", "Net Price", "Line Total", "Sale Date",
        ]
        # Convert each dict to an ordered list for the table widget
        display_rows = [[row[f] for f in field_order] for row in all_dicts]

        # Keep only rows where at least one of the first 5 fields starts with the keyword
        return [
            row for row in display_rows
            if any(row[i].lower().startswith(keyword) for i in range(5))
        ]

    def sort_by_date_interval(self, from_date, to_date):
        """
        Retrieve sales records that fall within a specified date range.

        Args:
            from_date (date): Starting date (inclusive).
            to_date   (date): Ending date (inclusive).

        Returns:
            list of dict: Matching sales records as display-ready dicts.
        """
        return self._fetch_sales_as_dicts(from_date=from_date, to_date=to_date)

    def get_sales_summary_data(self, filter_date):
        """
        Generate daily sales summary metrics from recorded transactions.

        Args:
            filter_date (str): Reporting period: "Daily", "Weekly", "Monthly",
                               "Yearly", or "All Time".

        Returns:
            list of lists: Each inner list:
            [Date, Total Orders, Total Quantity, Gross Sales,
             Discounts, Net Sales, Average Order Value]
        """
        # Resolve the filter string into an actual calendar start date
        start_date   = self.get_data_range(filter_date)
        # Fetch only the records that fall within the reporting period
        sale_records = self._fetch_sales_as_dicts(from_date=start_date)
        summary_data = []
        # Track distinct order IDs per day to count transactions without double-counting
        unique_orders = {}

        # Process each sale row to build or update the daily summary entry
        for sale_record in sale_records:
            # Skip rows with no sale date — guards against NULL sale_date
            # values that may exist from older records in the DB.
            if not sale_record["Sale Date"]:
                continue

            # Strip the time portion — the summary is grouped by date only
            sale_date     = sale_record["Sale Date"].split(" ")[0]
            sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

            if sale_date_obj >= start_date:
                sale_record_exists = False
                record_index       = None
                order_id           = sale_record.get("Order ID")

                # Parse formatted dollar strings back to Decimal for arithmetic
                line_total      = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))
                quantity        = Decimal(sale_record["Quantity"])
                gross_sale      = Decimal(sale_record["Unit Price"].strip("$").replace(",", "")) * quantity
                # Discount amount = what would have been paid without discount minus what was actually paid
                discount_amount = gross_sale - line_total
                net_sale        = line_total

                # Register this order ID under its date to avoid counting it twice
                if sale_date not in unique_orders:
                    unique_orders[sale_date] = [order_id]
                elif order_id not in unique_orders[sale_date]:
                    unique_orders[sale_date].append(order_id)

                # Count of unique orders processed on this date so far
                total_orders    = len(unique_orders[sale_date])
                # Rolling average — will be recalculated again after full aggregation
                avg_order_value = net_sale / Decimal(total_orders)

                # Check if a summary row already exists for this date
                for index, row in enumerate(summary_data):
                    if row[0] == sale_date:
                        sale_record_exists = True
                        record_index = index
                        break

                # First sale row for this date — create a new summary entry
                if not sale_record_exists:
                    summary_data.append([
                        sale_date, total_orders, quantity, gross_sale,
                        discount_amount, net_sale, avg_order_value,
                    ])
                # Date already exists — accumulate values into the existing row
                elif record_index is not None:
                    summary_data[record_index][1] = total_orders
                    summary_data[record_index][2] += quantity
                    summary_data[record_index][3] += gross_sale
                    summary_data[record_index][4] += discount_amount
                    summary_data[record_index][5] += net_sale
                    # Recalculate average using the updated net sales and order count
                    summary_data[record_index][6] = (
                        summary_data[record_index][5] / Decimal(summary_data[record_index][1])
                    ).quantize(Decimal("0.01"))

        # Round all Decimal fields to 2 decimal places before returning
        for row in summary_data:
            row[3] = row[3].quantize(Decimal("0.01"))  # Gross Sales
            row[4] = row[4].quantize(Decimal("0.01"))  # Discounts
            row[5] = row[5].quantize(Decimal("0.01"))  # Net Sales
            row[6] = row[6].quantize(Decimal("0.01"))  # Avg Order Value

        return summary_data

    def get_top_products_data(self, filter_date):
        """
        Generate a report of product performance sorted by total revenue.

        Args:
            filter_date (str): Reporting period.

        Returns:
            list of lists: Each inner list:
            [Item Name, SKU, Barcode, Quantity Sold, Total Revenue]
        """
        # Resolve the period to a start date and fetch matching records
        start_date        = self.get_data_range(filter_date)
        sale_records      = self._fetch_sales_as_dicts(from_date=start_date)
        top_products_data = []

        for sale_record in sale_records:
            if not sale_record["Sale Date"]:
                continue

            sale_date     = sale_record["Sale Date"].split(" ")[0]
            sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

            if sale_date_obj >= start_date:
                sale_record_exists = False
                record_index       = None
                barcode            = sale_record["Barcode"]
                sku                = sale_record["SKU"]

                # Look for an existing entry for this product matched by SKU and barcode
                for index, row in enumerate(top_products_data):
                    if row[1] == sku and row[2] == barcode:
                        sale_record_exists = True
                        record_index = index
                        break

                # Extract the fields needed for aggregation
                item_name     = sale_record["Item Name"]
                quantity_sold = int(sale_record["Quantity"])
                sale_revenue  = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))

                # New product — add a fresh entry to the list
                if not sale_record_exists:
                    top_products_data.append([
                        item_name, sku, barcode, quantity_sold, sale_revenue,
                    ])
                # Product already seen — accumulate quantity and revenue
                elif record_index is not None:
                    top_products_data[record_index][3] += quantity_sold
                    top_products_data[record_index][4] += sale_revenue

        # Rank products by total revenue, highest first
        top_products_data.sort(key=lambda row: row[4], reverse=True)
        return top_products_data

    def get_top_employees_data(self, filter_date):
        """
        Generate a performance report for employees sorted by total revenue.

        Args:
            filter_date (str): Reporting period.

        Returns:
            list of lists: Each inner list:
            [Username, Transactions, Items Sold, Total Revenue]
        """
        start_date         = self.get_data_range(filter_date)
        sale_records       = self._fetch_sales_as_dicts(from_date=start_date)
        top_employees_data = []
        # Track distinct order IDs per employee for accurate transaction counts
        unique_orders      = {}

        for sale_record in sale_records:
            if not sale_record["Sale Date"]:
                continue

            sale_date     = sale_record["Sale Date"].split(" ")[0]
            sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

            if sale_date_obj >= start_date:
                sale_record_exists = False
                record_index       = None
                order_id           = sale_record.get("Order ID")
                username           = sale_record["Username"]
                items_sold         = int(sale_record["Quantity"])
                sale_revenue       = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))

                # Register this order under the employee to avoid counting duplicates
                if username not in unique_orders:
                    unique_orders[username] = [order_id]
                elif order_id not in unique_orders[username]:
                    unique_orders[username].append(order_id)

                # Number of unique orders this employee has processed so far
                transactions = len(unique_orders[username])

                # Find the existing entry for this employee, if any
                for index, row in enumerate(top_employees_data):
                    if row[0] == username:
                        sale_record_exists = True
                        record_index = index
                        break

                # New employee — add a fresh entry to the list
                if not sale_record_exists:
                    top_employees_data.append([
                        username, transactions, items_sold, sale_revenue,
                    ])
                # Employee already seen — update transaction count and accumulate totals
                elif record_index is not None:
                    top_employees_data[record_index][1] = transactions
                    top_employees_data[record_index][2] += items_sold
                    top_employees_data[record_index][3] += sale_revenue

        # Rank employees by total revenue generated, highest first
        top_employees_data.sort(key=lambda row: row[3], reverse=True)
        return top_employees_data

    # -- return processing -----------------------------------------------------

    def get_order_items(self, order_id):
        """
        Fetch all sales rows for a given order_id with product joins.

        Args:
            order_id (str): The order ID to look up.

        Returns:
            list of dict: One dict per sales row, containing display strings
            and raw cents values needed by the return popup.

        Raises:
            ValueError: If the order does not exist.
        """
        response = (
            self.supabase.table("sales")
            .select(
                "id, order_id, quantity, unit_price, discount, "
                "net_price, line_total, sale_date, product_id, "
                "product:product_id(item_name, sku, barcode)"
            )
            .eq("order_id", order_id)
            .execute()
        )
        # Unpack the query result, defaulting to an empty list if nothing was found
        rows = response.data or []

        # Raise early if the order ID doesn't match any record in the DB
        if not rows:
            raise ValueError(f"No order found with ID '{order_id}'.")

        result = []
        for row in rows:
            product = row.get("product") or {} #type: ignore

            # Keep raw cents for arithmetic and formatted strings for display side-by-side
            unit_price_cents  = row.get("unit_price")  or 0 #type: ignore
            net_price_cents   = row.get("net_price")   or 0 #type: ignore
            line_total_cents  = row.get("line_total")  or 0 #type: ignore
            qty               = row.get("quantity")    or 0 #type: ignore

            raw_date = row.get("sale_date") or "" #type: ignore
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00")) #type: ignore
                sale_date = dt.date()
            except Exception:
                sale_date = None

            result.append({
                "id":               row.get("id"), #type: ignore
                "order_id":         row.get("order_id", ""), #type: ignore
                "item_name":        product.get("item_name", ""), #type: ignore
                "sku":              product.get("sku", ""), #type: ignore
                "barcode":          str(product.get("barcode", "")), #type: ignore
                "quantity":         qty,
                "unit_price_cents": unit_price_cents,
                "unit_price_str":   f"${Decimal(unit_price_cents) / 100:,.2f}", #type: ignore
                "discount":         row.get("discount") or 0, #type: ignore
                "net_price_cents":  net_price_cents,
                "net_price_str":    f"${Decimal(net_price_cents) / 100:,.2f}", #type: ignore
                "line_total_cents": line_total_cents,
                "line_total_str":   f"${Decimal(line_total_cents) / 100:,.2f}", #type: ignore
                "product_id":       row.get("product_id"), #type: ignore
                "sale_date":        sale_date,
            })

        return result

    def process_return(self, order_id, return_items, user_uuid):
        """
        Process a return transaction safely.

        For each item with return_qty > 0:
          - If return_qty == original_qty: DELETE the sales row.
          - If return_qty < original_qty: UPDATE the sales row
            (reduce quantity, recalculate line_total proportionally).
          - INSERT into returned_items (same schema as sales;
            sale_date stores the return timestamp).

        Inventory quantities are NOT restocked on return.

        Args:
            order_id (str): The order being returned.
            return_items (list of dict): Items to return. Each dict must contain:
                id, product_id, original_qty, return_qty,
                unit_price_cents, discount, net_price_cents.
            user_uuid (str): UUID of the staff member processing the return.
        """
        # Capture the return timestamp once so all returned rows share the same time
        now_iso = datetime.now().isoformat()
        # Collect rows to insert into returned_items after processing the originals
        returned_rows = []

        for item in return_items:
            return_qty   = item["return_qty"]
            original_qty = item["original_qty"]
            row_id       = item["id"]

            # Skip items the user chose not to return
            if return_qty <= 0:
                continue

            # -- update or delete the original sales row ----------------------
            # Full return — remove the original sales row entirely
            if return_qty >= original_qty:
                self.supabase.table("sales").delete().eq("id", row_id).execute()
            else:
                # Partial return — reduce quantity and recalculate line total proportionally
                new_qty        = original_qty - return_qty
                new_line_total = item["net_price_cents"] * new_qty
                self.supabase.table("sales").update({
                    "quantity":   new_qty,
                    "line_total": new_line_total,
                }).eq("id", row_id).execute()

            # -- build the returned_items row ---------------------------------
            returned_rows.append({
                "order_id":   order_id,
                "quantity":   return_qty,
                "unit_price": item["unit_price_cents"],
                "discount":   item["discount"],
                "net_price":  item["net_price_cents"],
                "line_total": item["net_price_cents"] * return_qty,
                "sale_date":  now_iso,          # sale_date = return timestamp
                "product_id": item["product_id"],
                "user_id":    user_uuid,
            })

        # Only insert if there is at least one item being returned
        if returned_rows:
            self.supabase.table("returned_items").insert(returned_rows).execute()

    def get_returned_items_display(self, keyword=None):
        """
        Fetch returned_items rows with product/user joins for the report tab.

        Args:
            keyword (str, optional): If provided, filter rows where any of the
                first five display fields starts with keyword (case-insensitive).

        Returns:
            list of list: Each inner list has 11 values matching the report columns:
            Processed By, SKU, Barcode, Order ID, Item Name, Quantity,
            Unit Price, Discount, Net Price, Line Total, Return Date.
        """
        response = (
            self.supabase.table("returned_items")
            .select(
                "order_id, quantity, unit_price, discount, "
                "net_price, line_total, sale_date, "
                "product:product_id(item_name, sku, barcode), "
                "user_info:user_id(username)"
            )
            .order("sale_date", desc=True)
            .execute()
        )
        rows = response.data or []

        # Local helper mirrors cents_to_str from _fetch_sales_as_dicts
        def cents_to_str(cents):
            if cents is None:
                return "$0.00"
            return f"${Decimal(cents) / 100:,.2f}"

        # Collect formatted display rows for the returns report table
        result = []
        # Flatten joined product/user fields and format each returned item for display
        for row in rows:
            product   = row.get("product")   or {} #type: ignore
            user_info = row.get("user_info") or {} #type: ignore

            raw_date = row.get("sale_date") or "" #type: ignore
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00")) #type: ignore
                formatted_date = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                formatted_date = ""

            # Build the 11-column display list in report-column order
            barcode = product.get("barcode") #type: ignore
            display_row = [
                user_info.get("username", ""), #type: ignore
                product.get("sku", ""), #type: ignore
                str(barcode) if barcode is not None else "",
                row.get("order_id", ""), #type: ignore
                product.get("item_name", ""), #type: ignore
                str(row.get("quantity") or 0), #type: ignore
                cents_to_str(row.get("unit_price")), #type: ignore
                f"{row.get('discount') or 0}%", #type: ignore
                cents_to_str(row.get("net_price")), #type: ignore
                cents_to_str(row.get("line_total")), #type: ignore
                formatted_date,
            ]

            # Apply the prefix-match filter only when a search keyword was provided
            if keyword:
                kw = keyword.lower()
                # Skip the row if none of the first 5 fields start with the keyword
                if not any(display_row[i].lower().startswith(kw) for i in range(5)):
                    continue

            result.append(display_row)

        return result

    def get_data_range(self, filter_date):
        """
        Return the start date for filtering data based on the selected reporting period.

        Args:
            filter_date (str): "Daily", "Weekly", "Monthly", "Yearly", or "All Time".

        Returns:
            date: Earliest date to include in reports.
        """
        # Anchor all relative date calculations to today's date
        today = date.today()

        if filter_date == "Daily":
            return today
        elif filter_date == "Weekly":
            return today - timedelta(days=7)
        elif filter_date == "Monthly":
            return today - relativedelta(months=1)
        elif filter_date == "Yearly":
            return today - relativedelta(years=1)
        else:  # "All Time" or unrecognized
            # date.min is the earliest possible date, effectively meaning no lower bound
            return date.min