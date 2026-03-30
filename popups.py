import warnings
from decimal import Decimal
from PySide6.QtWidgets import (QDialog, QLineEdit, QMessageBox, QLabel,
                                QVBoxLayout, QHBoxLayout, QPushButton,
                                QTableWidget, QTableWidgetItem, QHeaderView,
                                QAbstractItemView, QComboBox, QSpinBox,
                                QSpacerItem, QSizePolicy, QStackedWidget)
from ui.ui_return_item_popup import Ui_ReturnItemPopup
from PySide6.QtCore import QDate, Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon
from ui.ui_add_item_popup import Ui_AddItemPopup
from ui.ui_add_user_popup import Ui_AddUserPopUp
from ui.ui_discount_item_popup import Ui_DialogPopUp
from ui.ui_account_popup import Ui_AccountInformation
from models.inventory import InventoryData, InventoryValidator
from models.user import UserDatabase
from worker import run_worker
from datetime import datetime


class AddNewItem(QDialog):
    """Dialog to add inventory items with input validation and secure storage.

    Two-step flow:
    - Step 1 (lookup): Only barcode field shown. User scans/types barcode and clicks Look Up.
    - Step 2a (existing product): Product info shown as read-only label, only batch fields shown.
    - Step 2b (new product): All fields shown to create product + first batch together.
    """

    def __init__(self, inventory_data=None, _skip_two_step=False):
        """Initialize the Add New Item dialog.

        Args:
            inventory_data: An existing InventoryData instance. If provided,
                            its authenticated Supabase client is reused.
            _skip_two_step: If True, show all fields immediately (used by UpdateItem).
        """
        super().__init__()
        self.inventory_data = inventory_data if inventory_data is not None else InventoryData()

        self.ui = Ui_AddItemPopup()
        self.ui.setupUi(self)

        # Override popup size immediately so _resize_to_content works from a clean state.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

        # Set input constraints
        self.ui.quantity_spinBox.setRange(0, 999999999)
        self.ui.minimum_stock_spinBox.setMaximum(999999999)
        self.ui.cost_doubleSpinBox.setRange(0.01, 999999999.0)
        self.ui.price_doubleSpinBox.setRange(0.01, 999999999.0)
        self.ui.expiry_dateEdit.setDate(QDate.currentDate())

        # Label to display lookup result (product found / not found)
        self._status_label = QLabel()
        self._status_label.setWordWrap(True)
        self._status_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 4px 0;")
        self.ui.main_layout.insertWidget(0, self._status_label)
        self._status_label.hide()

        # Stores found product data after a successful lookup
        self._found_product = None
        self._btn_connected = False
        self._skip_two_step = _skip_two_step
        self._thread = None
        self._relay = None  # Keep both refs alive

        if _skip_two_step:
            # UpdateItem uses this path — show all fields immediately
            self.ui.add_item_btn.clicked.connect(self.handle_add_item)
        else:
            self._set_lookup_mode()

    def showEvent(self, event):
        """Reset to lookup mode every time the dialog is opened."""
        super().showEvent(event)
        if not self._skip_two_step:
            self._set_lookup_mode()

    # -- helpers -------------------------------------------------------------- 

    def _resize_to_content(self):
        """Resize to visible content, clamp to screen, lock, and center — zero grow loop.

        Why NOT adjustSize():
            adjustSize() calls QWidget::resize() internally, which fires a
            resizeEvent() on an already-visible window.  That event causes Qt
            to recalculate minimum sizes for all child widgets, raising the
            stored minimumSizeHint, which triggers another resize, repeating
            indefinitely — the QWindowsWindow::setGeometry grow loop.

        Correct approach:
            1. Unlock  — clear any prior fixed size so the layout is free.
            2. Activate — force the layout engine to recompute sizes in memory
                          without touching the window geometry.
            3. Read     — sizeHint() returns the ideal size with zero side-effects.
            4. Clamp   — cap height so window + frame always fits the screen.
                          availableGeometry() already excludes the taskbar.
                          Subtract 50 px for the window title bar + bottom border.
            5. Lock     — setFixedSize() sets min == max == target in one call,
                          so the single resulting resizeEvent cannot grow further.
            6. Center   — move to screen centre, clamped to screen bounds.
        """
        from PySide6.QtWidgets import QApplication

        # 1 — unlock any previously locked size
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

        # 2 — force layout to recompute sizes in memory (no resize event)
        self.layout().activate() #type: ignore

        # 3 — read ideal size without triggering any resize event
        hint = self.sizeHint()
        w = hint.width()

        # 4 — clamp height: availableGeometry excludes taskbar; subtract 50 px
        #     for the OS window frame (title bar ~31 px + borders ~8 px = ~39 px,
        #     +11 px spare for any theme/DPI variation)
        screen = QApplication.primaryScreen().availableGeometry()
        h = min(hint.height(), screen.height() - 50)

        # 5 — single setFixedSize call = single resizeEvent, already the final size
        self.setFixedSize(w, h)

        # 6 — center within screen, never off-screen
        x = screen.x() + max(0, (screen.width()  - w) // 2)
        y = screen.y() + max(0, (screen.height() - h) // 2)
        self.move(x, y)

    def _set_product_fields_visible(self, visible):
        """Show/hide fields that only apply to brand-new products."""
        for w in [self.ui.label, self.ui.category_comboBox,
                  self.ui.item_name_label, self.ui.item_name_lineEdit,
                  self.ui.minimum_stock_label, self.ui.minimum_stock_spinBox]:
            w.setVisible(visible)

    def _set_batch_fields_visible(self, visible):
        """Show/hide batch-specific fields."""
        for w in [self.ui.batch_no_label, self.ui.batch_no_lineEdit,
                  self.ui.quantity_label, self.ui.quantity_spinBox,
                  self.ui.cost_label, self.ui.cost_doubleSpinBox,
                  self.ui.price_label, self.ui.price_doubleSpinBox,
                  self.ui.expiry_date_label, self.ui.expiry_dateEdit]:
            w.setVisible(visible)

    def _reconnect_btn(self, slot):
        """Disconnect all existing button signals and reconnect to slot."""
        if self._btn_connected:
            self.ui.add_item_btn.clicked.disconnect()
        self.ui.add_item_btn.clicked.connect(slot)
        self._btn_connected = True

    # -- states ---------------------------------------------------------------

    def _set_lookup_mode(self):
        """Step 1: Show only barcode field and Look Up button."""
        self._found_product = None
        self._status_label.hide()

        self.ui.barcode_label.show()
        self.ui.barcode_lineEdit.show()
        self.ui.barcode_lineEdit.setReadOnly(False)
        self.ui.barcode_lineEdit.clear()

        self._set_product_fields_visible(False)
        self._set_batch_fields_visible(False)

        self.ui.add_item_btn.setText("Look Up Barcode")
        self._reconnect_btn(self._lookup_barcode)
        QTimer.singleShot(0, self._resize_to_content)

    def _set_existing_product_mode(self, product):
        """Step 2a: Product found — show read-only info + batch fields only."""
        self._found_product = product

        self._status_label.setStyleSheet(
            "font-size: 12pt; font-weight: bold; padding: 4px 0; color: #27ae60;")
        self._status_label.setText(
            f"✓  {product['item_name']}  ·  {product['category']}")
        self._status_label.show()

        self.ui.barcode_lineEdit.setReadOnly(True)
        self._set_product_fields_visible(False)
        self._set_batch_fields_visible(True)

        self.ui.add_item_btn.setText("Add Batch")
        self._reconnect_btn(self.handle_add_item)
        QTimer.singleShot(0, self._resize_to_content)

    def _set_new_product_mode(self):
        """Step 2b: Product not found — show full form to create product + batch."""
        self._found_product = None

        self._status_label.setStyleSheet(
            "font-size: 12pt; font-weight: bold; padding: 4px 0; color: #e67e22;")
        self._status_label.setText("✗  New product — fill in all details below.")
        self._status_label.show()

        self.ui.barcode_lineEdit.setReadOnly(True)
        self._set_product_fields_visible(True)
        self._set_batch_fields_visible(True)

        self.ui.add_item_btn.setText("Add New Item")
        self._reconnect_btn(self.handle_add_item)
        QTimer.singleShot(0, self._resize_to_content)

    # -- actions --------------------------------------------------------------

    def _lookup_barcode(self):
        """Look up barcode in product table and switch to the appropriate mode."""
        barcode = self.ui.barcode_lineEdit.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Missing Barcode", "Please enter or scan a barcode.")
            return

        try:
            InventoryValidator.validate_barcode(barcode)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Barcode", str(e))
            return

        self.ui.add_item_btn.setEnabled(False)
        self.ui.add_item_btn.setText("Looking Up...")

        def fetch():
            response = self.inventory_data.supabase.table("product").select(
                "category, item_name, minimum_stock, barcode"
            ).eq("barcode", int(barcode)).execute()
            return response.data

        def on_result(data):
            self.ui.add_item_btn.setEnabled(True)
            if data:
                self._set_existing_product_mode(data[0])
            else:
                self._set_new_product_mode()

        def on_error(msg):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText("Look Up Barcode")
            QMessageBox.warning(self, "Lookup Failed", f"Could not look up barcode: {msg}")

        self._thread, self._relay = run_worker(fetch, on_result=on_result, on_error=on_error)

    def handle_add_item(self):
        """Process form and add item or batch depending on lookup result."""
        barcode = self.ui.barcode_lineEdit.text().strip()
        batch_number = self.ui.batch_no_lineEdit.text()
        quantity = self.ui.quantity_spinBox.value()
        cost_per_unit = Decimal(str(self.ui.cost_doubleSpinBox.value()))
        price_per_unit = Decimal(str(self.ui.price_doubleSpinBox.value()))
        expiry_date = self.ui.expiry_dateEdit.date().toPython()

        if self._found_product:
            category = self._found_product["category"]
            item_name = self._found_product["item_name"]
            minimum_stock = self._found_product["minimum_stock"]
        else:
            category = self.ui.category_comboBox.currentText()
            item_name = self.ui.item_name_lineEdit.text()
            minimum_stock = self.ui.minimum_stock_spinBox.value()

        self.ui.add_item_btn.setEnabled(False)
        self.ui.add_item_btn.setText("Adding...")

        def do_add():
            self.inventory_data.add_item(category, item_name, barcode, batch_number,
                                         quantity, minimum_stock, cost_per_unit,
                                         price_per_unit, expiry_date)

        def on_result(_):
            self.ui.add_item_btn.setEnabled(True)
            QMessageBox.information(self, "Success", f"Item '{item_name}' added successfully.")
            self.clear_fields()
            self.close()

        def on_error(msg):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText(
                "Add Batch" if self._found_product else "Add New Item")
            QMessageBox.warning(self, "Add Item Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_add, on_result=on_result, on_error=on_error)

    def clear_fields(self):
        """Reset the dialog back to lookup mode."""
        self.ui.category_comboBox.setCurrentIndex(0)
        self.ui.item_name_lineEdit.clear()
        self.ui.batch_no_lineEdit.clear()
        self.ui.quantity_spinBox.setValue(0)
        self.ui.minimum_stock_spinBox.setValue(0)
        self.ui.cost_doubleSpinBox.setValue(0.01)
        self.ui.price_doubleSpinBox.setValue(0.01)
        self.ui.expiry_dateEdit.setDate(QDate.currentDate())
        self._set_lookup_mode()


class AddNewUser(QDialog):
    """Dialog to add users with input validation and secure storage."""
    
    def __init__(self, user_data=None):
        """Initialize the Add New User dialog."""
        super().__init__()

        if user_data:
            self.user_data = user_data
        else:
            self.user_data = UserDatabase()

        self.ui = Ui_AddUserPopUp()
        self.ui.setupUi(self)
        self.ui.password_lineEdit_1.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.add_user_btn.clicked.connect(self.handle_add_user)
        self._thread = None

    def handle_add_user(self):
        """Process user creation with credential validation."""
        username = self.ui.username_lineEdit_1.text()
        password = self.ui.password_lineEdit_1.text()
        role = self.ui.role_cb.currentText()

        self.ui.add_user_btn.setEnabled(False)
        self.ui.add_user_btn.setText("Adding...")

        def do_add():
            self.user_data.add_user(username, password, role)

        def on_result(_):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Add User")
            QMessageBox.information(self, "Success", f"User '{username}' added successfully.")
            self.clear_fields()
            self.close()

        def on_error(msg):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Add User")
            QMessageBox.warning(self, "Add User Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_add, on_result=on_result, on_error=on_error)

    def clear_fields(self):
        """Clear the form."""
        self.ui.username_lineEdit_1.clear()
        self.ui.password_lineEdit_1.clear()
        self.ui.role_cb.setCurrentIndex(0)


class UpdateItem(AddNewItem):
    """Dialog window for updating existing inventory items."""
    
    def __init__(self, inventory_data=None):
        """Initialize the update dialog."""
        super().__init__(inventory_data=inventory_data, _skip_two_step=True)

        self.setWindowTitle("Update Item")

        # Hide barcode (not needed in update)
        self.ui.barcode_label.hide()
        self.ui.barcode_lineEdit.hide()

        # Hide product-level fields (category, item name, minimum stock)
        self.ui.label.hide()
        self.ui.category_comboBox.hide()
        self.ui.item_name_label.hide()
        self.ui.item_name_lineEdit.hide()
        self.ui.minimum_stock_label.hide()
        self.ui.minimum_stock_spinBox.hide()

        # Show batch number as editable field
        self.ui.batch_no_label.show()
        self.ui.batch_no_lineEdit.show()

        self.ui.add_item_btn.setText("Update Item")
        # Resize after all fields are hidden so the window fits the content.
        QTimer.singleShot(0, self._resize_to_content)

        # Safe defaults — overwritten by perform_update's on_result
        self._loaded_category = ""
        self._loaded_item_name = ""
        self._loaded_minimum_stock = 0

    def perform_update(self, batch_number):
        """Load existing item data into the form (async)."""
        self.ui.add_item_btn.setEnabled(False)
        self.ui.add_item_btn.setText("Loading...")

        def fetch():
            response = self.inventory_data.supabase.table("inventory").select(
                "*, product(category, item_name, minimum_stock)"
            ).eq("batch_number", batch_number).execute()
            return response.data

        def on_result(data):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText("Update Item")
            if data and len(data) > 0:
                batch = data[0]
                product = batch.get("product")
                # Store product fields as instance variables — more reliable than hidden widgets
                self._loaded_category = product.get("category", "")
                self._loaded_item_name = product.get("item_name", "")
                self._loaded_minimum_stock = int(product.get("minimum_stock", 0))
                # Populate batch number display
                self.ui.batch_no_lineEdit.setText(batch_number)
                # Editable batch fields
                self.ui.quantity_spinBox.setValue(int(batch.get("quantity", 0)))
                self.ui.cost_doubleSpinBox.setValue(batch.get("cost_per_unit", 0) / 100)
                self.ui.price_doubleSpinBox.setValue(batch.get("price_per_unit", 0) / 100)
                expiry_str = batch.get("expiry_date")
                if expiry_str:
                    expiry = datetime.fromisoformat(expiry_str).date()
                    self.ui.expiry_dateEdit.setDate(QDate(expiry.year, expiry.month, expiry.day))

            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    self.ui.add_item_btn.clicked.disconnect()
            except (TypeError, RuntimeError):
                pass
            self.ui.add_item_btn.clicked.connect(lambda: self.handle_update_item(batch_number))

        def on_error(msg):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText("Update Item")
            QMessageBox.warning(self, "Load Error", f"Failed to load item: {msg}")

        self._thread, self._relay = run_worker(fetch, on_result=on_result, on_error=on_error)

    def handle_update_item(self, batch_number):
        """Apply item changes."""
        new_batch_number = self.ui.batch_no_lineEdit.text().strip()
        new_category = self._loaded_category
        new_item_name = self._loaded_item_name
        new_minimum_stock = self._loaded_minimum_stock
        new_quantity = self.ui.quantity_spinBox.value()
        new_cost_per_unit = Decimal(str(self.ui.cost_doubleSpinBox.value()))
        new_price_per_unit = Decimal(str(self.ui.price_doubleSpinBox.value()))
        new_expiry_date = self.ui.expiry_dateEdit.date().toPython()

        confirm = QMessageBox.question(self, "Confirm Update",
                                       f"Update item with batch number '{batch_number}'?")

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.ui.add_item_btn.setEnabled(False)
        self.ui.add_item_btn.setText("Updating...")

        def do_update():
            self.inventory_data.update_item(new_category, new_item_name, batch_number,
                                            new_quantity, new_minimum_stock,
                                            new_cost_per_unit, new_price_per_unit,
                                            new_expiry_date, new_batch_number)

        def on_result(_):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText("Update Item")
            QMessageBox.information(self, "Item Updated",
                    f"Item with batch number '{batch_number}' was updated successfully.")
            self.close()

        def on_error(msg):
            self.ui.add_item_btn.setEnabled(True)
            self.ui.add_item_btn.setText("Update Item")
            QMessageBox.warning(self, "Update Item Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_update, on_result=on_result, on_error=on_error)


class UpdateUser(AddNewUser):
    """Dialog window for updating existing user accounts."""
    
    def __init__(self, user_data=None):
        """Initialize the update user dialog."""
        super().__init__(user_data=user_data)

        self.setWindowTitle("Update User")
        self.ui.username_label.hide()
        self.ui.username_lineEdit_1.hide()
        self.ui.password_label.setText("New Password:")
        self.ui.role_label.setText("New Role:")
        self.ui.add_user_btn.setText("Update User")
        # No manual locking — UpdateUser has fixed fields; the UI file already
        # sets an appropriate fixed size for this dialog.

    def perform_update(self, keyword):
        """Load current user role (async) and pre-fill the form."""
        self.ui.add_user_btn.setEnabled(False)
        self.ui.add_user_btn.setText("Loading...")

        def fetch():
            return self.user_data.get_role(keyword)

        def on_result(role):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Update User")
            if role:
                self.ui.role_cb.setCurrentText(role.capitalize())
            self.ui.password_lineEdit_1.clear()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    self.ui.add_user_btn.clicked.disconnect()
            except (TypeError, RuntimeError):
                pass
            self.ui.add_user_btn.clicked.connect(lambda: self.handle_update_user(keyword))

        def on_error(msg):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Update User")
            QMessageBox.warning(self, "Load Error", f"Failed to load user: {msg}")

        self._thread, self._relay = run_worker(fetch, on_result=on_result, on_error=on_error)

    def handle_update_user(self, username):
        """Apply updates to user."""
        new_password = self.ui.password_lineEdit_1.text()
        new_role = self.ui.role_cb.currentText()

        confirm = QMessageBox.question(self, "Confirm Update", f"Update user '{username}'?")

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.ui.add_user_btn.setEnabled(False)
        self.ui.add_user_btn.setText("Updating...")

        def do_update():
            self.user_data.update_user(username, new_password, new_role)

        def on_result(_):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Update User")
            QMessageBox.information(self, "User Updated",
                                    f"User '{username}' was updated successfully.")
            self.close()

        def on_error(msg):
            self.ui.add_user_btn.setEnabled(True)
            self.ui.add_user_btn.setText("Update User")
            QMessageBox.warning(self, "Update User Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_update, on_result=on_result, on_error=on_error)


class DiscountItem(QDialog):
    """Dialog window for applying a discount to an inventory item."""
    
    def __init__(self, batch_number, inventory_data=None):
        """Initialize the discount dialog."""
        super().__init__()
        self.inventory_data = inventory_data if inventory_data is not None else InventoryData()
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.batch_number = batch_number
        self._thread = None
        self._relay = None
        self.ui.apply_discount_btn.clicked.connect(self.perform_discount)

    def perform_discount(self):
        """Apply percentage discount."""
        discount_amount = self.ui.discount_lineEdit.text()

        if not discount_amount.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Discount must be a whole number")
            return

        discount_amount = int(discount_amount)
        if not (0 <= discount_amount <= 100):
            QMessageBox.warning(self, "Invalid Range", "Discount must be 0-100%")
            return

        confirm = QMessageBox.question(self, "Confirm Discount",
            f"Apply {discount_amount}% discount to selected item?")

        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.ui.apply_discount_btn.setEnabled(False)
        self.ui.apply_discount_btn.setText("Applying...")

        def do_discount():
            self.inventory_data.apply_inventory_discount(
                self.batch_number, discount_amount) #type: ignore

        def on_result(_):
            self.ui.apply_discount_btn.setEnabled(True)
            self.ui.apply_discount_btn.setText("Apply Discount")
            QMessageBox.information(self, "Success", "Discount applied successfully.")
            self.close()

        def on_error(msg):
            self.ui.apply_discount_btn.setEnabled(True)
            self.ui.apply_discount_btn.setText("Apply Discount")
            QMessageBox.warning(self, "Operation Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_discount, on_result=on_result, on_error=on_error)


class SetQuantity(QDialog):
    """Dialog window for setting quantity in checkout cart."""
    
    def __init__(self, checkout_list, barcode, current_row_quantity, 
                 checkout_quantity, stock_quantity, row_index):
        """Initialize the quantity-setting dialog."""
        super().__init__()
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.checkout_list = checkout_list
        self.barcode = barcode
        self.current_row_quantity = current_row_quantity
        self.stock_quantity = stock_quantity
        self.checkout_quantity = checkout_quantity
        self.row_index = row_index

        self.setWindowTitle("Set Quantity")
        self.ui.percentage_label.setText("")
        self.ui.discount_lineEdit.setPlaceholderText("Enter quantity...")
        self.ui.discount_lineEdit.setAlignment(Qt.AlignLeft) #type: ignore
        self.ui.apply_discount_btn.setText("Set Quantity")
        self.setFixedSize(220, 115)
        self.ui.apply_discount_btn.clicked.connect(self.perform_set_quantity)

    def perform_set_quantity(self):
        """Validate and apply new quantity."""
        new_quantity = self.ui.discount_lineEdit.text()
        
        if not new_quantity.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Quantity must be a whole number")
            return

        new_quantity = int(new_quantity)
        if new_quantity <= 0:
            QMessageBox.warning(self, "Invalid Quantity", "Quantity must be positive")
        elif (new_quantity - self.current_row_quantity) + self.checkout_quantity > self.stock_quantity:
            QMessageBox.warning(self, "Stock Limit Reached", 
                                        "Cannot add more of this item. It exceeds available stock.")
        else:
            confirm = QMessageBox.question(self, "Confirm Change", 
                              f"Set quantity to {new_quantity} for this item?")
            
            if confirm == QMessageBox.StandardButton.Yes:
                row = self.checkout_list[self.row_index]
                row["Quantity"] = str(new_quantity)
                net_price = Decimal(row["Net Price"].replace(",", "").strip("$"))
                row["Line Total"] = f"${(Decimal(new_quantity) * net_price).quantize(Decimal('0.01')):,}"
                self.close()


class CheckoutDiscountItem(QDialog):
    """Dialog window for applying discount during checkout."""
    
    def __init__(self, checkout_list, barcode, row_index):
        """Initialize the discount dialog."""
        super().__init__()
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.checkout_list = checkout_list
        self.barcode = barcode
        self.row_index = row_index
        self.ui.apply_discount_btn.clicked.connect(self.perform_discount)

    def perform_discount(self):
        """Apply discount to cart item."""
        discount_amount = self.ui.discount_lineEdit.text()
        
        if not discount_amount.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Discount must be a whole number")
            return

        discount_amount = int(discount_amount)
        if 0 <= discount_amount <= 100:
            confirm = QMessageBox.question(self, "Confirm Discount", 
                f"Apply {discount_amount}% discount to this item?")
            
            if confirm == QMessageBox.StandardButton.Yes:
                row = self.checkout_list[self.row_index]
                price = Decimal(row["Unit Price"].strip("$").replace(",", ""))
                row["Discount"] = f"{discount_amount}%"
                discounted_price = price - (price * Decimal(discount_amount) / Decimal(100))
                row["Net Price"] = f"${discounted_price.quantize(Decimal('0.01')):,}"
                quantity = int(row["Quantity"])
                row["Line Total"] = f"${(discounted_price * Decimal(quantity)).quantize(Decimal('0.01')):,}"
                self.close()
        else:
            QMessageBox.warning(self, "Invalid Range", "Discount must be 0-100%")


class AccountInfo(QDialog):
    """Dialog for account information."""
    
    def __init__(self, username, role):
        """Initialize the account information window."""
        super().__init__()
        self.ui = Ui_AccountInformation()
        self.ui.setupUi(self)
        self.username = username
        self.role = role.capitalize()
        self.log_out = False

        self.ui.username_lbl.setText(self.username)
        self.ui.role_lbl.setText(self.role)
        self.ui.logout_btn.clicked.connect(self.perform_log_out)
        

    def perform_log_out(self):
        """Handle logout confirmation."""
        self.log_out = False
        reply = QMessageBox.question(self, "Confirm Logout", "Log out now?")

        if reply == QMessageBox.StandardButton.Yes:
            self.log_out = True
            self.close()

# -- Products popup -------------------------------------------------------------

_PRODUCT_CATEGORIES = [
    "Bakery", "Beverages", "Canned Goods", "Dairy", "Deli",
    "Frozen", "Grains & Pasta", "Household", "Meat & Seafood",
    "Personal Care", "Produce", "Snacks & Confectionery", "Other"
]

_PRODUCT_DIALOG_STYLE = """
    QDialog { background-color: #F5F7F9; }
    QPushButton {
        background-color: #34495e;
        color: white;
        border: 2px solid #34495e;
        border-radius: 5px;
        font-family: "Segoe UI";
        font-weight: 600;
        font-size: 12pt;
        min-height: 38px;
        min-width: 110px;
    }
    QPushButton:hover { background-color: #2c3e50; border-color: #2c3e50; }
    QPushButton:pressed { background-color: #22313f; border-color: #22313f; }
    QPushButton:disabled { background-color: #7f8c8d; border-color: #7f8c8d; }
    QLineEdit, QSpinBox, QComboBox {
        border: 1px solid #34495e;
        background: #F5F7F9;
        padding: 6px 8px;
        border-radius: 4px;
        font-family: "Segoe UI";
        font-size: 11pt;
        min-height: 32px;
    }
    QLabel { font-family: "Segoe UI"; font-size: 11pt; color: #2c3e50; }
    QTableWidget {
        border: 1px solid #34495e;
        background-color: white;
        gridline-color: #dce1e7;
        font-family: "Segoe UI";
        font-size: 11pt;
    }
    QTableWidget::item:selected { background-color: #34495e; color: white; }
    QHeaderView::section {
        background-color: #34495e;
        color: white;
        font-family: "Segoe UI";
        font-weight: 600;
        font-size: 11pt;
        padding: 6px;
        border: none;
        border-right: 1px solid #2c3e50;
    }
"""

_PRODUCT_COLUMNS = ["Category", "Item Name", "SKU", "Barcode", "Minimum Stock", "Availability"]


def _product_form_row(label_text, widget):
    """Return a label + widget pair in an HBoxLayout."""
    lbl = QLabel(label_text)
    lbl.setMinimumWidth(130)
    row = QHBoxLayout()
    row.addWidget(lbl)
    row.addWidget(widget)
    return row


class AddProduct(QDialog):
    """Dialog to add a new product (no batch) to the product table."""

    def __init__(self, inventory_data, parent=None):
        super().__init__(parent)
        self.inventory_data = inventory_data
        self._thread = None
        self._relay = None
        self.setWindowTitle("Add Product")
        self.setMinimumWidth(420)
        self.setStyleSheet(_PRODUCT_DIALOG_STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 20)

        title = QLabel("Add New Product")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e; margin-bottom: 4px;")
        layout.addWidget(title)

        self.category_cb = QComboBox()
        self.category_cb.addItems(_PRODUCT_CATEGORIES)
        layout.addLayout(_product_form_row("Category:", self.category_cb))

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Whole Milk")
        layout.addLayout(_product_form_row("Item Name:", self.name_edit))

        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("13-digit EAN barcode")
        layout.addLayout(_product_form_row("Barcode:", self.barcode_edit))

        self.min_stock_spin = QSpinBox()
        self.min_stock_spin.setRange(0, 999999)
        self.min_stock_spin.setValue(10)
        layout.addLayout(_product_form_row("Minimum Stock:", self.min_stock_spin))

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #7f8c8d; border-color: #7f8c8d;")
        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn = QPushButton("Add Product")
        self.add_btn.clicked.connect(self._handle_add)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.add_btn)
        layout.addLayout(btn_row)

    def _handle_add(self):
        category = self.category_cb.currentText()
        item_name = self.name_edit.text().strip()
        barcode = self.barcode_edit.text().strip()
        min_stock = self.min_stock_spin.value()

        if not item_name:
            QMessageBox.warning(self, "Missing Field", "Item name is required.")
            return
        if not barcode:
            QMessageBox.warning(self, "Missing Field", "Barcode is required.")
            return

        self.add_btn.setEnabled(False)
        self.add_btn.setText("Adding...")

        def do_add():
            self.inventory_data.add_product(category, item_name, barcode, min_stock)

        def on_result(_):
            self.add_btn.setEnabled(True)
            self.add_btn.setText("Add Product")
            QMessageBox.information(self, "Success",
                                    f"Product '{item_name.title()}' added successfully.")
            self.accept()

        def on_error(msg):
            self.add_btn.setEnabled(True)
            self.add_btn.setText("Add Product")
            QMessageBox.warning(self, "Add Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_add, on_result=on_result, on_error=on_error)


class UpdateProduct(QDialog):
    """Dialog to update an existing product's editable fields."""

    def __init__(self, inventory_data, parent=None):
        super().__init__(parent)
        self.inventory_data = inventory_data
        self._product_row = None
        self._thread = None
        self._relay = None
        self.setWindowTitle("Update Product")
        self.setMinimumWidth(420)
        self.setStyleSheet(_PRODUCT_DIALOG_STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 20)

        title = QLabel("Update Product")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e; margin-bottom: 4px;")
        layout.addWidget(title)

        self.category_cb = QComboBox()
        self.category_cb.addItems(_PRODUCT_CATEGORIES)
        layout.addLayout(_product_form_row("Category:", self.category_cb))

        self.name_edit = QLineEdit()
        layout.addLayout(_product_form_row("Item Name:", self.name_edit))

        self.barcode_lbl = QLabel()
        self.barcode_lbl.setStyleSheet("font-size: 11pt; color: #555;")
        layout.addLayout(_product_form_row("Barcode (fixed):", self.barcode_lbl))

        self.min_stock_spin = QSpinBox()
        self.min_stock_spin.setRange(0, 999999)
        layout.addLayout(_product_form_row("Minimum Stock:", self.min_stock_spin))

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #7f8c8d; border-color: #7f8c8d;")
        self.cancel_btn.clicked.connect(self.reject)
        self.update_btn = QPushButton("Update Product")
        self.update_btn.clicked.connect(self._handle_update)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.update_btn)
        layout.addLayout(btn_row)

    def load_product(self, product_row):
        """Populate the form with an existing product's data."""
        self._product_row = product_row
        idx = self.category_cb.findText(product_row.get("category", ""))
        if idx >= 0:
            self.category_cb.setCurrentIndex(idx)
        self.name_edit.setText(product_row.get("item_name", ""))
        self.barcode_lbl.setText(str(product_row.get("barcode", "")))
        self.min_stock_spin.setValue(int(product_row.get("minimum_stock", 0)))

    def _handle_update(self):
        if not self._product_row:
            return

        category = self.category_cb.currentText()
        item_name = self.name_edit.text().strip()
        min_stock = self.min_stock_spin.value()
        product_id = self._product_row.get("id")

        if not item_name:
            QMessageBox.warning(self, "Missing Field", "Item name is required.")
            return

        self.update_btn.setEnabled(False)
        self.update_btn.setText("Updating...")

        def do_update():
            self.inventory_data.update_product(product_id, category, item_name, min_stock)

        def on_result(_):
            self.update_btn.setEnabled(True)
            self.update_btn.setText("Update Product")
            QMessageBox.information(self, "Success",
                                    f"Product '{item_name.title()}' updated successfully.")
            self.accept()

        def on_error(msg):
            self.update_btn.setEnabled(True)
            self.update_btn.setText("Update Product")
            QMessageBox.warning(self, "Update Failed", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(do_update, on_result=on_result, on_error=on_error)


# -- Return Item popup ----------------------------------------------------------

_RETURN_14_DAYS = 14   # maximum days after sale that a return is allowed


class _ReturnConfirmDialog(QDialog):
    """Styled confirmation dialog for processing a return."""

    def __init__(self, selected, total_refund, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Return")
        self.setMinimumWidth(560)
        self.setStyleSheet(_PRODUCT_DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("The following items will be returned:")
        title.setStyleSheet(
            "font-size: 13pt; font-weight: bold; color: #2c3e50; padding-bottom: 4px;")
        layout.addWidget(title)

        # Items table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Item", "Qty", "Net Price", "Subtotal"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3):
            table.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeMode.ResizeToContents)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setRowCount(len(selected))

        for row_idx, s in enumerate(selected):
            item_total = (Decimal(s["net_price_cents"]) / 100
                          * Decimal(s["return_qty"]))
            vals = [s["item_name"], str(s["return_qty"]),
                    s["net_price_str"], f"${item_total:,.2f}"]
            for col_idx, val in enumerate(vals):
                cell = QTableWidgetItem(val)
                align = (Qt.AlignmentFlag.AlignVCenter |
                         (Qt.AlignmentFlag.AlignLeft if col_idx == 0
                          else Qt.AlignmentFlag.AlignCenter))
                cell.setTextAlignment(align)
                table.setItem(row_idx, col_idx, cell)

        table.resizeRowsToContents()
        table.setMinimumHeight(min(len(selected) * 38 + 44, 280))
        layout.addWidget(table)

        # Separator line
        sep = QLabel()
        sep.setFixedHeight(2)
        sep.setStyleSheet("background-color: #bdc3c7; margin: 2px 0;")
        layout.addWidget(sep)

        # Total refund row
        total_row = QHBoxLayout()
        total_lbl = QLabel("Total Refund:")
        total_lbl.setStyleSheet(
            "font-size: 13pt; font-weight: bold; color: #2c3e50;")
        total_val = QLabel(f"  ${total_refund:,.2f}")
        total_val.setStyleSheet(
            "font-size: 14pt; font-weight: bold; color: #27ae60;")
        total_row.addWidget(total_lbl)
        total_row.addStretch()
        total_row.addWidget(total_val)
        layout.addLayout(total_row)

        layout.addSpacing(6)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "QPushButton { background-color: #7f8c8d; border-color: #7f8c8d; }"
            "QPushButton:hover { background-color: #6c7a7d; border-color: #6c7a7d; }"
            "QPushButton:pressed { background-color: #5a6566; border-color: #5a6566; }")
        confirm_btn = QPushButton("Confirm Return")
        confirm_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; border-color: #27ae60; }"
            "QPushButton:hover { background-color: #219a52; border-color: #219a52; }"
            "QPushButton:pressed { background-color: #1a7a42; border-color: #1a7a42; }")
        btn_row.addWidget(cancel_btn)
        btn_row.addSpacing(8)
        btn_row.addWidget(confirm_btn)
        layout.addLayout(btn_row)

        cancel_btn.clicked.connect(self.reject)
        confirm_btn.clicked.connect(self.accept)


class ReturnItemPopup(QDialog):
    """
    Two-page dialog for processing item returns.

    Page 1 — Order lookup: cashier enters an order ID.
    Page 2 — Item selection: table shows all items in that order;
              the rightmost column has a SpinBox for the return quantity.
    After selecting quantities the cashier clicks "Return Item(s)", which opens
    a confirmation dialog. On confirmation the return is processed in the background
    and a refund-amount dialog is shown on success.
    """

    def __init__(self, sales_data, user_uuid, on_return_complete=None, parent=None):
        """
        Args:
            sales_data:          Authenticated SalesData instance.
            user_uuid (str):     UUID of the logged-in user processing the return.
            on_return_complete:  Optional callable; called (with no args) after a
                                 successful return so the caller can refresh tables.
            parent:              Optional parent widget.
        """
        super().__init__(parent)
        self.sales_data        = sales_data
        self.user_uuid         = user_uuid
        self.on_return_complete = on_return_complete
        self._order_items      = []   # list of item dicts from get_order_items
        self._thread           = None
        self._relay            = None

        _icon = QIcon()
        _icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(_icon)
        self.setMinimumWidth(480)
        self.setStyleSheet(_PRODUCT_DIALOG_STYLE)

        # Build UI from the dedicated UI class
        self.ui = Ui_ReturnItemPopup()
        self.ui.setupUi(self)

        # Convenience aliases so the rest of the methods stay unchanged
        self._stacked        = self.ui.stacked
        self._order_id_edit  = self.ui.order_id_edit
        self._lookup_btn     = self.ui.lookup_btn
        self._page1_status   = self.ui.page1_status
        self._page2_title    = self.ui.page2_title
        self._items_table    = self.ui.items_table
        self._back_btn       = self.ui.back_btn
        self._return_btn     = self.ui.return_btn

        # Wire up signals
        self._order_id_edit.returnPressed.connect(self._lookup_order)
        self._lookup_btn.clicked.connect(self._lookup_order)
        self._back_btn.clicked.connect(self._go_back)
        self._return_btn.clicked.connect(self._do_return)

    # -- page transitions ------------------------------------------------------

    def showEvent(self, event):
        """Always start on page 1 when the dialog is (re)opened."""
        super().showEvent(event)
        self._go_back()

    def _go_back(self):
        self._order_items = []
        self._order_id_edit.clear()
        self._page1_status.setText("")
        self._lookup_btn.setEnabled(True)
        self._lookup_btn.setText("Look Up")
        self.ui.page2.hide()
        self.ui.page1.show()
        self._stacked.setCurrentIndex(0)
        self.setMinimumWidth(480)
        self.setMaximumHeight(16777215)
        self.adjustSize()
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.x() + (screen.width()  - self.width())  // 2,
            screen.y() + (screen.height() - self.height()) // 2,
        )
        self._order_id_edit.setFocus()

    def _show_page2(self, order_id, items):
        self._order_items = items
        self._page2_title.setText(f"Return Items  ·  Order: {order_id}")
        self._populate_items_table(items)
        self.ui.page1.hide()
        self.ui.page2.show()
        self._stacked.setCurrentIndex(1)
        self.setMinimumWidth(820)
        self.setMaximumHeight(16777215)
        self.adjustSize()
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.x() + (screen.width()  - self.width())  // 2,
            screen.y() + (screen.height() - self.height()) // 2,
        )

    # -- data ------------------------------------------------------------------

    def _lookup_order(self):
        order_id = self._order_id_edit.text().strip().upper()
        if not order_id:
            self._page1_status.setStyleSheet(
                "font-size:11pt; font-weight:bold; color: #c0392b;")
            self._page1_status.setText("Please enter an Order ID.")
            return

        self._lookup_btn.setEnabled(False)
        self._lookup_btn.setText("Looking Up…")
        self._page1_status.setText("")

        def fetch():
            return self.sales_data.get_order_items(order_id)

        def on_result(items):
            self._lookup_btn.setEnabled(True)
            self._lookup_btn.setText("Look Up")

            # Check 14-day policy
            from datetime import date, timedelta
            today = date.today()
            sale_date = items[0]["sale_date"] if items else None
            if sale_date is None or (today - sale_date).days > _RETURN_14_DAYS:
                self._page1_status.setStyleSheet(
                    "font-size:11pt; font-weight:bold; color: #c0392b;")
                self._page1_status.setText(
                    f"Return period expired. Returns are only accepted within "
                    f"{_RETURN_14_DAYS} days of purchase.")
                return

            self._show_page2(order_id, items)

        def on_error(msg):
            self._lookup_btn.setEnabled(True)
            self._lookup_btn.setText("Look Up")
            self._page1_status.setStyleSheet(
                "font-size:11pt; font-weight:bold; color: #c0392b;")
            self._page1_status.setText(msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(fetch, on_result=on_result, on_error=on_error)

    # -- table population ------------------------------------------------------

    def _populate_items_table(self, items):
        self._items_table.setRowCount(len(items))
        self._spinboxes = []   # [(row_index, QSpinBox)] — kept in order

        for row_idx, item in enumerate(items):
            for col_idx, value in enumerate([
                item["item_name"],
                str(item["quantity"]),
                item["unit_price_str"],
                f"{item['discount']}%",
                item["line_total_str"],
            ]):
                cell = QTableWidgetItem(value)
                cell.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self._items_table.setItem(row_idx, col_idx, cell)

            # SpinBox for return quantity — max = qty sold, min = 0
            sb = QSpinBox()
            sb.setRange(0, item["quantity"])
            sb.setValue(0)
            sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sb.setStyleSheet(
                "QSpinBox { border: 1px solid #34495e; border-radius: 3px;"
                " padding: 2px 4px; font-size: 11pt; }")
            self._items_table.setCellWidget(row_idx, 5, sb)
            self._spinboxes.append(sb)

    # -- return action ---------------------------------------------------------

    def _do_return(self):
        # Collect items where return qty > 0
        selected = []
        for row_idx, (item, sb) in enumerate(
                zip(self._order_items, self._spinboxes)):
            return_qty = sb.value()
            if return_qty > 0:
                selected.append({
                    "id":               item["id"],
                    "product_id":       item["product_id"],
                    "original_qty":     item["quantity"],
                    "return_qty":       return_qty,
                    "unit_price_cents": item["unit_price_cents"],
                    "discount":         item["discount"],
                    "net_price_cents":  item["net_price_cents"],
                    "item_name":        item["item_name"],
                    "net_price_str":    item["net_price_str"],
                })

        if not selected:
            QMessageBox.warning(self, "No Items Selected",
                                "Please enter a return quantity greater than 0 for "
                                "at least one item.")
            return

        # Compute total refund amount
        total_refund = sum(
            Decimal(s["net_price_cents"]) / 100 * Decimal(s["return_qty"])
            for s in selected
        )

        # Build and show styled confirmation dialog
        dlg = _ReturnConfirmDialog(selected, total_refund, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return   # stay on page 2

        # -- process return in background --------------------------------------
        order_id        = self._order_items[0]["order_id"]
        refund_str      = f"${total_refund:,.2f}"
        self._return_btn.setEnabled(False)
        self._return_btn.setText("Processing…")

        def do_return():
            self.sales_data.process_return(order_id, selected, self.user_uuid)

        def on_result(_):
            self._return_btn.setEnabled(True)
            self._return_btn.setText("Return Item(s)")
            QMessageBox.information(
                self, "Return Processed",
                f"Return successful.\n\nRefund amount to customer:  {refund_str}")
            if self.on_return_complete:
                self.on_return_complete()
            self.close()

        def on_error(msg):
            self._return_btn.setEnabled(True)
            self._return_btn.setText("Return Item(s)")
            QMessageBox.warning(self, "Return Failed",
                                f"Could not process return:\n{msg.strip().splitlines()[-1]}")

        self._thread, self._relay = run_worker(
            do_return, on_result=on_result, on_error=on_error)


class ProductsPopup(QDialog):
    """
    Product catalog dialog. Shows all products with Add and Update actions.
    All DB operations are delegated to InventoryData:
        get_all_products(), add_product(), update_product()
    """

    def __init__(self, inventory_data, parent=None):
        super().__init__(parent)
        self.inventory_data = inventory_data
        self._thread = None
        self._relay = None
        self._products = []          # full list from DB
        self._displayed_products = []  # subset currently shown (after filtering)

        self.setWindowTitle("Products")
        _icon = QIcon()
        _icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(_icon)
        self.setMinimumSize(900, 560)
        self.setStyleSheet(_PRODUCT_DIALOG_STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 16)

        title = QLabel("Product Catalog")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e;")
        layout.addWidget(title)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.add_product_btn = QPushButton("Add Product")
        self.add_product_btn.setMinimumSize(140, 44)
        self.add_product_btn.clicked.connect(self._open_add_dialog)
        btn_row.addWidget(self.add_product_btn)

        self.update_product_btn = QPushButton("Update Product")
        self.update_product_btn.setMinimumSize(160, 44)
        self.update_product_btn.clicked.connect(self._open_update_dialog)
        btn_row.addWidget(self.update_product_btn)

        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumSize(100, 44)
        self.refresh_btn.clicked.connect(self.load_products)
        btn_row.addWidget(self.refresh_btn)

        layout.addLayout(btn_row)

        # Search row
        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by Item Name, SKU, Barcode, or Category…")
        self.search_edit.setMinimumHeight(40)
        self.search_edit.textChanged.connect(self._filter_products)
        search_row.addWidget(self.search_edit)

        self.clear_search_btn = QPushButton("Clear")
        self.clear_search_btn.setMinimumSize(100, 40)
        self.clear_search_btn.clicked.connect(self._clear_search)
        search_row.addWidget(self.clear_search_btn)

        layout.addLayout(search_row)

        self.table = QTableWidget()
        self.table.setColumnCount(len(_PRODUCT_COLUMNS))
        self.table.setHorizontalHeaderLabels(_PRODUCT_COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            self.table.styleSheet() +
            "QTableWidget { alternate-background-color: #eef1f4; }"
        )
        self.table.setFont(QFont("Segoe UI", 11))
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.table)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: #7f8c8d; font-size: 10pt;")
        layout.addWidget(self.status_lbl)

    # -- data ------------------------------------------------------------------

    def load_products(self):
        """Fetch all products from DB and populate the table."""
        self.status_lbl.setText("Loading…")
        self.add_product_btn.setEnabled(False)
        self.update_product_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)

        def fetch():
            return self.inventory_data.get_all_products()

        def on_result(products):
            self._products = products
            self._populate_table(products)
            # Re-apply search filter if user had typed something
            keyword = self.search_edit.text().strip()
            if keyword:
                self._filter_products(keyword)
            else:
                self._displayed_products = list(products)
                self.status_lbl.setText(f"{len(products)} product(s) found.")
            self.add_product_btn.setEnabled(True)
            self.update_product_btn.setEnabled(True)
            self.refresh_btn.setEnabled(True)

        def on_error(msg):
            self.add_product_btn.setEnabled(True)
            self.update_product_btn.setEnabled(True)
            self.refresh_btn.setEnabled(True)
            self.status_lbl.setText("Failed to load products.")
            QMessageBox.warning(self, "Load Error", msg.strip().splitlines()[-1])

        self._thread, self._relay = run_worker(fetch, on_result=on_result, on_error=on_error)

    # -- helpers ---------------------------------------------------------------

    def _populate_table(self, products):
        """Render a list of product dicts into the table."""
        self.table.setRowCount(len(products))
        for row_idx, product in enumerate(products):
            values = [
                product.get("category", ""),
                product.get("item_name", ""),
                product.get("sku", ""),
                str(product.get("barcode", "")),
                str(product.get("minimum_stock", "")),
                (product.get("availability") or "").title(),
            ]
            for col_idx, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col_idx == 5:
                    if val.lower() == "available":
                        item.setForeground(Qt.GlobalColor.darkGreen)
                    elif val.lower() == "low stock":
                        item.setForeground(Qt.GlobalColor.darkYellow)
                    elif val.lower() == "out of stock":
                        item.setForeground(Qt.GlobalColor.red)
                self.table.setItem(row_idx, col_idx, item)

    def _filter_products(self, keyword=None):
        """Filter the table client-side based on the search box content."""
        if keyword is None:
            keyword = self.search_edit.text()
        kw = keyword.strip().lower()

        if not kw:
            self._displayed_products = list(self._products)
            self._populate_table(self._displayed_products)
            self.status_lbl.setText(f"{len(self._products)} product(s) found.")
            return

        filtered = [
            p for p in self._products
            if kw in (p.get("category") or "").lower()
            or kw in (p.get("item_name") or "").lower()
            or kw in (p.get("sku") or "").lower()
            or kw in str(p.get("barcode", "")).lower()
        ]
        self._displayed_products = filtered
        self._populate_table(filtered)
        self.status_lbl.setText(
            f"{len(filtered)} of {len(self._products)} product(s) match \"{keyword.strip()}\"."
        )

    def _clear_search(self):
        """Clear the search box and restore the full product list."""
        self.search_edit.clear()

    # -- actions ---------------------------------------------------------------

    def _open_add_dialog(self):
        dlg = AddProduct(self.inventory_data, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_products()

    def _open_update_dialog(self):
        if not self.table.selectedItems():
            QMessageBox.warning(self, "No Selection", "Please select a product row to update.")
            return
        row_idx = self.table.currentRow()
        if row_idx < 0 or row_idx >= len(self._displayed_products):
            return
        dlg = UpdateProduct(self.inventory_data, parent=self)
        dlg.load_product(self._displayed_products[row_idx])
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_products()