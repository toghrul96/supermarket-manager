import os
import threading
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import uuid
from decimal import Decimal
from supabase import create_client
from dotenv import load_dotenv


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
        load_dotenv()
        self._url = os.getenv("SUPABASE_URL")
        self._key = os.getenv("SUPABASE_KEY")
        if not self._url or not self._key:
            raise ValueError("Missing Supabase credentials in .env file")

        self._access_token  = access_token
        self._refresh_token = refresh_token

        # Thread-local client — same pattern as InventoryData.
        # record_sales and all fetch methods run in worker threads;
        # sharing one httpx HTTP/2 client across threads corrupts the pool.
        self._local = threading.local()

    # ── thread-local client ───────────────────────────────────────────────────

    @property
    def supabase(self):
        """Return a thread-local Supabase client, creating one if needed."""
        if not hasattr(self._local, 'client'):
            client = create_client(self._url, self._key)
            if self._access_token and self._refresh_token:
                try:
                    client.auth.set_session(self._access_token, self._refresh_token)
                except Exception:
                    # set_session timed out — fall back to directly setting the
                    # Bearer token so RLS-protected queries still work.
                    client.postgrest.auth(self._access_token)
            self._local.client = client
        return self._local.client

    # ── internal helpers ──────────────────────────────────────────────────────

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

        if from_date is not None:
            query = query.gte("sale_date", from_date.isoformat())
        if to_date is not None:
            # lt the day *after* to_date so the full day is included
            query = query.lt("sale_date", (to_date + timedelta(days=1)).isoformat())

        response = query.execute()
        rows = response.data or []

        result = []
        for row in rows:
            product   = row.get("product")   or {}
            user_info = row.get("user_info") or {}

            # Convert integer cents → formatted dollar string
            def cents_to_str(cents):
                if cents is None:
                    return "$0.00"
                return f"${Decimal(cents) / 100:,.2f}"

            # Convert ISO timestamptz → dd/mm/yyyy HH:MM
            raw_date = row.get("sale_date") or ""
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                formatted_date = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                formatted_date = ""

            # Barcode is stored as integer in DB — convert to string for display
            barcode = product.get("barcode")
            barcode_str = str(barcode) if barcode is not None else ""

            result.append({
                "Username":   user_info.get("username", ""),
                "SKU":        product.get("sku", ""),
                "Barcode":    barcode_str,
                "Order ID":   row.get("order_id", ""),
                "Item Name":  product.get("item_name", ""),
                "Quantity":   str(row.get("quantity") or 0),
                "Unit Price": cents_to_str(row.get("unit_price")),
                "Discount":   f"{row.get('discount') or 0}%",
                "Net Price":  cents_to_str(row.get("net_price")),
                "Line Total": cents_to_str(row.get("line_total")),
                "Sale Date":  formatted_date,
            })

        return result

    # ── public API ────────────────────────────────────────────────────────────

    def record_sales(self, checkout_list, user_uuid):
        """
        Insert all items from the checkout list as a new sales transaction.

        Prices are stored as integer cents (e.g. $9.99 → 999).
        product_id is resolved by looking up each item's barcode in the product table.

        Args:
            checkout_list (list of dict): Items sold; each dict contains sale details.
            user_uuid (str):              UUID of the logged-in user (stored as user_id).
        """
        order_id = self.generate_uuid_order_id()

        # Barcodes in checkout_list are strings; the product table stores them
        # as integers. Convert before querying so the IN filter matches correctly.
        barcodes_int = list({int(item["Barcode"]) for item in checkout_list})
        prod_response = (
            self.supabase.table("product")
            .select("id, barcode")
            .in_("barcode", barcodes_int)
            .execute()
        )
        # Key by string barcode so lookup matches checkout_list["Barcode"]
        barcode_to_product_id = {
            str(row["barcode"]): row["id"]
            for row in (prod_response.data or [])
        }

        def dollar_str_to_cents(value):
            """Strip formatting and convert a dollar string to integer cents."""
            return int(Decimal(value.strip("$").replace(",", "")) * 100)

        now_iso = datetime.now().isoformat()

        rows = []
        for item in checkout_list:
            discount_str = item.get("Discount", "0%").replace("%", "").strip()
            try:
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
        keyword = keyword.lower()
        all_dicts = self._fetch_sales_as_dicts()

        field_order = [
            "Username", "SKU", "Barcode", "Order ID", "Item Name",
            "Quantity", "Unit Price", "Discount", "Net Price", "Line Total", "Sale Date",
        ]
        display_rows = [[row[f] for f in field_order] for row in all_dicts]

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
        start_date   = self.get_data_range(filter_date)
        sale_records = self._fetch_sales_as_dicts(from_date=start_date)
        summary_data = []
        unique_orders = {}

        for sale_record in sale_records:
            # Skip rows with no sale date — guards against NULL sale_date
            # values that may exist from older records in the DB.
            if not sale_record["Sale Date"]:
                continue

            sale_date     = sale_record["Sale Date"].split(" ")[0]
            sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

            if sale_date_obj >= start_date:
                sale_record_exists = False
                record_index       = None
                order_id           = sale_record.get("Order ID")

                line_total      = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))
                quantity        = Decimal(sale_record["Quantity"])
                gross_sale      = Decimal(sale_record["Unit Price"].strip("$").replace(",", "")) * quantity
                discount_amount = gross_sale - line_total
                net_sale        = line_total

                if sale_date not in unique_orders:
                    unique_orders[sale_date] = [order_id]
                elif order_id not in unique_orders[sale_date]:
                    unique_orders[sale_date].append(order_id)

                total_orders    = len(unique_orders[sale_date])
                avg_order_value = net_sale / Decimal(total_orders)

                for index, row in enumerate(summary_data):
                    if row[0] == sale_date:
                        sale_record_exists = True
                        record_index = index
                        break

                if not sale_record_exists:
                    summary_data.append([
                        sale_date, total_orders, quantity, gross_sale,
                        discount_amount, net_sale, avg_order_value,
                    ])
                elif record_index is not None:
                    summary_data[record_index][1] = total_orders
                    summary_data[record_index][2] += quantity
                    summary_data[record_index][3] += gross_sale
                    summary_data[record_index][4] += discount_amount
                    summary_data[record_index][5] += net_sale
                    summary_data[record_index][6] = (
                        summary_data[record_index][5] / Decimal(summary_data[record_index][1])
                    ).quantize(Decimal("0.01"))

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

                for index, row in enumerate(top_products_data):
                    if row[1] == sku and row[2] == barcode:
                        sale_record_exists = True
                        record_index = index
                        break

                item_name     = sale_record["Item Name"]
                quantity_sold = int(sale_record["Quantity"])
                sale_revenue  = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))

                if not sale_record_exists:
                    top_products_data.append([
                        item_name, sku, barcode, quantity_sold, sale_revenue,
                    ])
                elif record_index is not None:
                    top_products_data[record_index][3] += quantity_sold
                    top_products_data[record_index][4] += sale_revenue

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

                if username not in unique_orders:
                    unique_orders[username] = [order_id]
                elif order_id not in unique_orders[username]:
                    unique_orders[username].append(order_id)

                transactions = len(unique_orders[username])

                for index, row in enumerate(top_employees_data):
                    if row[0] == username:
                        sale_record_exists = True
                        record_index = index
                        break

                if not sale_record_exists:
                    top_employees_data.append([
                        username, transactions, items_sold, sale_revenue,
                    ])
                elif record_index is not None:
                    top_employees_data[record_index][1] = transactions
                    top_employees_data[record_index][2] += items_sold
                    top_employees_data[record_index][3] += sale_revenue

        top_employees_data.sort(key=lambda row: row[3], reverse=True)
        return top_employees_data

    # ── return processing ─────────────────────────────────────────────────────

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
        rows = response.data or []

        if not rows:
            raise ValueError(f"No order found with ID '{order_id}'.")

        result = []
        for row in rows:
            product = row.get("product") or {}

            unit_price_cents  = row.get("unit_price")  or 0
            net_price_cents   = row.get("net_price")   or 0
            line_total_cents  = row.get("line_total")  or 0
            qty               = row.get("quantity")    or 0

            raw_date = row.get("sale_date") or ""
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                sale_date = dt.date()
            except Exception:
                sale_date = None

            result.append({
                "id":               row.get("id"),
                "order_id":         row.get("order_id", ""),
                "item_name":        product.get("item_name", ""),
                "sku":              product.get("sku", ""),
                "barcode":          str(product.get("barcode", "")),
                "quantity":         qty,
                "unit_price_cents": unit_price_cents,
                "unit_price_str":   f"${Decimal(unit_price_cents) / 100:,.2f}",
                "discount":         row.get("discount") or 0,
                "net_price_cents":  net_price_cents,
                "net_price_str":    f"${Decimal(net_price_cents) / 100:,.2f}",
                "line_total_cents": line_total_cents,
                "line_total_str":   f"${Decimal(line_total_cents) / 100:,.2f}",
                "product_id":       row.get("product_id"),
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
        now_iso = datetime.now().isoformat()
        returned_rows = []

        for item in return_items:
            return_qty   = item["return_qty"]
            original_qty = item["original_qty"]
            row_id       = item["id"]

            if return_qty <= 0:
                continue

            # ── update or delete the original sales row ──────────────────────
            if return_qty >= original_qty:
                self.supabase.table("sales").delete().eq("id", row_id).execute()
            else:
                new_qty        = original_qty - return_qty
                new_line_total = item["net_price_cents"] * new_qty
                self.supabase.table("sales").update({
                    "quantity":   new_qty,
                    "line_total": new_line_total,
                }).eq("id", row_id).execute()

            # ── build the returned_items row ─────────────────────────────────
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

        def cents_to_str(cents):
            if cents is None:
                return "$0.00"
            return f"${Decimal(cents) / 100:,.2f}"

        result = []
        for row in rows:
            product   = row.get("product")   or {}
            user_info = row.get("user_info") or {}

            raw_date = row.get("sale_date") or ""
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                formatted_date = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                formatted_date = ""

            barcode = product.get("barcode")
            display_row = [
                user_info.get("username", ""),
                product.get("sku", ""),
                str(barcode) if barcode is not None else "",
                row.get("order_id", ""),
                product.get("item_name", ""),
                str(row.get("quantity") or 0),
                cents_to_str(row.get("unit_price")),
                f"{row.get('discount') or 0}%",
                cents_to_str(row.get("net_price")),
                cents_to_str(row.get("line_total")),
                formatted_date,
            ]

            if keyword:
                kw = keyword.lower()
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
            return date.min