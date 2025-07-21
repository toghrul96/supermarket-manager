import csv 
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import uuid
from decimal import Decimal


class SalesData():
    """
    Manage sales records stored in a CSV file.

    Provides functionality to record transactions, search sales data,
    and generate various sales reports.
    """
    
    def __init__(self, filename):
        """
        Initialize the SalesData manager with the CSV file.

        Args:
            filename (str): Path to the CSV file used for storing sales records.
        """
        self.filename = filename
        # Define the order and names of CSV columns for sales data
        self.fieldnames = ["Username", "SKU", "Barcode", "Order ID", 
                           "Item Name", "Quantity", "Unit Price", "Discount", "Net Price", 
                           "Line Total", "Sale Date"]
        
        # Ensure the folder exists before file creation
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        # Initialize data file with headers if missing
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def record_sales(self, checkout_list):
        """
        Save all items from the checkout list as a new sales transaction.

        Args:
            checkout_list (list of dict): List of items sold, each containing sale details.
        """
        # Generate a unique ID to link all items in this transaction
        order_id = self.generate_uuid_order_id()

        # Read existing sales data to keep transaction history intact
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            existing_rows = list(reader)

        # Build new rows for the current transaction with timestamp
        new_rows = []
        for item in checkout_list:
            new_rows.append({
                "Username": item["Username"], 
                "SKU": item["SKU"],
                "Barcode": item["Barcode"],
                "Order ID": order_id,
                "Item Name": item["Item Name"],
                "Quantity": item["Quantity"],
                "Unit Price": item['Unit Price'],
                "Discount": item['Discount'],
                "Net Price": item['Net Price'],
                "Line Total": item['Line Total'],
                "Sale Date": datetime.today().strftime("%d/%m/%Y %H:%M")
            })
        
        # Write header + new row + old rows (new transactions added to top of file)
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)       # New transactions first
            writer.writerows(existing_rows)  # Then existing transactions

    def generate_uuid_order_id(self):
        """Create unique transaction ID with prefix."""
        return "ORD-" + str(uuid.uuid4())[:8].upper()
    
    def search(self, keyword):
        """
        Search the sales data for items where any of the first six fields
        start with the given keyword (case-insensitive).

        The fields searched include: Username, SKU, Barcode, Order ID, and Item Name.

        Args:
            keyword (str): The search keyword to match against field prefixes.

        Returns:
            list: List of matching rows.
        """
        # Convert input to lowercase for consistent comparison
        keyword = keyword.lower()
        matched_items = []

        with open(self.filename, "r", newline="") as file:
            reader = csv.reader(file)
            # Read all rows, skipping the header
            items = list(reader)[1:]

            # Search through the first 5 fields of each row for prefix matches
            for row in items:
                if any(row[i].lower().startswith(keyword) for i in range(0, 5)):
                    matched_items.append(row)

        return matched_items

    def sort_by_date_interval(self, from_date, to_date):
        """
        Retrieve sales records that fall within a specified date range.

        Args:
            from_date (date): The starting date of the interval (inclusive).
            to_date (date): The ending date of the interval (inclusive).

        Returns:
            list: A list of sales records (as dictionaries) that match the date range.
        """
        matching_rows = []

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Extract and parse only the date part from the "Sale Date" field
                sale_date_str = row.get("Sale Date").split(" ")[0]  #type: ignore
                sale_date = datetime.strptime(sale_date_str, "%d/%m/%Y").date()

                # Include the row if the sale date is within the given range
                if from_date <= sale_date <= to_date:
                    matching_rows.append(row)

        return matching_rows

    def get_sales_summary_data(self, filter_date): 
        """
        Generate daily sales summary metrics from recorded transactions.

        Args:
        filter_date (str): The starting point for filtering sales records.

        Returns:
        list of lists: Each inner list contains summary data for a specific date:
        [Date, Total Orders, Total Quantity, Gross Sales, Discounts, Net Sales, Average Order Value]
        """
        summary_data = []
        # Keep track of unique order IDs per date to count total orders
        unique_orders = {} 

        # Get the earliest date to include in the summary based on selected filter
        start_date = self.get_data_range(filter_date)

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for sale_record in reader:
                # Extract and convert the sale date from the record
                sale_date = sale_record["Sale Date"].split(" ")[0]
                sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

                # Include only records on or after the selected start date
                if sale_date_obj >= start_date:
                    sale_record_exists = False
                    record_index = None
                    order_id = sale_record.get("Order ID")
                    
                    # Compute values for the sale
                    line_total = Decimal(sale_record.get("Line Total").strip("$").replace(",", "")) # type:ignore
                    quantity = Decimal(sale_record.get("Quantity")) # type:ignore
                    gross_sale = Decimal(sale_record.get("Unit Price").strip("$").replace(",", "")) * quantity # type:ignore
                    discount_amount = gross_sale - line_total
                    net_sale = line_total

                    # Register order ID under the corresponding date if not already tracked
                    if sale_date not in unique_orders:
                        unique_orders[sale_date] = [order_id]
                    elif order_id not in unique_orders[sale_date]:
                        unique_orders[sale_date].append(order_id)

                     # Calculate order metrics for the day
                    total_orders = len(unique_orders[sale_date])
                    avg_order_value = (net_sale / Decimal(total_orders))

                    # Check if this date already has an entry in summary_data
                    for index, row in enumerate(summary_data):
                        if row[0] == sale_date:
                            sale_record_exists = True
                            record_index = index
                            break
    
                     # Add new entry for the date or update the existing one
                    if not sale_record_exists:
                        summary_data.append([
                            sale_date, total_orders, quantity, gross_sale, 
                            discount_amount, net_sale, avg_order_value
                        ])                
                    else:
                        if record_index is not None:
                            # Update the existing summary by aggregating values
                            summary_data[record_index][1] = total_orders
                            summary_data[record_index][2] += quantity
                            summary_data[record_index][3] += gross_sale
                            summary_data[record_index][4] += discount_amount
                            summary_data[record_index][5] += net_sale
                            summary_data[record_index][6] = (
                                summary_data[record_index][5] / Decimal(summary_data[record_index][1])
                                ).quantize(Decimal("0.01"))
                            
        # Round final values for each row
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
            filter_date (str): The date from which to start including sales data.

        Returns:
            list of lists: Each inner list contains product data:
            [Item Name, SKU, Barcode, Quantity Sold, Total Revenue]
        """
        top_products_data = []
        # Determine the start date for filtering sales records
        start_date = self.get_data_range(filter_date)

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for sale_record in reader:
                # Extract and convert the sale date from the record
                sale_date = sale_record["Sale Date"].split(" ")[0]
                sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

                # Only process sales on or after the start date
                if sale_date_obj >= start_date:
                    sale_record_exists = False
                    record_index = None
                    barcode = sale_record["Barcode"]
                    sku = sale_record["SKU"]

                    # Check if product already has an entry in the summary list
                    for index, row in enumerate(top_products_data):
                        if row[1] == sku and row[2] == barcode:
                            sale_record_exists = True
                            record_index = index
                            break

                    # Extract sales metrics for the current sale record
                    item_name = sale_record["Item Name"]
                    quantity_sold = int(sale_record["Quantity"])
                    sale_revenue = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))

                    # Add a new product record or update the existing one
                    if not sale_record_exists:
                        top_products_data.append([
                            item_name, sku, barcode, quantity_sold, sale_revenue
                        ])
                    else:
                        if record_index is not None:
                            # Add quantities and revenues to existing product record
                            top_products_data[record_index][3] += quantity_sold
                            top_products_data[record_index][4] += sale_revenue

        # Sort products by total revenue in descending order
        top_products_data.sort(key=lambda row: row[4], reverse=True)

        return top_products_data
    
    def get_top_employees_data(self, filter_date):
        """
        Generate a performance report for employees sorted by total revenue.

        Args:
            filter_date (str): The date from which sales data is included.

        Returns:
            list of lists: Each inner list contains employee data:
            [Username, Transactions, Items Sold, Total Revenue]
        """
        top_employees_data = []
        # Store unique order IDs per employee to count transactions
        unique_orders = {}

        # Get the earliest date to include for filtering
        start_date = self.get_data_range(filter_date)

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for sale_record in reader:
                # Extract and convert the sale date from the record
                sale_date = sale_record["Sale Date"].split(" ")[0]
                sale_date_obj = datetime.strptime(sale_date, "%d/%m/%Y").date()

                # Process records only on or after the start date
                if sale_date_obj >= start_date:
                    sale_record_exists = False
                    record_index = None
                    order_id = sale_record.get("Order ID")
                    username = sale_record["Username"]
                    items_sold = int(sale_record["Quantity"])
                    sale_revenue = Decimal(sale_record["Line Total"].strip("$").replace(",", ""))

                    # Track unique orders to avoid counting duplicates per employee
                    if username not in unique_orders:
                        unique_orders[username] = [order_id]
                    elif order_id not in unique_orders[username]:
                        unique_orders[username].append(order_id)

                    transactions = len(unique_orders[username])

                    # Check if the employee already has an entry in the summary
                    for index, row in enumerate(top_employees_data):
                        if row[0] == username:
                            sale_record_exists = True
                            record_index = index
                            break

                    # Add a new employee record or update the existing one
                    if not sale_record_exists:
                        top_employees_data.append([
                            username, transactions, items_sold, sale_revenue
                        ])
                    else:
                        if record_index is not None:
                            # Update totals for the employee
                            top_employees_data[record_index][1] = transactions
                            top_employees_data[record_index][2] += items_sold
                            top_employees_data[record_index][3] += sale_revenue

        # Sort employees by revenue, highest first
        top_employees_data.sort(key=lambda row: row[3], reverse=True)

        return top_employees_data
    
    def get_data_range(self, filter_date):
        """
        Return the start date for filtering data based on the selected reporting period.

        Args:
            filter_date (str): The reporting period, e.g., "Daily", "Weekly", "Monthly", "Yearly", or "All Time".

        Returns:
            date: The earliest date to include in reports based on the filter.
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
        elif filter_date == "All Time":
            return date.min
        # Default to all data if filter is unrecognized
        else:
            return date.min



            








