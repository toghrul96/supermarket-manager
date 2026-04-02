import os
import re
from datetime import datetime, date
from decimal import Decimal
from dotenv import load_dotenv
from supabase import create_client


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

class InventoryData():
    """
    Handles inventory management with product and inventory (batch) tables.
    
    Schema:
    - product: category, item_name, sku, barcode, minimum_stock, availability
    - inventory: product_id, batch_number, quantity, cost_per_unit (cents), 
                 price_per_unit (cents), discount (0-100), net_price (cents),
                 received_date, expiry_date, expiry_condition (boolean)
    """
    def __init__(self, supabase=None, access_token=None, refresh_token=None):
        """Initialize with Supabase credentials and session tokens.

        The supabase parameter is accepted but not stored — each worker thread
        creates its own client via thread-local storage to avoid corrupting the
        shared httpx HTTP/2 connection pool.

        Args:
            supabase: Unused. Kept for call-site compatibility.
            access_token (str): JWT from the logged-in session. Passed to every
                                thread-local client so RLS policies apply correctly.
            refresh_token (str): Refresh token paired with access_token.
        """
        import threading
        _load_env()
        self._url = os.getenv("SUPABASE_URL")
        self._key = os.getenv("SUPABASE_KEY")
        if not self._url or not self._key:
            raise ValueError("Missing Supabase credentials in .env file")

        # Auth tokens inherited from the logged-in UserDatabase session.
        self._access_token = access_token
        self._refresh_token = refresh_token

        # Thread-local storage: each thread gets its own supabase client
        # and therefore its own httpx HTTP/2 connection pool.
        # Sharing one client across threads corrupts the HTTP/2 pool.
        self._local = threading.local()

        # barcode (int) → product_id cache shared across threads.
        # Python dict reads/writes are for simple key lookups.
        self._product_id_cache: dict = {}

    @property
    def supabase(self):
        """Return a thread-local supabase client, creating one if needed."""
        if not hasattr(self._local, 'client'):
            client = create_client(self._url, self._key) #type: ignore
            if self._access_token and self._refresh_token:
                try:
                    # set_session validates the JWT via a network call to /auth/v1/user.
                    # If that round-trip succeeds, supabase-py automatically updates
                    # the postgrest auth headers for us.
                    client.auth.set_session(self._access_token, self._refresh_token)
                except Exception:
                    # set_session timed out or failed. Fall back to setting the JWT
                    # directly on the postgrest client — no network call needed.
                    # returns self, so RLS-protected queries still work correctly.
                    client.postgrest.auth(self._access_token)
            self._local.client = client
        return self._local.client
    
    def add_item(self, category, item_name, barcode, batch_number, 
                 quantity, minimum_stock, cost_per_unit, price_per_unit, expiry_date):
        """
        Add a new inventory batch. Creates product if doesn't exist.
        
        Args:
            cost_per_unit (Decimal): Price in dollars
            price_per_unit (Decimal): Price in dollars
        """
        # Validate inputs
        item_name = item_name.strip().title()
        InventoryValidator.validate_item_name(item_name)
        barcode = int(barcode.strip())
        batch_number = batch_number.strip().upper()
        InventoryValidator.validate_batch_number(batch_number)
        InventoryValidator.validate_numeric_fields(quantity, minimum_stock, cost_per_unit, price_per_unit)
        
        # Convert prices from dollars to cents
        cost_cents = int(cost_per_unit * 100)
        price_cents = int(price_per_unit * 100)
        
        # Find or create product
        product = self.supabase.table("product").select("*").eq(
            "barcode", barcode
        ).execute()
        
        if not product.data:
            # Create new product
            sku = InventoryHelpers.generate_SKU(self.supabase, category, item_name)
            new_product = {
                "category": category,
                "item_name": item_name,
                "sku": sku,
                "barcode": barcode,
                "minimum_stock": minimum_stock,
                "availability": "available"
            }
            product_response = self.supabase.table("product").insert(new_product).execute()
            product_id = product_response.data[0]["id"] #type: ignore
        else:
            product_id = product.data[0]["id"] #type: ignore
        
        # Calculate net price and expiry condition
        discount = 0  # Default no discount
        net_price = price_cents * (100 - discount) // 100
        expiry_condition = date.today() > expiry_date
        
        # Create inventory batch
        batch = {
            "product_id": product_id,
            "batch_number": batch_number,
            "quantity": quantity,
            "cost_per_unit": cost_cents,
            "price_per_unit": price_cents,
            "discount": discount,
            "net_price": net_price,
            "received_date": datetime.now().isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "expiry_condition": expiry_condition
        }
        
        self.supabase.table("inventory").insert(batch).execute()
        
        # Update product availability
        self._update_product_availability(product_id)

    def update_item(self, new_category, new_item_name, batch_number, new_quantity, 
                    new_minimum_stock, new_cost_per_unit, new_price_per_unit, new_expiry_date,
                    new_batch_number=None):
        """Update an inventory batch and its product."""
        # Validate
        new_item_name = new_item_name.strip().title()
        InventoryValidator.validate_item_name(new_item_name)
        InventoryValidator.validate_numeric_fields(new_quantity, new_minimum_stock, 
                                                    new_cost_per_unit, new_price_per_unit)
        if new_batch_number:
            new_batch_number = new_batch_number.strip().upper()
            InventoryValidator.validate_batch_number(new_batch_number)
        
        # Convert to cents
        cost_cents = int(new_cost_per_unit * 100)
        price_cents = int(new_price_per_unit * 100)
        
        # Get batch
        batch = self.supabase.table("inventory").select("*, product_id").eq(
            "batch_number", batch_number
        ).execute()
        
        if not batch.data:
            raise ValueError(f"Batch '{batch_number}' not found")
        
        product_id = batch.data[0]["product_id"] #type: ignore
        discount = batch.data[0]["discount"] #type: ignore
        
        # Calculate new values
        net_price = price_cents * (100 - discount) // 100 #type: ignore
        expiry_condition = date.today() > new_expiry_date
        
        # Update batch
        update_data = {
            "quantity": new_quantity,
            "cost_per_unit": cost_cents,
            "price_per_unit": price_cents,
            "net_price": net_price,
            "expiry_date": new_expiry_date.isoformat(),
            "expiry_condition": expiry_condition
        }
        # Only update batch number if a new one is provided and it differs from the current
        if new_batch_number and new_batch_number != batch_number:
            update_data["batch_number"] = new_batch_number
        
        self.supabase.table("inventory").update(update_data).eq(
            "batch_number", batch_number
        ).execute()
        
        # Update product
        new_sku = InventoryHelpers.generate_SKU(self.supabase, new_category, new_item_name)
        self.supabase.table("product").update({
            "category": new_category,
            "item_name": new_item_name.strip().title(),
            "sku": new_sku,
            "minimum_stock": new_minimum_stock
        }).eq("id", product_id).execute()
        
        # Update availability
        self._update_product_availability(product_id)

    def search(self, keyword):
        """
        Search inventory batches with product info.
        Returns rows formatted for UI display with status column.
        """
        keyword = keyword.lower()
        
        # Get all inventory with product details
        response = self.supabase.table("inventory").select(
            "*, product(category, item_name, sku, barcode, availability, minimum_stock)"
        ).execute()
        
        matched = []
        for row in (response.data or []):
            if isinstance(row, dict) and row.get("product"):
                product = row["product"]
                # Search in category, item_name, sku, barcode, batch_number
                searchable = f"{product.get('category', '')} {product.get('item_name', '')} {product.get('sku', '')} {str(product.get('barcode', ''))} {row.get('batch_number', '')}".lower()  #type: ignore
                
                if keyword in searchable or searchable.startswith(keyword):
                    # Calculate status for display
                    status = self._calculate_status(row, product)
                    
                    # Format for UI - column order matches ui_main.py:
                    # Item Name, Batch Number, Quantity, Cost per Unit, Price per Unit,
                    # Discount, Net Price, Received Date, Expiry Date, Status
                    ui_row = [
                        product.get("item_name"), #type: ignore
                        row.get("batch_number"),
                        str(row.get("quantity")),
                        f"${row.get('cost_per_unit', 0) / 100:.2f}", #type: ignore
                        f"${row.get('price_per_unit', 0) / 100:.2f}", #type: ignore
                        f"{row.get('discount')}%",
                        f"${row.get('net_price', 0) / 100:.2f}", #type: ignore
                        row.get("received_date"),
                        row.get("expiry_date"),
                        status
                    ]
                    matched.append(ui_row)
        
        return matched
    
    def checkout_find(self, barcode):
        """
        Find available inventory batch for checkout (FIFO by expiry).
        Returns dict with product and batch info.
        """
        try:
            barcode = int(barcode.strip())
        except ValueError:
            raise ValueError("Please enter a valid barcode number (digits only).")
        
        # Get product
        product = self.supabase.table("product").select("*").eq(
            "barcode", barcode
        ).execute()
        
        if not product.data:
            raise ValueError("Product not found")
        
        product_id = product.data[0]["id"] #type: ignore
        # Cache so count_item_quantity skips the product lookup for this barcode
        self._product_id_cache[barcode] = product_id
        
        # Get non-expired batches with quantity > 0, ordered by expiry
        batches = self.supabase.table("inventory").select("*").eq(
            "product_id", product_id
        ).eq("expiry_condition", False).gt("quantity", 0).order(
            "expiry_date", desc=False
        ).execute()
        
        if not batches.data:
            raise ValueError("No available stock found for the entered barcode")
        
        # Return first batch (earliest expiry)
        batch = batches.data[0]
        
        # Format for checkout (match what checkout expects)
        return {
            "SKU": product.data[0]["sku"], #type: ignore
            "Barcode": str(barcode),
            "Item Name": product.data[0]["item_name"], #type: ignore
            "Price per Unit": f"${batch['price_per_unit'] / 100:.2f}", #type: ignore
            "Discount": f"{batch['discount']}%", #type: ignore
            "Net Price": f"${batch['net_price'] / 100:.2f}" #type: ignore
        }

    def delete(self, batch_number):
        """Delete an inventory batch."""
        # Get product_id before deleting
        batch = self.supabase.table("inventory").select("product_id").eq(
            "batch_number", batch_number
        ).execute()
        
        if not batch.data:
            raise ValueError(f"Batch '{batch_number}' not found")
        
        product_id = batch.data[0]["product_id"] #type: ignore
        
        # Delete batch
        self.supabase.table("inventory").delete().eq(
            "batch_number", batch_number
        ).execute()
        
        # Update product availability
        self._update_product_availability(product_id)

    def find_by_status(self, status):
        """Find inventory batches by status, filtering at the DB level.

        For availability-based statuses (Available, Low Stock, Out of Stock)
        we query the product table first — PostgREST cannot filter on embedded
        foreign-table columns, so the old .eq("product.availability", ...) was
        silently ignored and every row was fetched. Querying products first and
        using .in_("product_id", ids) pushes the filter to the database and
        returns only the rows we actually need.
        """
        status_lower = status.lower()

        if status_lower == "expired":
            # expiry_condition lives on the inventory table - filter directly
            response = self.supabase.table("inventory").select(
                "*, product(category, item_name, sku, barcode, availability, minimum_stock)"
            ).eq("expiry_condition", True).execute()
        else:
            # Map UI label -> DB availability value
            avail_map = {
                "available":    "available",
                "low stock":    "low stock",
                "out of stock": "out of stock",
            }
            db_avail = avail_map.get(status_lower)
            if db_avail is None:
                return []

            # Step 1: fetch only matching product IDs
            products = self.supabase.table("product").select("id").eq(
                "availability", db_avail
            ).execute()

            if not products.data:
                return []

            product_ids = [p["id"] for p in products.data] #type: ignore

            # Step 2: fetch inventory rows for those products only
            response = self.supabase.table("inventory").select(
                "*, product(category, item_name, sku, barcode, availability, minimum_stock)"
            ).in_("product_id", product_ids).execute()

        matched = []
        for row in (response.data or []):
            if isinstance(row, dict) and row.get("product"):
                product = row["product"]
                calc_status = self._calculate_status(row, product)
                # Skip rows whose calculated status doesn't match the requested filter
                if calc_status.lower() != status_lower:
                    continue
                ui_row = [
                        product.get("item_name"), #type: ignore
                        row.get("batch_number"),
                        str(row.get("quantity")),
                        f"${row.get('cost_per_unit', 0) / 100:.2f}", #type: ignore
                        f"${row.get('price_per_unit', 0) / 100:.2f}", #type: ignore
                        f"{row.get('discount')}%",
                        f"${row.get('net_price', 0) / 100:.2f}", #type: ignore
                        row.get("received_date"),
                        row.get("expiry_date"),
                        calc_status
                    ]
                matched.append(ui_row)

        return matched

    def calculate_stock_value(self, value_type):
        """Calculate total inventory value."""
        response = self.supabase.table("inventory").select("quantity, cost_per_unit, net_price").execute()
        
        total = 0
        for row in (response.data or []):
            qty = row.get("quantity", 0) #type: ignore
            # Use cost price or net selling price depending on value_type
            if value_type.lower() == "cost":
                total += qty * row.get("cost_per_unit", 0) #type: ignore
            else:
                total += qty * row.get("net_price", 0) #type: ignore
        
        # Convert cents to dollars
        return f"${total / 100:.2f}"

    def count_items(self, status=None):
        """Count inventory batches by status."""
        if not status:
            # Count all batches
            response = self.supabase.table("inventory").select("id", count="exact").execute()  # type: ignore
            return response.count or 0
        
        # Count by status
        response = self.supabase.table("inventory").select(
            "*, product(availability)"
        ).execute()
        
        count = 0
        for row in (response.data or []):
            if isinstance(row, dict) and row.get("product"):
                calc_status = self._calculate_status(row, row["product"])
                if calc_status.lower() == status.lower():
                    count += 1
        
        return count

    def count_item_quantity(self, barcode):
        """Get total available quantity for a product."""
        barcode = int(barcode)

        # Use cached product_id if checkout_find already looked it up —
        # this saves one DB round trip on every +/- button press.
        if barcode in self._product_id_cache:
            product_id = self._product_id_cache[barcode]
        else:
            product = self.supabase.table("product").select("id").eq("barcode", barcode).execute()
            if not product.data:
                return 0
            product_id = product.data[0]["id"] #type: ignore
            self._product_id_cache[barcode] = product_id

        # Sum quantities of non-expired batches
        batches = self.supabase.table("inventory").select("quantity").eq(
            "product_id", product_id
        ).eq("expiry_condition", False).execute()
        
        total = sum(row.get("quantity", 0) for row in (batches.data or [])) #type: ignore
        return total

    def reduce_stock_quantity(self, barcode, quantity_to_reduce, item_name):
        """Reduce stock using FIFO (earliest expiry first)."""
        barcode = int(barcode)
        quantity_to_reduce = int(quantity_to_reduce)
        
        # Get product
        product = self.supabase.table("product").select("id").eq("barcode", barcode).execute()
        if not product.data:
            raise ValueError(f"Product not found")
        
        product_id = product.data[0]["id"] #type: ignore
        
        # Check available stock
        total_available = self.count_item_quantity(barcode)
        if total_available < quantity_to_reduce:
            raise ValueError(
                f"Not enough stock for item '{item_name}'.\n"
                f"Requested: {quantity_to_reduce}, available: {total_available}."
            )
        
        # Get batches ordered by expiry (FIFO)
        batches = self.supabase.table("inventory").select("*").eq(
            "product_id", product_id
        ).eq("expiry_condition", False).order("expiry_date", desc=False).execute()
        
        remaining = quantity_to_reduce
        for batch in (batches.data or []):
            if remaining <= 0:
                break
            
            batch_qty = batch.get("quantity", 0) #type: ignore
            batch_id = batch.get("id") #type: ignore
            
            if batch_qty >= remaining: #type: ignore
                # This batch has enough — deduct only what's needed
                new_qty = batch_qty - remaining #type: ignore
                self.supabase.table("inventory").update({
                    "quantity": new_qty
                }).eq("id", batch_id).execute()
                remaining = 0
            else:
                # Use up entire batch
                self.supabase.table("inventory").update({
                    "quantity": 0
                }).eq("id", batch_id).execute()
                remaining -= batch_qty #type: ignore
        
        # Update product availability
        self._update_product_availability(product_id)

    def get_all_products(self):
        """
        Fetch all products ordered by category then item name.

        Returns:
            list[dict]: Each dict has keys id, category, item_name, sku,
                        barcode, minimum_stock, availability.
        """
        response = self.supabase.table("product").select(
            "id, category, item_name, sku, barcode, minimum_stock, availability"
        ).order("category").order("item_name").execute()
        return response.data or []

    def add_product(self, category, item_name, barcode, minimum_stock):
        """
        Add a brand-new product (no batch) to the product table.

        Args:
            category (str): Product category.
            item_name (str): Product name (will be title-cased).
            barcode (str): 13-digit EAN barcode string.
            minimum_stock (int): Reorder threshold.

        Raises:
            ValueError: If barcode already exists or inputs are invalid.
        """
        item_name = item_name.strip().title()
        InventoryValidator.validate_item_name(item_name)
        InventoryValidator.validate_barcode(barcode)

        # Prevent duplicate products with the same barcode
        existing = self.supabase.table("product").select("id").eq(
            "barcode", int(barcode)
        ).execute()
        if existing.data:
            raise ValueError("A product with this barcode already exists.")

        sku = InventoryHelpers.generate_SKU(self.supabase, category, item_name)
        self.supabase.table("product").insert({
            "category": category,
            "item_name": item_name,
            "sku": sku,
            "barcode": int(barcode),
            "minimum_stock": int(minimum_stock),
            "availability": "out of stock",
        }).execute()

    def update_product(self, product_id, category, item_name, minimum_stock):
        """
        Update a product's editable fields. Barcode is never changed.

        Args:
            product_id: The product's primary key (uuid or int).
            category (str): New category.
            item_name (str): New item name (will be title-cased).
            minimum_stock (int): New reorder threshold.

        Raises:
            ValueError: If item_name fails validation or product not found.
        """
        item_name = item_name.strip().title()
        InventoryValidator.validate_item_name(item_name)

        # Regenerate SKU since category or item name may have changed
        new_sku = InventoryHelpers.generate_SKU(self.supabase, category, item_name)
        result = self.supabase.table("product").update({
            "category": category,
            "item_name": item_name,
            "sku": new_sku,
            "minimum_stock": int(minimum_stock),
        }).eq("id", product_id).execute()

        if not result.data:
            raise ValueError("Product not found.")

    def apply_inventory_discount(self, batch_number, discount_amount):
        """Apply discount to a batch."""
        # Get batch
        batch = self.supabase.table("inventory").select("price_per_unit").eq(
            "batch_number", batch_number
        ).execute()
        
        if not batch.data:
            raise ValueError("Batch not found")
        
        price_cents = batch.data[0]["price_per_unit"] #type: ignore
        net_price = price_cents * (100 - discount_amount) // 100
        
        # Update
        self.supabase.table("inventory").update({
            "discount": discount_amount,
            "net_price": net_price
        }).eq("batch_number", batch_number).execute()

    def update_item_statuses(self):
        """Update expiry_condition for all batches and product availability.
        Uses bulk UPDATE calls instead of one request per row (N+1).
        """
        from collections import defaultdict
        today = date.today()

        batches = self.supabase.table("inventory").select("id, expiry_date").execute()
        expired_ids, fresh_ids = [], []
        for batch in (batches.data or []):
            expiry = datetime.fromisoformat(batch["expiry_date"]).date() #type: ignore
            (expired_ids if today > expiry else fresh_ids).append(batch["id"]) #type: ignore
        if expired_ids:
            self.supabase.table("inventory").update({"expiry_condition": True}).in_("id", expired_ids).execute()
        if fresh_ids:
            self.supabase.table("inventory").update({"expiry_condition": False}).in_("id", fresh_ids).execute()

        all_inv = self.supabase.table("inventory").select("product_id, quantity, expiry_condition").execute()
        # Accumulate non-expired stock totals per product
        stock_by_product: dict = defaultdict(int)
        for row in (all_inv.data or []):
            if not row.get("expiry_condition"): #type: ignore
                stock_by_product[row["product_id"]] += row.get("quantity", 0) #type: ignore

        products = self.supabase.table("product").select("id, minimum_stock").execute()
        out_ids, low_ids, avail_ids = [], [], []
        for product in (products.data or []):
            pid = product["id"] #type: ignore
            qty = stock_by_product.get(pid, 0)
            min_s = product.get("minimum_stock", 0) #type: ignore
            if qty == 0:
                out_ids.append(pid)
            elif qty <= min_s: #type: ignore
                low_ids.append(pid)
            else:
                avail_ids.append(pid)

        if out_ids:
            self.supabase.table("product").update({"availability": "out of stock"}).in_("id", out_ids).execute()
        if low_ids:
            self.supabase.table("product").update({"availability": "low stock"}).in_("id", low_ids).execute()
        if avail_ids:
            self.supabase.table("product").update({"availability": "available"}).in_("id", avail_ids).execute()

    def _update_product_availability(self, product_id):
        """Calculate and update product availability based on total quantity."""
        # Get product minimum_stock
        product = self.supabase.table("product").select("minimum_stock").eq(
            "id", product_id
        ).execute()
        
        if not product.data:
            return
        
        min_stock = product.data[0]["minimum_stock"] #type: ignore
        
        # Sum all non-expired batch quantities
        batches = self.supabase.table("inventory").select("quantity").eq(
            "product_id", product_id
        ).eq("expiry_condition", False).execute()
        
        total_qty = sum(row.get("quantity", 0) for row in (batches.data or [])) #type: ignore
        
        # Determine availability
        if total_qty == 0:
            availability = "out of stock"
        elif total_qty <= min_stock:
            availability = "low stock"
        else:
            availability = "available"
        
        # Update product
        self.supabase.table("product").update({
            "availability": availability
        }).eq("id", product_id).execute()

    def _calculate_status(self, batch, product):
        """
        Calculate display status for a batch.
        Priority: Out of Stock > Expired > (availability from product)
        """
        # First check if product is out of stock
        if product.get("availability") == "out of stock":
            return "Out of Stock"
        
        # Then check if batch is expired
        if batch.get("expiry_condition"):
            return "Expired"
        
        # Otherwise use product availability
        avail = product.get("availability", "available")
        if avail == "low stock":
            return "Low Stock"
        elif avail == "out of stock":
            return "Out of Stock"
        else:
            return "Available"


class InventoryHelpers:
    """Helper methods for inventory operations."""
    
    @staticmethod
    def generate_SKU(supabase_client, category, item_name):
        """Generate unique SKU: CATEGORY-ITEMNAME-001"""
        first_part = category[0:4].upper()
        
        result = re.search(r"^([a-z]{1,4})(?:.*?(\d{1,4}))?", item_name, re.IGNORECASE)
        if result:
            second_part = result.group(1).upper()
            if result.group(2):
                second_part += result.group(2)
        else:
            second_part = "ITEM"
        
        # Find unique number
        num = 1
        while True:
            sku = f"{first_part}-{second_part}-{num:03d}"
            existing = supabase_client.table("product").select("sku, item_name").eq(
                "sku", sku
            ).execute()
            
            if not existing.data:
                break
            if existing.data[0].get("item_name") == item_name:
                # SKU already belongs to this item — reuse it
                break
            num += 1
        
        return sku


class InventoryValidator:
    """Input validation for inventory."""
    
    @staticmethod
    def validate_item_name(item_name):
        if not item_name:
            raise ValueError("Item name must not be empty")
        if not re.search(r"^[a-zA-Z0-9\- ]+$", item_name):
            raise ValueError("Item name can only contain letters, numbers, spaces, or dashes")
        if len(item_name) > 50:
            raise ValueError("Item name must not exceed 50 characters")
    
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
    def validate_numeric_fields(quantity, minimum_stock, cost_per_unit, price_per_unit):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer")
        if not isinstance(minimum_stock, int) or minimum_stock < 0:
            raise ValueError("Minimum stock must be a positive integer")
        if not isinstance(cost_per_unit, Decimal) or cost_per_unit <= 0:
            raise ValueError("Cost per unit must be positive")
        if not isinstance(price_per_unit, Decimal) or price_per_unit <= 0:
            raise ValueError("Price per unit must be positive")

    @staticmethod
    def validate_batch_number(batch_number):
        """
        Validate a batch number for correct format and length.

        Batch numbers must be non-empty, contain only uppercase letters,
        digits, and dashes, and must not exceed 20 characters. They are
        expected to be pre-stripped and uppercased by the caller before
        this method is invoked.

        Args:
            batch_number (str): The batch number string to validate.

        Raises:
            ValueError: If the batch number is empty, contains invalid
                        characters, or exceeds the maximum length.
        """
        if not batch_number:
            raise ValueError("Batch number must not be empty")
        if not re.search(r"^[A-Z0-9\-]+$", batch_number):
            raise ValueError("Batch number can only contain uppercase letters, digits, or dashes")
        if len(batch_number) > 20:
            raise ValueError("Batch number must not exceed 20 characters")