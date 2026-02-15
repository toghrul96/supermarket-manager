import csv 
import os
import re
from datetime import datetime, date
from decimal import Decimal

class InventoryData():
    """
    Handles inventory management tasks including adding, updating, deleting, searching, 
    and reporting on inventory items stored in a CSV file.

    Responsibilities:
      Initializes inventory structure with predefined fields if file doesn't exist.
      Validates and records new stock entries.
      Updates existing items and applies discounts.
      Filters, searches, and counts items by various criteria.
      Reduces stock quantities during checkout and updates statuses based on stock level and expiry.
      Calculates total inventory value based on cost or selling price.
    """
    def __init__(self, filename):
        """
        Initialize the InventoryData instance.

        Args:
            filename (str): Path to the CSV file used for storing inventory records.
        """
        # Initialize inventory file and field structure
        self.filename = filename
        self.fieldnames = [
            "Category", "Item Name", "SKU", "Barcode", "Batch Number",
            "Quantity", "Minimum Stock", "Cost per Unit", "Price per Unit", 
            "Discount", "Net Price", "Received Date", "Expiry Date", "Status"
        ]

        # Ensure the folder exists before file creation
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        # Initialize data file with headers if missing
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def add_item(self, category, item_name, barcode, batch_number, 
             quantity, minimum_stock, cost_per_unit, price_per_unit, expiry_date):
        """
        Add a new inventory item with field validation and auto-generated SKU, status, and data fields.
        """
        
        # Clean and validate input values
        item_name = item_name.strip().title()
        InventoryValidator.validate_item_name(item_name)
        barcode = barcode.strip()
        InventoryValidator.validate_barcode(barcode)
        batch_number = batch_number.strip().upper()
        InventoryValidator.validate_batch_number(self.filename, barcode, batch_number)
        InventoryValidator.validate_numeric_fields(quantity, minimum_stock, cost_per_unit, price_per_unit)

        # Automatically generate derived fields
        sku = InventoryHelpers.generate_SKU(self.filename, category, item_name)
        status = InventoryHelpers.set_item_status(quantity, minimum_stock, expiry_date)
        received_date = date.today().strftime("%d/%m/%Y")  # Store current date as receiving date

        # Compute Net Price from price and discount
        discount = Decimal("0")  # Default discount 0%
        price = Decimal(price_per_unit)
        net_price = price * (Decimal("1") - discount / Decimal("100"))

        # Read current inventory to preserve existing records
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            existing_rows = list(reader)

        # Build the complete inventory entry
        new_row = {
            "Category": category,
            "Item Name": item_name,
            "SKU": sku,
            "Barcode": barcode,
            "Batch Number": batch_number,
            "Quantity": quantity,
            "Minimum Stock": minimum_stock,
            "Cost per Unit": f"${Decimal(cost_per_unit).quantize(Decimal('0.01')):,}",
            "Price per Unit": f"${Decimal(price_per_unit).quantize(Decimal('0.01')):,}",
            "Discount": f"{discount}%",  # Default discount for new items
            "Net Price": f"${net_price.quantize(Decimal('0.01')):,}",
            "Received Date": received_date,
            "Expiry Date": expiry_date.strftime("%d/%m/%Y"),
            "Status": status  # Stock status based on quantity and expiry
        }

        # Write updated inventory with new item at the top
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerow(new_row)       # Add new item first
            writer.writerows(existing_rows)  # Then append previous inventory

    def update_item(self, new_category, new_item_name, batch_number, new_quantity, new_minimum_stock,
                new_cost_per_unit, new_price_per_unit, new_expiry_date):
        """
        Update an existing inventory item identified by batch number, validating inputs and recalculating derived fields.
        """
        # Track whether the item was found and updated
        updated = False
        
        # Validate updated fields before applying changes
        InventoryValidator.validate_item_name(new_item_name)
        InventoryValidator.validate_numeric_fields(new_quantity, new_minimum_stock, 
                                                new_cost_per_unit, new_price_per_unit)
        
        # Generate updated SKU and status based on new data
        new_sku = InventoryHelpers.generate_SKU(self.filename, new_category, new_item_name)
        new_status = InventoryHelpers.set_item_status(new_quantity, new_minimum_stock, new_expiry_date)

        # Load current inventory to find and modify the matching item
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            items = list(reader)  # Load all items into memory for editing

            # Locate the item by batch number and update its fields
            for row in items:
                if row.get("Batch Number") == batch_number:
                    row["Category"] = new_category
                    row["Item Name"] = new_item_name.strip().title()
                    row["SKU"] = new_sku
                    row["Quantity"] = new_quantity
                    row["Minimum Stock"] = new_minimum_stock
                    row["Cost per Unit"] = f"${new_cost_per_unit:,}"
                    row["Price per Unit"] = f"${new_price_per_unit:,}"
                    row["Expiry Date"] = new_expiry_date.strftime("%d/%m/%Y")
                    row["Status"] = new_status

                    # Recalculate Net Price using existing discount and new price
                    discount = Decimal(row.get("Discount").strip("%")) #type: ignore
                    price = Decimal(new_price_per_unit)
                    net_price = price * (Decimal("1") - discount / Decimal("100"))
                    row["Net Price"] = f"${net_price.quantize(Decimal('0.01')):,}"

                    updated = True  # Confirm successful update
                    break

        # Raise an error if the batch number was not found
        if not updated:
            raise ValueError(f"Item batch number '{batch_number}' not found.")

        # Save the updated inventory back to the file
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writeheader()
            writer.writerows(items)

    def search(self, keyword):
        """
        Search inventory items by checking if the keyword matches the start of key fields (case-insensitive).

        Args:
            keyword (str): The search term to match against inventory fields.

        Returns:
            list: A list of matching inventory rows where the keyword is a prefix in relevant fields.
        """
        # Convert to lowercase for case-insensitive matching
        keyword = keyword.lower()
        matched_items = []

        # Open the inventory file and read all items (skip header)
        with open(self.filename, "r", newline="") as file:
            reader = csv.reader(file)
            items = list(reader)[1:]  # Exclude header row

            # Check if the keyword matches the start of any of the selected fields: 
            # Category, Item Name, SKU, or Barcode (columns 1 to 4)
            for row in items:
                if any(row[i].lower().startswith(keyword) for i in range(1, 5)):
                    matched_items.append(row)

        return matched_items
    
    def checkout_find(self, barcode):
        """
        Locate the inventory item matching the barcode with available stock, prioritizing earliest expiry.

        Args:
            barcode (str): The barcode of the item to find.

        Returns:
            dict: The inventory record for the matching item with the soonest expiry date.
        """
        barcode = barcode.strip()
        # Validate barcode format
        InventoryValidator.validate_barcode(barcode)

        matches = []
        # Collect all items with matching barcode and positive quantity
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expiry = datetime.strptime(row.get("Expiry Date"), "%d/%m/%Y").date() # type: ignore
                today = date.today()
                if row.get("Barcode") == barcode and int(row.get("Quantity")) > 0 and today <= expiry:  # type: ignore
                    matches.append(row)
        
        # Raise error if no available stock found for barcode
        if not matches:
            raise ValueError("No available stock found for the entered barcode.")
                
        # Choose the item with the earliest expiry date (FIFO by expiry)
        earliest_expiry = datetime.strptime("9/9/9999", "%d/%m/%Y")  # Placeholder far future date
        for row in matches:
            expiry = datetime.strptime(row.get("Expiry Date"), "%d/%m/%Y")
            if expiry < earliest_expiry:
                earliest_expiry = expiry
                item = row

        return item # type: ignore

    def delete(self, batch_number):
        """
        Remove an inventory item identified by its unique batch number.

        Args:
            batch_number (str): The batch number of the item to delete.
        """
        # Load all items except the one with the given batch number
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            items = [row for row in reader if row.get("Batch Number") != batch_number]

        # Save the filtered list back to the file, effectively deleting the item
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(items)

    def find_by_status(self, status):
        """
        Retrieve all inventory items matching a specific status.

        Args:
            status (str): The inventory status to filter by (e.g., 'Expired', 'Low Stock').

        Returns:
            list: A list of rows (items) that have the given status.
        """
        matched_items = []
        with open(self.filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if row has enough columns and status matches the requested one
                if len(row) >= 14 and row[13] == status:
                    matched_items.append(row)
        return matched_items

    def calculate_stock_value(self, value_type):
        """
        Calculate the total inventory value based on either cost or net price.

        Args:
            value_type (str): Specify 'cost' to calculate based on cost per unit,
                            or 'price' to calculate based on net selling price.

        Returns:
            str: Formatted total value as a string with two decimal places and commas.
        """
        # Determine which column to use for calculation
        if value_type.lower() == "cost":
            column_name = "Cost per Unit"
        elif value_type.lower() == "price":
            column_name = "Net Price"
        else:
            raise ValueError("Invalid value type")

        total = Decimal('0')
        # Calculate sum of quantity multiplied by unit value for all items
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                total += Decimal(row.get("Quantity")) * Decimal(row.get(column_name).strip("$").replace(",",""))  # type: ignore
        return f"${total.quantize(Decimal('0.01')):,}"

    def count_items(self, status=None):
        """
        Count inventory items optionally filtered by status.

        Args:
            status (str, optional): Inventory status to filter by (e.g., "Available", "Expired").
                                    If None, counts all items.

        Returns:
            int: Number of items matching the filter or total items if no filter is applied.
        """
        total = 0
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not status:  # Count all items if no status filter
                    total += 1
                elif row.get("Status").lower() == status.lower():  #type:ignore
                    total += 1
        return total
    
    def count_item_quantity(self, barcode):
        """
        Get the quantity available for a specific item by barcode.

        Args:
            barcode (str): Barcode of the item.
        Returns:
            int: Quantity available for the specified item. Returns 0 if not found.
        """
        total_item_quantity = 0
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Barcode") == barcode and row.get("Status") != "Expired":
                    total_item_quantity += int(row.get("Quantity"))  # type: ignore
        return total_item_quantity

    def reduce_stock_quantity(self, barcode, quantity_to_reduce, item_name):
        """
        Decrease stock quantity for a given barcode after a checkout, validating availability.

        Args:
            barcode (str): Barcode of the item to reduce.
            quantity_to_reduce (str): Number of units to deduct from stock.
            item_name (str): Name of the item (used in error messages).

        Notes:
            Uses FIFO (first-expired-first-out) logic to reduce stock from oldest batches first.
        """
        quantity_to_reduce = int(quantity_to_reduce)
        
        # Calculate total available stock for this barcode excluding expired items
        total_stock_quantity = self.count_item_quantity(barcode)
        # Validate sufficient stock before proceeding
        if total_stock_quantity < quantity_to_reduce:
            raise ValueError(
                f"Not enough stock for item '{item_name}' or the item is expired.\n"
                f"Requested quantity: {quantity_to_reduce}, available: {total_stock_quantity}."
            )

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            items = list(reader)
            # Reduce stock quantity from oldest batches
            for row in reversed(items):
                if row.get("Barcode") == barcode and row.get("Status") != "Expired":
                    stock_quantity = int(row.get("Quantity"))  # type: ignore
                    final_quantity = stock_quantity - quantity_to_reduce

                    if final_quantity >= 0:
                        row["Quantity"] = str(final_quantity)
                        break  # Reduction complete
                    else:
                        # Use up this batch completely and continue reducing remaining quantity from other batches
                        row["Quantity"] = "0"
                        quantity_to_reduce -= stock_quantity

        # Write updated stock back to file
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writeheader()
            writer.writerows(items)

    def apply_inventory_discount(self, barcode, batch_number, discount_amount):
        """
        Apply a percentage discount to a specific inventory item batch and update net price.

        Args:
            barcode (str): Barcode of the item to discount.
            batch_number (str): Batch number of the item.
            discount_amount (int): Discount percentage to apply.

        Notes:
            Updates the 'Discount' and 'Net Price' fields for the specified batch.
        """
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            items = list(reader)
            for row in items:
                if row.get("Barcode") == barcode and row.get("Batch Number") == batch_number:
                    price = Decimal(row.get("Price per Unit").strip("$").replace(",", ""))  # type: ignore
                    discounted_price = price - (price * Decimal(discount_amount) / Decimal(100))
                    row["Discount"] = f"{discount_amount}%"
                    row["Net Price"] = f"${discounted_price.quantize(Decimal('0.01')):,}"
                    break

        # Save updated inventory data
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writeheader()
            writer.writerows(items)

    def update_item_statuses(self):
        """
        Automatically update inventory item statuses based on expiry dates and stock levels.

        Logic:
            - Status is set to 'Expired' if current date is past expiry date.
            - 'Out of Stock' if quantity is zero.
            - 'Low Stock' if quantity is at or below minimum stock.
            - Otherwise 'Available'.
        """
        today = date.today()

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            items = list(reader)

        # Update status for each item
        for row in items:
            quantity = int(row["Quantity"])
            minimum_stock = int(row["Minimum Stock"])
            expiry_date = datetime.strptime(row["Expiry Date"], "%d/%m/%Y").date()

            row["Status"] = InventoryHelpers.set_item_status(quantity, minimum_stock, expiry_date)

        # Write updated statuses back to file
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writeheader()
            writer.writerows(items)


class InventoryHelpers:
    """
    Utility helper class for inventory-related operations.

    Provides static methods for:
    - Generating unique SKU codes based on category and item name.
    - Determining item stock status based on quantity, minimum stock, and expiry date.
    """

    @staticmethod
    def generate_SKU(filename, category, item_name):
        """
        Generate a unique SKU (Stock Keeping Unit) for an inventory item.

        SKU format: CATEGORY-ITEMNUMBER-XXX
          - CATEGORY: First 4 uppercase letters of category
          - ITEMNUMBER: First 1 to 4 letters + optional digits extracted from item name
          - XXX: Incrementing 3-digit number ensuring uniqueness

        Args:
            filename (str): Path to the inventory CSV file to check existing SKUs.
            category (str): Category name of the item.
            item_name (str): Item name used to extract SKU components.

        Returns:
            str: Unique SKU string.

        Process:
            1. Extract category prefix (first 4 letters, uppercase).
            2. Extract first letters and digits from item name.
            3. Append incrementing number starting from 001.
            4. Check if SKU exists:
               - If SKU exists with same item name, reuse it.
               - If SKU exists with different item, increment number and retry.
            5. Return unique SKU.
        """
        # Extract category prefix (4 letters uppercase)
        first_part = category[0:4].upper()

        # Extract letters and optional digits from item name
        second_part = ""
        result = re.search(r"^([a-z]{1,4})(?:.*?(\d{1,4}))?", item_name, re.IGNORECASE)
        if result:
            result_first_part = result.group(1).upper()
            result_second_part = result.group(2) if result.group(2) else ""
            second_part = result_first_part + result_second_part

        # Initialize SKU number suffix
        third_part = 1
        sku = f"{first_part}-{second_part}-{third_part:03}"

        # Loop to ensure SKU is unique by checking the inventory file
        retry = True
        while retry:
            with open(filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("SKU") == sku:
                        # If SKU exists with same item, reuse SKU (no increment)
                        if row.get("Item Name") == item_name:
                            retry = False # SKU is unique
                            break
                        else:
                            # Increment number to generate unique SKU
                            third_part += 1
                            sku = f"{first_part}-{second_part}-{third_part:03}"
                            break
                else:
                    retry = False # SKU is unique

        return sku

    @staticmethod
    def set_item_status(quantity, minimum_stock, expiry_date):
        """
        Determine inventory status of an item based on quantity and expiry.

        Args:
            quantity (int): Current stock quantity of the item.
            minimum_stock (int): Minimum stock threshold for warning.
            expiry_date (date): Expiry date of the item.

        Returns:
            str: Expired, Out of Stock, Low Stock or Available status:
        """
        if date.today() > expiry_date:
            return "Expired"
        elif quantity == 0:
            return "Out of Stock"
        elif quantity <= minimum_stock:
            return "Low Stock"
        else:
            return "Available"


class InventoryValidator:
    """
    Validator class to ensure data integrity for inventory fields.

    Contains static methods to validate:
    - Item name format and length
    - EAN-13 barcode correctness including checksum
    - Batch number format and uniqueness in inventory
    - Numeric fields meet required positive value constraints
    """

    @staticmethod
    def validate_item_name(item_name):
        """
        Validate item name string for allowed characters and length.

        Args:
            item_name (str): Name of the inventory item.
        """
        if not item_name:
            raise ValueError("Item name must not be empty.")
        elif not re.search(r"^[a-zA-Z0-9\- ]+$", item_name):
            raise ValueError("Item name can only contain letters, numbers, spaces, or dashes.")
        elif len(item_name) > 50:
            raise ValueError("Item name must not exceed 50 characters.")

    @staticmethod
    def validate_barcode(barcode):
        """
        Validate EAN-13 barcode length, numeric format, and checksum correctness.

        Args:
            barcode (str): Barcode string to validate.
        
        Algorithm:
            - Sum of digits in even positions (index 1,3,5...) multiplied by 3
            - Sum of digits in odd positions (index 0,2,4...)
            - Calculate checksum digit and compare with last digit
        """
        if len(barcode) != 13:
            raise ValueError("Barcode (EAN-13) must be 13 digits long.")
        elif not barcode.isnumeric():
            raise ValueError("Barcode must contain digits only.")
        
        # Calculate checksum for EAN-13
        even_position_digits = sum(int(num) for num in barcode[1:12:2]) * 3
        odd_position_digits = sum(int(num) for num in barcode[:12:2])
        digits_sum = even_position_digits + odd_position_digits
        checksum = 0 if digits_sum % 10 == 0 else 10 - (digits_sum % 10)

        if int(barcode[12]) != checksum:
            raise ValueError("Invalid barcode: checksum does not match, please check the barcode number.")

    @staticmethod
    def validate_batch_number(filename, barcode, batch_number):
        """
        Validate batch number format and ensure it is unique for the given product in the inventory file.

        Args:
            filename (str): Inventory CSV file path to check uniqueness.
            barcode (str): Product barcode to match.
            batch_number (str): Batch number string to validate.
        """
        if not batch_number:
            raise ValueError("Batch number must not be empty.")
        elif not re.search(r"^[a-zA-Z0-9\-]+$", batch_number):
            raise ValueError("Batch number can only contain letters, numbers, or dashes.")
        elif len(batch_number) > 20:
            raise ValueError("Batch number must not exceed 20 characters.")

        # Check for duplicates in inventory CSV
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Barcode") == barcode and row.get("Batch Number") == batch_number:
                    raise ValueError(
                        f"Batch number '{batch_number}' already exists for product with barcode '{barcode}'. "
                        "\nPlease enter a unique batch number for this product.")

    @staticmethod
    def validate_numeric_fields(quantity, minimum_stock, cost_per_unit, price_per_unit):
        """
        Validate numeric inventory fields for correct types and positive values.

        Args:
            quantity (int): Stock quantity, must be positive integer.
            minimum_stock (int): Minimum stock threshold, must be positive integer.
            cost_per_unit (Decimal): Cost per unit, must be positive number.
            price_per_unit (Decimal): Price per unit, must be positive number.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer")
        elif not isinstance(minimum_stock, int) or minimum_stock < 0:
            raise ValueError("Minimum stock must be a positive integer.")
        elif not isinstance(cost_per_unit, (Decimal)) or cost_per_unit <= 0:
            raise ValueError("Cost per unit must be a positive number greater than zero.")
        elif not isinstance(price_per_unit, (Decimal)) or price_per_unit <= 0:
            raise ValueError("Price per unit must be a positive number greater than zero.")



