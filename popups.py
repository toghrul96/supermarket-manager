from decimal import Decimal
from PySide6.QtWidgets import QDialog, QLineEdit, QMessageBox
from PySide6.QtCore import QDate, Qt
from ui.ui_add_item_popup import Ui_AddItemPopup
from ui.ui_add_user_popup import Ui_AddUserPopUp
from ui.ui_discount_item_popup import Ui_DialogPopUp
from ui.ui_account_popup import Ui_AccountInformation
from models.inventory import InventoryData
from models.user import UserDatabase
import csv


class AddNewItem(QDialog):
    """Dialog to add inventory items with input validation and secure storage."""
    
    def __init__(self, filename):
        """
        Initialize the Add New Item dialog.

        Args:
            filename (str): Path to the inventory data CSV file.
        """
        super().__init__()
        self.inventory_data = InventoryData(filename)

        # Initialize UI components
        self.ui = Ui_AddItemPopup()
        self.ui.setupUi(self)

        # Connect UI signals
        self.ui.add_item_btn.clicked.connect(self.handle_add_item)

        # Set input constraints to prevents invalid data entry
        self.ui.quantity_spinBox.setRange(0, 999999999)  # Prevent negative quantities
        self.ui.minimum_stock_spinBox.setMaximum(999999999)  # Same max as quantity
        self.ui.cost_doubleSpinBox.setRange(0.01, 999999999.0)  # Minimum $0.01
        self.ui.price_doubleSpinBox.setRange(0.01, 999999999.0)  # Minimum $0.01
        self.ui.expiry_dateEdit.setDate(QDate.currentDate())  # Default to today
        

    def handle_add_item(self):
        """Process form input, validating data and showing errors if any."""
        # Gather all form data
        category = self.ui.category_comboBox.currentText()
        item_name = self.ui.item_name_lineEdit.text()
        barcode = self.ui.barcode_lineEdit.text()
        batch_number = self.ui.batch_no_lineEdit.text()
        quantity = self.ui.quantity_spinBox.value()
        minimum_stock = self.ui.minimum_stock_spinBox.value()
        cost_per_unit = Decimal(str(self.ui.cost_doubleSpinBox.value()))
        price_per_unit = Decimal(str(self.ui.price_doubleSpinBox.value()))
        expiry_date = self.ui.expiry_dateEdit.date().toPython()

        try:
            # Pass data to inventory handler to validate to save it securely
            self.inventory_data.add_item(category, item_name, barcode, batch_number, 
                                      quantity, minimum_stock, cost_per_unit, 
                                      price_per_unit, expiry_date)
        except ValueError as e:
            # Show specific validation errors to user
            QMessageBox.warning(self, "Add New Item Failed", str(e))
        else:
            # Success feedback and cleanup
            QMessageBox.information(self, "Success", f"Item '{item_name}' added successfully.")
            self.clear_fields()
            self.close()  # Auto-close pop-up on success

    def clear_fields(self):
        """Clear the form and set it back to default for reuse."""
        self.ui.category_comboBox.setCurrentIndex(0)  # First category
        self.ui.item_name_lineEdit.clear()
        self.ui.barcode_lineEdit.clear()
        self.ui.batch_no_lineEdit.clear()
        self.ui.quantity_spinBox.setValue(0)  # Default quantity
        self.ui.minimum_stock_spinBox.setValue(0)  # Default min stock
        self.ui.cost_doubleSpinBox.setValue(0.01)  # Minimum cost
        self.ui.price_doubleSpinBox.setValue(0.01)  # Minimum price
        self.ui.expiry_dateEdit.setDate(QDate.currentDate())  # Today's date


class AddNewUser(QDialog):
    """Dialog to add users with input validation and secure storage."""
    
    def __init__(self, filename):
        """
        Initialize the Add New User dialog.

        Args:
            filename (str): Path to the user data CSV file.
        """
        super().__init__()
        self.user_data = UserDatabase(filename)

        # Initialize UI components
        self.ui = Ui_AddUserPopUp()
        self.ui.setupUi(self)

        # Mask password input
        self.ui.password_lineEdit_1.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect signals
        self.ui.add_user_btn.clicked.connect(self.handle_add_user)

    def handle_add_user(self):
        """Process user creation with credential validation."""
        username = self.ui.username_lineEdit_1.text()
        password = self.ui.password_lineEdit_1.text()
        role = self.ui.role_cb.currentText()  # Predefined roles in comboBox

        try:
            # Pass data to user handler to validate to save it securely
            self.user_data.add_user(username, password, role)
        except ValueError as e:
            # Show specific validation errors to user
            QMessageBox.warning(self, "Add User Failed", str(e))
        else:
            # Success feedback and cleanup
            QMessageBox.information(self, "Success", f"User '{username}' added successfully.")
            self.clear_fields()
            self.close()

    def clear_fields(self):
        """Clear the form and set it back to default for reuse."""
        self.ui.username_lineEdit_1.clear()
        self.ui.password_lineEdit_1.clear()
        self.ui.role_cb.setCurrentIndex(0)  # Reset to default role


class UpdateItem(AddNewItem):
    """
    Dialog window for updating existing inventory items.

    Inherits from AddNewItem but disables editing of immutable fields
    such as barcode and batch number, and adjusts the interface to reflect
    an update operation instead of item creation.
    """
    
    def __init__(self, filename):
        """
        Initialize the update dialog with modified UI and behavior.

        Args:
            filename (str): Path to the inventory CSV file.
        """
        super().__init__(filename)
        self.filename = filename
        self.inventory_data = InventoryData(filename)

        # Modify UI for update context
        self.setWindowTitle("Update Item")
        self.ui.barcode_label.hide()  # Immutable field
        self.ui.barcode_lineEdit.hide()
        self.ui.batch_no_label.hide()  # Immutable field
        self.ui.batch_no_lineEdit.hide()
        self.ui.add_item_btn.setText("Update Item")

        # Fixed size for better UI
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.minimumSizeHint())

    def perform_update(self, keyword):
        """
        Load existing item data by batch number and pre-fill the update form.

        Args:
            keyword (str): The batch number used to locate the item.
        """
        # Load current item data
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Batch Number") == keyword:
                    # Populate form fields
                    self.ui.category_comboBox.setCurrentText(row.get("Category")) # type: ignore
                    self.ui.item_name_lineEdit.setText(row.get("Item Name"))
                    self.ui.quantity_spinBox.setValue(int(row.get("Quantity"))) # type: ignore
                    self.ui.minimum_stock_spinBox.setValue(int(row.get("Minimum Stock"))) # type: ignore
                    self.ui.cost_doubleSpinBox.setValue(Decimal(row.get("Cost per Unit").strip("$").replace(",",""))) # type: ignore
                    self.ui.price_doubleSpinBox.setValue(Decimal(row.get("Price per Unit").strip("$").replace(",",""))) # type: ignore
                    self.ui.expiry_dateEdit.setDate(QDate.fromString(row.get("Expiry Date"), "dd/MM/yyyy")) # type: ignore
    
        # Reconfigure button for update action
        try:
            self.ui.add_item_btn.clicked.disconnect()  # Clear inherited handler
        except TypeError:
            pass
        self.ui.add_item_btn.clicked.connect(lambda: self.handle_update_item(keyword))
        

    def handle_update_item(self, batch_number):
        """
        Apply item changes and update the inventory file.

        Args:
            batch_number (str): Identifier for the item being updated.
        """
        # Gather updated values
        new_category = self.ui.category_comboBox.currentText()
        new_item_name = self.ui.item_name_lineEdit.text()
        new_quantity = self.ui.quantity_spinBox.value()
        new_minimum_stock = self.ui.minimum_stock_spinBox.value()
        new_cost_per_unit = Decimal(str(self.ui.cost_doubleSpinBox.value()))
        new_price_per_unit = Decimal(str(self.ui.price_doubleSpinBox.value()))
        new_expiry_date = self.ui.expiry_dateEdit.date().toPython()

        # Confirm destructive action
        confirm = QMessageBox.question(self, "Confirm Update", 
                                    f"Update item with batch number '{batch_number}'?")
            
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Delegate to inventory handler
                self.inventory_data.update_item(new_category, new_item_name, batch_number, 
                                             new_quantity, new_minimum_stock, 
                                             new_cost_per_unit, new_price_per_unit, 
                                             new_expiry_date)
            except ValueError as e:
                QMessageBox.warning(self, "Update Item Failed", str(e))
            else:
                # Success feedback
                QMessageBox.information(self, "Item Updated", 
                        f"Item with batch number '{batch_number}' was updated successfully.")
                self.close()


class UpdateUser(AddNewUser):
    """
    Dialog window for updating existing user accounts.

    Inherits from AddNewUser but disables editing of username field, 
    and adjusts the interface to reflect an update operation instead of new user creation.
    """
    
    def __init__(self, filename):
        """
        Initialize the update user dialog with inherited UI and adjustments.

        Args:
            filename (str): Path to the user data storage file.
        """
        super().__init__(filename)
        self.user_data = UserDatabase(filename)
        self.filename = filename

        # Modify UI for update context
        self.setWindowTitle("Update User")
        self.ui.username_label.hide()  # Immutable field
        self.ui.username_lineEdit_1.hide()
        self.ui.password_label.setText("New Password:")  # Clarify action
        self.ui.role_label.setText("New Role:")  # Clarify action
        self.ui.add_user_btn.setText("Update User")  # Action-specific label

        # Fixed size for consistency
        self.setMinimumSize(self.minimumSizeHint())
        self.setMaximumSize(self.minimumSizeHint())

    def perform_update(self, keyword):
        """
        Load existing user data and prepare the form for editing.

        Args:
            keyword (str): The username of the user to be updated.
        """
        # Load current user data
        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("Username") == keyword:
                    self.ui.role_cb.setCurrentText(row.get("Role")) # type: ignore                   
        self.ui.password_lineEdit_1.clear()  # Never show existing password
        
        # Reconfigure button for update action
        try:
            self.ui.add_user_btn.clicked.disconnect()  # Clear inherited handler
        except TypeError:
            pass
        self.ui.add_user_btn.clicked.connect(lambda: self.handle_update_user(keyword))

    def handle_update_user(self, username):
        """
        Apply updates to an existing user and handle validation and feedback.

        Args:
            username (str): The username of the user whose account is being updated.
        """
        new_password = self.ui.password_lineEdit_1.text()
        new_role = self.ui.role_cb.currentText()

        confirm = QMessageBox.question(self, "Confirm Update", 
                                           f"Update user '{username}'?")
            
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Delegate to user handler
                self.user_data.update_user(username, new_password, new_role)
            except ValueError as e:
                QMessageBox.warning(self, "Update User Failed", str(e))
            else:
                # Success feedback
                QMessageBox.information(self, "User Updated", 
                                            f"User '{username}' was updated successfully.")
                self.close()


class DiscountItem(QDialog):
    """
    Dialog window for applying a discount to an existing inventory item.

    Allows users to enter a discount percentage, validates the input,
    and applies the discount to the item identified by its barcode and batch number.
    """
    
    def __init__(self, filename, barcode, batch_number):
        """
        Initialize the discount dialog and prepare it for use.

        Args:
            filename (str): Path to the CSV file containing inventory data.
            barcode (str): The barcode of the item to apply a discount to.
            batch_number (str): The batch number of the item to apply a discount to.
        """
        super().__init__()
        self.inventory_data = InventoryData(filename)
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.barcode = barcode
        self.batch_number = batch_number
        self.ui.apply_discount_btn.clicked.connect(self.perform_discount)

    def perform_discount(self):
        """Apply percentage discount with range validation."""
        discount_amount = self.ui.discount_lineEdit.text()
        
        # Validate input format
        if not discount_amount.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Discount must be a whole number")
            return

        discount_amount = int(discount_amount)
        if 0 <= discount_amount <= 100:
            confirm = QMessageBox.question(self, "Confirm Discount", 
                f"Apply {discount_amount}% discount to selected item?")
            
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    # Delegate to inventory handler
                    self.inventory_data.apply_inventory_discount(self.barcode, 
                                                               self.batch_number, 
                                                               discount_amount)
                except ValueError as e:
                    QMessageBox.warning(self, "Operation Failed", str(e))
                else:
                    QMessageBox.information(self, "Success", "Discount applied successfully.")
                    self.close()
        else:
            QMessageBox.warning(self, "Invalid Range", "Discount must be 0-100%")


class SetQuantity(QDialog):
    """Dialog window for setting the quantity of an item in the checkout cart."""
    
    def __init__(self, checkout_list, barcode, current_row_quantity, 
                 checkout_quantity, stock_quantity, row_index):
        """
        Initialize the quantity-setting dialog with references to cart and stock data.

        Args:
            checkout_list (list): The current list of items in the checkout cart.
            barcode (str): The barcode of the item to update.
            current_row_quantity (int): The total quantity of the item in the selected row.
            checkout_quantity (int): The total quantity of the item in the checkout list.
            stock_quantity (int): The available quantity of the item in stock.
            row_index (int): The index of the selected item in the checkout list.
        """
        super().__init__()
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.checkout_list = checkout_list  # Live cart reference
        self.barcode = barcode
        self.current_row_quantity = current_row_quantity # Current row count
        self.stock_quantity = stock_quantity  # Current inventory count
        self.checkout_quantity = checkout_quantity # Current checkout count
        self.row_index = row_index

        # Customize UI for quantity setting
        self.setWindowTitle("Set Quantity")
        self.ui.percentage_label.setText("")
        self.ui.discount_lineEdit.setPlaceholderText("Enter quantity...")
        self.ui.discount_lineEdit.setAlignment(Qt.AlignLeft) # type: ignore
        self.ui.apply_discount_btn.setText("Set Quantity")
        self.setFixedSize(220, 115)  # Optimal size for this dialog

        self.ui.apply_discount_btn.clicked.connect(self.perform_set_quantity)

    def perform_set_quantity(self):
        """Validate and apply new quantity to cart item."""
        new_quantity = self.ui.discount_lineEdit.text()
        
        if not new_quantity.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Quantity must be a whole number")
            return

        new_quantity = int(new_quantity)
        if new_quantity <= 0:
            QMessageBox.warning(self, "Invalid Quantity", "Quantity must be positive")
        elif (new_quantity - self.current_row_quantity) + self.checkout_quantity > self.stock_quantity:
            # Ensure total checkout quantity stays within actual stock limits to avoid overselling
            QMessageBox.warning(self, "Stock Limit Reached", 
                                        "Cannot add more of this item. It exceeds available stock.")
        else:
            confirm = QMessageBox.question(self, "Confirm Change", 
                              f"Set quantity to {new_quantity} for this item?")
            
            if confirm == QMessageBox.StandardButton.Yes:
                # Direct cart modification
                row = self.checkout_list[self.row_index]
                row["Quantity"] = str(new_quantity)
                net_price = Decimal(row["Net Price"].replace(",", "").strip("$"))
                row["Line Total"] = f"${(Decimal(new_quantity) * net_price).quantize(Decimal('0.01')):,}"
                self.close()


class CheckoutDiscountItem(QDialog):
    """Dialog window for applying a discount to an item during checkout."""
    
    def __init__(self, checkout_list, barcode, row_index):
        """
        Initialize the discount dialog with cart data and item identifiers.

        Args:
            checkout_list (list): The current list of items in the checkout cart.
            barcode (str): The barcode of the item to apply the discount to.
            row_index (int): The index of the selected item in the checkout list.
        """
        super().__init__()
        self.ui = Ui_DialogPopUp()
        self.ui.setupUi(self)
        self.checkout_list = checkout_list  # Reference to live cart data
        self.barcode = barcode
        self.row_index = row_index
        self.ui.apply_discount_btn.clicked.connect(self.perform_discount)

    def perform_discount(self):
        """Apply discount to cart item with immediate feedback."""
        discount_amount = self.ui.discount_lineEdit.text()
        
        if not discount_amount.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Discount must be a whole number")
            return

        discount_amount = int(discount_amount)
        if 0 <= discount_amount <= 100:
            confirm = QMessageBox.question(self, "Confirm Discount", 
                f"Apply {discount_amount}% discount to this item?")
            
            if confirm == QMessageBox.StandardButton.Yes:
                # Direct cart modification
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
    """Dialog window for displaying the current user's account information with logout control."""
    
    def __init__(self, username, role):
        """
        Initialize the account information window with user details.

        Args:
            username (str): The username of the current user.
            role (str): The role associated with the user.
        """
        super().__init__()
        self.ui = Ui_AccountInformation()
        self.ui.setupUi(self)
        self.username = username
        self.role = role
        self.log_out = False  # Tracks if user chose to log out

        # Display user info
        self.ui.username_lbl.setText(self.username)
        self.ui.role_lbl.setText(self.role)
        self.ui.logout_btn.clicked.connect(self.perform_log_out)
        

    def perform_log_out(self):
        """Handle logout confirmation with state management."""
        self.log_out = False  # Reset logout status each time
        reply = QMessageBox.question(self, "Confirm Logout", "Log out now?")

        if reply == QMessageBox.StandardButton.Yes:
            self.log_out = True  # Mark that logout was confirmed
            self.close()