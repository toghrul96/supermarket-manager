from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QTableWidgetItem, QAbstractItemView, QHeaderView)
from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, Qt, QDate
from PySide6.QtGui import QFont
from ui.ui_main import Ui_MainWindow
from models.user import UserDatabase
from models.sales import SalesData
from models.inventory import InventoryData
from popups import (AddNewUser, UpdateUser, AddNewItem, UpdateItem, DiscountItem, 
                    CheckoutDiscountItem, SetQuantity, AccountInfo)
import csv
from decimal import Decimal, InvalidOperation

USER_DATA = "data/user_data.csv"
INVENTORY_DATA = "data/inventory_data.csv"
SALES_DATA = "data/sales_data.csv"


class MainWindow(QMainWindow):
    """
    Main application window for the supermarket management system.

    This class handles initialization of the user interface, connecting UI elements
    to their logic, and loading user, inventory, and sales data. It manages navigation,
    popups, checkout processing, filtering, and reports.
    """
    def __init__(self, username):
        """
        Initialize the main window with UI setup, data connections, and signal bindings.

        Args:
            username (str): Username of the logged-in user.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize user identity and apply role-based access controls
        self.user_data = UserDatabase(USER_DATA)
        self.username = username
        self.role = self.user_data.get_role(self.username)
        self.set_user_access(self.role)

        # Initialize data handlers
        self.inventory_data = InventoryData(INVENTORY_DATA)
        self.sales_data = SalesData(SALES_DATA)

        # Initialize popup windows for user, item, and account operations
        self.add_user_popup = AddNewUser(USER_DATA)
        self.update_user_popup = UpdateUser(USER_DATA)
        self.add_item_popup = AddNewItem(INVENTORY_DATA)
        self.update_item_popup = UpdateItem(INVENTORY_DATA)
        self.account_popup = AccountInfo(self.username, self.role)

        # Checkout-related variables
        self.checkout_list = []         # List of items added to checkout
        self.payment_method = None      # Selected payment method at checkout

        # Sidebar toggle state (collapsed by default)
        self.sidebar_expanded = False

        # Default to checkout page and focus on barcode input
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.checkout_btn.setChecked(True)
        self.ui.barcode_lineEdit.setFocus()
        self.ui.barcode_lineEdit.returnPressed.connect(self.checkout_add_item)

        # Navigation buttons
        self.ui.menu_btn.clicked.connect(self.toggle_sidebar)
        self.ui.checkout_btn.clicked.connect(self.switch_to_checkout_page)
        self.ui.inventory_btn.clicked.connect(self.switch_to_inventory_page)
        self.ui.reports_btn.clicked.connect(self.switch_to_reports_page)
        self.ui.users_btn.clicked.connect(self.switch_to_users_page)
        self.ui.exit_btn.clicked.connect(self.confirm_exit)

        # User management buttons
        self.ui.add_user_btn.clicked.connect(
            lambda: self.add_popup_ui(self.add_user_popup, self.ui.user_table, USER_DATA))
        self.ui.delete_user_btn.clicked.connect(
            lambda: self.delete_ui(self.user_data, self.ui.user_table, USER_DATA))
        self.ui.update_user_btn.clicked.connect(
            lambda: self.update_ui(self.update_user_popup, self.ui.user_table, USER_DATA))
        self.ui.username_search_lineEdit.textChanged.connect(
            lambda: self.search_ui(self.user_data, self.ui.user_table, USER_DATA, self.ui.username_search_lineEdit))
        self.ui.clear_user_tb_btn.clicked.connect(
            lambda: self.clear_search_ui(self.ui.user_table, USER_DATA, self.ui.username_search_lineEdit))

        # Inventory management buttons
        self.ui.add_item_btn.clicked.connect(
            lambda: self.add_popup_ui(self.add_item_popup, self.ui.inventory_table, INVENTORY_DATA))
        self.ui.delete_item_btn.clicked.connect(
            lambda: self.delete_ui(self.inventory_data, self.ui.inventory_table, INVENTORY_DATA))
        self.ui.update_item_btn.clicked.connect(
            lambda: self.update_ui(self.update_item_popup, self.ui.inventory_table, INVENTORY_DATA))
        self.ui.item_search_lineEdit.textChanged.connect(
            lambda: self.search_ui(self.inventory_data, self.ui.inventory_table, INVENTORY_DATA, self.ui.item_search_lineEdit))
        self.ui.clear_inventory_tb_btn.clicked.connect(
            lambda: self.clear_search_ui(self.ui.inventory_table, INVENTORY_DATA, self.ui.item_search_lineEdit))

        # Inventory filtering by stock status
        self.ui.low_stock_btn.clicked.connect(lambda: self.list_by_status("Low Stock"))
        self.ui.out_of_stock_btn.clicked.connect(lambda: self.list_by_status("Out of Stock"))
        self.ui.expired_btn.clicked.connect(lambda: self.list_by_status("Expired"))

        # Checkout buttons and shortcuts
        self.ui.checkout_add_item.clicked.connect(self.checkout_add_item)
        self.ui.checkout_add_item.setShortcut("F1")
        self.ui.cancel_sale_btn.clicked.connect(self.checkout_cancel_sale)
        self.ui.cancel_sale_btn.setShortcut("Esc")
        self.ui.increase_item_btn.clicked.connect(lambda: self.checkout_update_item_quantity("+"))
        self.ui.decrease_item_btn.clicked.connect(lambda: self.checkout_update_item_quantity("-"))
        self.ui.remove_item_btn.clicked.connect(self.checkout_delete_item)
        self.ui.cash_received_lineEdit.textChanged.connect(self.checkout_compute_change)
        self.ui.cash_btn.clicked.connect(lambda: self.checkout_payment_selection("Cash"))
        self.ui.cash_btn.setShortcut("F2")
        self.ui.card_btn.clicked.connect(lambda: self.checkout_payment_selection("Card"))
        self.ui.card_btn.setShortcut("F3")
        self.ui.checkout_btn_2.clicked.connect(self.perform_checkout)
        self.ui.discount_item_btn.clicked.connect(self.discount_item_popup)
        self.ui.apply_discount_btn.clicked.connect(self.checkout_discount_item_popup)
        self.ui.set_quantity_btn.clicked.connect(self.checkout_set_quantity_popup)
        self.ui.add_free_unit_btn.clicked.connect(self.checkout_add_free_unit)

        # Reports filtering
        self.ui.sales_search_lineEdit.textChanged.connect(
            lambda: self.search_ui(self.sales_data, self.ui.sales_history_table, SALES_DATA, self.ui.sales_search_lineEdit))
        self.ui.clear_sales_tbl.clicked.connect(
            lambda: self.clear_search_ui(self.ui.sales_history_table, SALES_DATA, self.ui.sales_search_lineEdit))
        self.ui.sales_history_reset_btn.clicked.connect(self.reset_sales_history_table)
        self.ui.from_date.dateChanged.connect(self.filter_sales_history_table)
        self.ui.to_date.dateChanged.connect(self.filter_sales_history_table)
        self.ui.filter_summary_comboBox.currentTextChanged.connect(self.filter_sales_summary_table)
        self.ui.filter_products_comboBox.currentTextChanged.connect(self.filter_top_products_table)
        self.ui.filter_employees_comboBox.currentTextChanged.connect(self.filter_top_employees_table)

        # Account information popup
        self.ui.account_btn.clicked.connect(self.account_popup_ui)

        # Table setup and data loading
        self.set_table(self.ui.user_table)
        self.load_csv_to_table(self.ui.user_table, USER_DATA)
        self.set_table(self.ui.inventory_table)
        self.load_csv_to_table(self.ui.inventory_table, INVENTORY_DATA)
        self.set_table(self.ui.sales_history_table)
        self.load_csv_to_table(self.ui.sales_history_table, SALES_DATA)
        self.set_table(self.ui.sales_summary_table)
        self.filter_sales_summary_table()
        self.set_table(self.ui.top_products_table)
        self.filter_top_products_table()
        self.set_table(self.ui.top_employees_table)
        self.filter_top_employees_table()

        # Set font size for better readability in tables
        font = QFont()
        font.setPointSize(12)
        self.ui.user_table.verticalHeader().setFont(font)
        self.ui.user_table.setColumnHidden(1, True)  # Hide password
        self.ui.inventory_table.verticalHeader().setFont(font)
        self.ui.sales_history_table.verticalHeader().setFont(font)
        self.ui.sales_summary_table.verticalHeader().setFont(font)
        self.ui.top_products_table.verticalHeader().setFont(font)
        self.ui.top_employees_table.verticalHeader().setFont(font)

        # Checkout table with larger font and hidden internal columns
        self.set_table(self.ui.checkout_table)
        font2 = QFont()
        font2.setPointSize(18)
        self.ui.checkout_table.verticalHeader().setFont(font2)
        self.ui.checkout_table.setColumnHidden(0, True)  # Hide barcode

        # Default "To Date" for reports = Today
        self.ui.to_date.setDate(QDate.currentDate())

        # Update dashboard info and item statuses
        self.set_header_info_texts()
        self.inventory_data.update_item_statuses()


    def switch_to_checkout_page(self):
        """Switch the stacked widget to show the checkout page."""
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.barcode_lineEdit.setFocus()  # Immediate focus for scanning barcode
    
    def switch_to_inventory_page(self):
        """Switch the stacked widget to show the inventory page."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_to_reports_page(self):
        """Switch the stacked widget to show the reports page."""
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.reports_tab.setCurrentIndex(0)  # Default to first tab

    def switch_to_users_page(self):
        """Switch the stacked widget to show the users page."""
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_account_btn_clicked(self):
        """Switch the stacked widget to show the account page."""
        self.ui.stackedWidget.setCurrentIndex(4)

    def confirm_exit(self):
        """Show confirmation dialog before exiting the application."""
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?")

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def toggle_sidebar(self):
        """Toggle the sidebar between expanded and collapsed states with animation."""
        # Animate width for smooth transition
        start_width = self.ui.sidebar.width()
        end_width = 170 if not self.sidebar_expanded else 90  # Expanded vs collapsed widths

        # Create animation group for parallel animations
        self.anim_group = QParallelAnimationGroup(self)
        
        # Animate minimumWidth property
        anim_min = QPropertyAnimation(self.ui.sidebar, b"minimumWidth")
        anim_min.setDuration(500)  # Half-second animation
        anim_min.setStartValue(start_width)
        anim_min.setEndValue(end_width)
        anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart)  # Smooth easing curve
        
        # Animate maximumWidth property
        anim_max = QPropertyAnimation(self.ui.sidebar, b"maximumWidth")
        anim_max.setDuration(500)
        anim_max.setStartValue(start_width)
        anim_max.setEndValue(end_width)
        anim_max.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
        # Add both animations to the group for synchronized execution
        self.anim_group.addAnimation(anim_min)
        self.anim_group.addAnimation(anim_max)

        # Toggle the sidebar state
        self.sidebar_expanded = not self.sidebar_expanded

        # Update widgets based on current sidebar state
        if self.sidebar_expanded:
            # Expanded state - show full text and larger logo
            self.ui.logo.setText("Supermarket\nManager")
            self.ui.logo.setMinimumWidth(170)
            self.ui.logo.setStyleSheet("""font-size: 20px;""")
            self.ui.checkout_btn.setText(" Checkout")
            self.ui.inventory_btn.setText(" Inventory")
            self.ui.reports_btn.setText(" Reports")
            self.ui.users_btn.setText(" Users")
            self.ui.exit_btn.setText(" Exit")
            for btn in (self.ui.checkout_btn, self.ui.inventory_btn, self.ui.reports_btn,
            self.ui.users_btn, self.ui.exit_btn):
                btn.setStyleSheet("""text-align: left; padding-left: 10px; qproperty-iconSize: 33px 33px""")
        else:
            # Collapsed state - show only icons
            self.ui.logo.setText("S.M.")
            self.ui.logo.setMinimumWidth(60)
            self.ui.logo.setStyleSheet(""" font-size: 27px; """)
            for btn in (self.ui.checkout_btn, self.ui.inventory_btn, self.ui.reports_btn, 
            self.ui.users_btn, self.ui.exit_btn):
                btn.setText("")
                btn.setStyleSheet("""qproperty-iconSize: 33px 33px""")

        self.anim_group.start()

    def checkout_add_item(self):
        """Add an item to the checkout list based on barcode input."""
        barcode = self.ui.barcode_lineEdit.text()
        try:
            # Attempt to find item in inventory
            item = self.inventory_data.checkout_find(barcode)
        except ValueError as e:
            # Show error if item not found
            QMessageBox.warning(self, "Add Item Failed", str(e))
            self.ui.barcode_lineEdit.clear()
            self.ui.barcode_lineEdit.setFocus()
        else: 
            # Check if item already exists in checkout
            repeated_item = False
            quantity = 1
            for index, row in enumerate(self.checkout_list):
                if barcode == row["Barcode"]:
                    repeated_item = True
                    # Increment quantity if item exists
                    quantity = int(row["Quantity"]) + 1
                    line_total = quantity * Decimal(item.get("Net Price").strip("$").replace(",", ""))
                    # Update existing item
                    self.checkout_list[index] = {"Username": self.username,
                                                "SKU": item.get("SKU"),
                                                "Barcode": item.get("Barcode"),
                                                "Item Name": item.get("Item Name"),
                                                "Quantity": str(quantity),
                                                "Unit Price": item.get("Price per Unit"),
                                                "Discount": item.get("Discount"),
                                                "Net Price": item.get("Net Price"),
                                                "Line Total": f"${line_total.quantize(Decimal('0.01')):,}"}
                    break
            if not repeated_item:
                # Add new item to checkout
                self.checkout_list.append({ "Username": self.username, 
                                            "SKU": item.get("SKU"),
                                            "Barcode": item.get("Barcode"),
                                            "Item Name": item.get("Item Name"),
                                            "Quantity": "1",
                                            "Unit Price": item.get("Price per Unit"),
                                            "Discount": item.get("Discount"),
                                            "Net Price": item.get("Net Price"),
                                            "Line Total": item.get("Net Price")})
            # Refresh checkout display
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.clear()
            self.ui.barcode_lineEdit.setFocus()
            self.inventory_data.update_item_statuses()

    def checkout_cancel_sale(self):
        """Cancel the current sale and clear the checkout list."""
        confirm = QMessageBox.question(self, "Cancel Sale", "Are you sure you want to cancel this sale?")

        if confirm == QMessageBox.StandardButton.Yes:
            # Empty the checkout list
            self.checkout_list = []
            self.checkout_payment_selection("Reset")
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
    
    def checkout_update_item_quantity(self, operation):
        """
        Update the quantity of an item in the checkout list.
        
        Args:
            operation (str): Either "+" to increase or "-" to decrease quantity
        """
        table_row_index = self.ui.checkout_table.currentRow()

        if table_row_index != -1:
            barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
            quantity = int(self.ui.checkout_table.item(table_row_index, 2).text())  # type: ignore
            
            # Adjust quantity based on operation
            if operation == "+":
                checkout_quantity = self.checkout_count_item_quantity(barcode)
                stock_quantity = self.inventory_data.count_item_quantity(barcode)

                # Check if adding one more unit would exceed available stock
                if (checkout_quantity + 1) > stock_quantity:
                    QMessageBox.warning(self, "Stock Limit Reached", 
                                        "Cannot add more of this item. It exceeds available stock.")
                    return
                else:
                    # When it is safe, increase quantity by one
                    quantity += 1
            elif operation == "-":
                if quantity > 1:
                    quantity -= 1
                else:
                    quantity = 1  # Prevent zero or negative quantities

            # Update the checkout list
            row = self.checkout_list[table_row_index]
            row["Quantity"] = str(quantity)
            net_price = Decimal(row["Net Price"].replace(",", "").strip("$"))
            # Calculate line total
            row["Line Total"] = f"${(net_price * Decimal(quantity)).quantize(Decimal('0.01')):,}"
            self.load_checkout_table()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
        else:
            QMessageBox.warning(self, "No Selection", "Select an item before changing its quantity.")
            self.ui.barcode_lineEdit.setFocus()
    
    def checkout_delete_item(self):
        """Remove an item from the checkout list."""
        table_row_index = self.ui.checkout_table.currentRow()

        if table_row_index != -1:
            confirm = QMessageBox.question(self, "Delete Item", "Are you sure you want to delete selected item?")

            if confirm == QMessageBox.StandardButton.Yes:
                # Remove item from checkout list
                del self.checkout_list[table_row_index]
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
        else:
            QMessageBox.warning(self, "No Selection", "Select an item before deleting.")
            self.ui.barcode_lineEdit.setFocus()

    def checkout_set_quantity_popup(self):
        """Show popup to manually set item quantity in checkout."""
        table_row_index = self.ui.checkout_table.currentRow()

        if table_row_index != -1:
            barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
            current_row_quantity = int(self.ui.checkout_table.item(table_row_index, 2).text()) # type: ignore
            checkout_quantity = self.checkout_count_item_quantity(barcode)
            stock_quantity = self.inventory_data.count_item_quantity(barcode)
            popup = SetQuantity(self.checkout_list, barcode, 
                                current_row_quantity, checkout_quantity, stock_quantity, table_row_index)
            popup.exec()
            # Refresh checkout display
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before setting quantity.")
    
    def checkout_discount_item_popup(self):
        """
        Show popup to apply a discount to an item in the current checkout. 
        This does not affect the item's price in the inventory.
        """
        table_row_index = self.ui.checkout_table.currentRow()

        if table_row_index != -1:
            barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
            popup = CheckoutDiscountItem(self.checkout_list, barcode, table_row_index)
            popup.exec()
            # Refresh checkout display
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before applying discount.")

    def checkout_add_free_unit(self):
        """Add one unstacked promotional (free) unit of the selected item in the checkout table."""
        table_row_index = self.ui.checkout_table.currentRow()

        if table_row_index != -1:
            item_name = self.ui.checkout_table.item(table_row_index, 1).text() # type: ignore
            confirm = QMessageBox.question(self,"Add Free Unit",
                f"Add a free promotional unit of '{item_name}' to the checkout?")

            if confirm == QMessageBox.StandardButton.Yes:
                barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
                # Prevent exceeding available stock
                checkout_quantity = self.checkout_count_item_quantity(barcode)
                stock_quantity = self.inventory_data.count_item_quantity(barcode)
                if checkout_quantity + 1 > stock_quantity:
                    QMessageBox.warning(self, "Stock Limit Reached", 
                                        "Cannot add more of this item. It exceeds available stock.")
                else:
                    item = self.inventory_data.checkout_find(barcode)
                    # 100% discount and $0 ensure it's treated as a free unit in totals
                    self.checkout_list.append({ "Username": self.username, 
                                            "SKU": item.get("SKU"),
                                            "Barcode": item.get("Barcode"),
                                            "Item Name": item.get("Item Name"),
                                            "Quantity": "1",
                                            "Unit Price": item.get("Price per Unit"),
                                            "Discount": "100%",
                                            "Net Price": "$0",
                                            "Line Total": "$0"})
                    # Refresh checkout display
                    self.load_checkout_table()
                    self.ui.checkout_table.clearSelection()
                    self.checkout_get_total()
                    self.ui.barcode_lineEdit.clear()
                    self.ui.barcode_lineEdit.setFocus()
                    self.inventory_data.update_item_statuses()

    def checkout_count_item_quantity(self, barcode):
        """
        Calculate the total quantity of a specific item in the current checkout list.

        Args:
            barcode (str): Barcode of the item to count.

        Returns:
            int: Total quantity of the specified item currently in the checkout list. Returns 0 if not found.
        """
        checkout_quantity = 0
        for row in self.checkout_list:
                    if row["Barcode"] == barcode:
                        checkout_quantity += int(row["Quantity"])
        return checkout_quantity

    def checkout_get_total(self):
        """
        Calculate and display the total amount for the current checkout.
        
        Returns:
            Decimal: The total amount of the checkout
        """
        self.ui.total_lbl.setText(f"$0")  # Reset display
        total = Decimal(0)
        # Sum all line totals
        for row in self.checkout_list:
            total += Decimal(row["Line Total"].replace(",", "").strip("$"))
        self.ui.total_lbl.setText(f"${total.quantize(Decimal('0.01')):,}")  # Format with 2 decimal places
        return total
    
    def checkout_compute_change(self):
        """Calculate and display the change due based on cash received."""
        total = self.checkout_get_total()
        cash_received = self.ui.cash_received_lineEdit.text().strip().strip("$").replace(",", "")
        try:
            change_due = Decimal(cash_received) - total
            if change_due < 0:
                self.ui.change_due_lbl.setText("$0")  # Don't show negative change
            else:
                self.ui.change_due_lbl.setText(f"${change_due.quantize(Decimal('0.01')):,}")
        except (ValueError, InvalidOperation):
            self.ui.change_due_lbl.setText("$0")  # Handle invalid input

    def checkout_payment_selection(self, payment_method):
        """
        Set the payment method and update UI accordingly.
        
        Args:
            payment_method (str): Either "Cash" or "Card" payment method or "Reset" to reset button selection
        """
        disabled_button_style = """
        background-color: #e0e0e0;
        color: #7f8c8d;
        border: 2px solid #bdc3c7;
        border-radius: 5px;
        font-family: "Segoe UI";
        font-weight: 600;
        font-size: 12pt;
        """
        if payment_method == "Cash":
            self.payment_method = "Cash"
            self.ui.cash_btn.setStyleSheet("")  # default style
            self.ui.card_btn.setStyleSheet(disabled_button_style)  # visually indicate inactive
        elif payment_method == "Card":
            self.payment_method = "Card"
            self.ui.card_btn.setStyleSheet("")
            self.ui.cash_btn.setStyleSheet(disabled_button_style)
        elif payment_method == "Reset":
            self.ui.cash_btn.setStyleSheet("")
            self.ui.card_btn.setStyleSheet("")

    def perform_checkout(self):
        """Process the checkout based on selected payment method."""
        total = self.checkout_get_total()
        msg_box = QMessageBox(self)
        font = msg_box.font()
        font.setPointSize(14)
        msg_box.setFont(font)
        if self.payment_method is None:
            QMessageBox.warning(self, "Payment Method Required",
            "Please select a payment method (Cash or Card) before proceeding to checkout.")
        elif self.payment_method == "Cash":
            msg_box.setWindowTitle("Cash Payment")
            msg_box.setText(
            f"<p style='text-align: center; margin-right: 30px;'>"
            f"Please collect ${Decimal(total).quantize(Decimal('0.01')):,} in cash."
            f"<br><br>Confirm payment received? </p>")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply = msg_box.exec()
            if reply == QMessageBox.StandardButton.Yes:
                self.finalize_checkout()
            else:
                QMessageBox.information(self, "Payment", "Cash payment not confirmed.")
        elif self.payment_method == "Card":
            # TODO: Implement card payment method
            msg_box.setWindowTitle("Card Payment")
            msg_box.setText("<p style='text-align: center; margin-right: 30px;'>Card payment is unavailable</p>")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def finalize_checkout(self):
        """Finalize the checkout process by updating inventory and clearing the checkout."""
        if not self.checkout_list:
            QMessageBox.warning(self, "Empty List", "The checkout list is empty!")
            return
        else:
            # First reduce stock quantities for all items
            for item in self.checkout_list:
                try:
                    self.inventory_data.reduce_stock_quantity(item["Barcode"], item["Quantity"], item["Item Name"])
                except ValueError as e:
                    QMessageBox.warning(self, "Stock Reduction Failed", str(e))
                    return  # Abort if any reduction fails

            # Record the sale if all reductions succeeded
            self.sales_data.record_sales(self.checkout_list)
            self.inventory_data.update_item_statuses()
            # Reset checkout state
            self.checkout_list = []
            self.checkout_payment_selection("Reset")
            self.load_checkout_table()
            self.checkout_get_total()
            # Refresh inventory display
            self.load_csv_to_table(self.ui.inventory_table, INVENTORY_DATA)
            self.set_header_info_texts()
            self.ui.barcode_lineEdit.setFocus()
            # Update all reports
            self.filter_sales_history_table()
            self.filter_sales_summary_table()
            self.filter_top_employees_table()
            self.filter_top_products_table()
            QMessageBox.information(self, "Checkout Complete", "Checkout completed successfully.")

    def load_checkout_table(self):
        """Load the checkout items into the checkout table."""
        self.ui.checkout_table.setRowCount(len(self.checkout_list))
        headers = ["Barcode", "Item Name", "Quantity", 
                    "Unit Price", "Discount", 
                    "Net Price", "Line Total"]
        # Fill the table by iterating over each row and each item in that row
        for row_index, row_dict in enumerate(self.checkout_list):
            for column_index, header in enumerate(headers):
                value = row_dict.get(header)
                self.ui.checkout_table.setItem(row_index, column_index, QTableWidgetItem(value))

    def discount_item_popup(self):
        """Show the discount popup for the selected inventory item."""
        table_row_index = self.ui.inventory_table.currentRow()

        if table_row_index != -1:
            barcode = self.ui.inventory_table.item(table_row_index, 3).text()  # type: ignore
            batch_number = self.ui.inventory_table.item(table_row_index, 4).text()  # type: ignore
            popup = DiscountItem(INVENTORY_DATA, barcode, batch_number)
            popup.exec()
            # Refresh inventory after discount change
            self.load_csv_to_table(self.ui.inventory_table, INVENTORY_DATA)
            self.set_header_info_texts()
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before applying discount.")

    def filter_sales_history_table(self):
        """Filter sales history table by date range."""
        from_date = self.ui.from_date.date().toPython()
        to_date = self.ui.to_date.date().toPython()

        matched_data = self.sales_data.sort_by_date_interval(from_date, to_date)

        # Set number of rows based on filtered data
        self.ui.sales_history_table.setRowCount(len(matched_data))
        
        headers = ["Username", "SKU", "Barcode", "Order ID", "Item Name", 
                   "Quantity", "Unit Price", "Discount", 
                    "Net Price", "Line Total", "Sale Date"]

        # Populate table with filtered data
        for row_index, row_dict in enumerate(matched_data):
            for column_index, header in enumerate(headers):
                value = row_dict.get(header)
                self.ui.sales_history_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))
            
    def reset_sales_history_table(self):
        """Reset sales history date filters to default range."""
        self.ui.from_date.setDate(QDate(2025, 1, 1))  # Arbitrary start date
        self.ui.to_date.setDate(QDate.currentDate())

    def filter_sales_summary_table(self):
        """Filter sales summary table by selected time period."""
        filter_date = self.ui.filter_summary_comboBox.currentText()
        top_products_data = self.sales_data.get_sales_summary_data(filter_date)

        # Clear the current table
        self.ui.sales_summary_table.setRowCount(0)

        # Set the number of rows in the table to match the number of filtered records
        self.ui.sales_summary_table.setRowCount(len(top_products_data))

        # Loop through each matched record and insert into the table
        for row_index, row in enumerate(top_products_data):
            self.ui.sales_summary_table.setItem(row_index, 0, QTableWidgetItem(row[0]))              # Date
            self.ui.sales_summary_table.setItem(row_index, 1, QTableWidgetItem(str(row[1])))         # Total orders
            self.ui.sales_summary_table.setItem(row_index, 2, QTableWidgetItem(str(row[2])))         # Total quantity
            self.ui.sales_summary_table.setItem(row_index, 3, QTableWidgetItem(f"${row[3]:,}"))      # Gross sales
            self.ui.sales_summary_table.setItem(row_index, 4, QTableWidgetItem(f"${row[4]:,}"))      # Discounts
            self.ui.sales_summary_table.setItem(row_index, 5, QTableWidgetItem(f"${row[5]:,}"))      # Net sales
            self.ui.sales_summary_table.setItem(row_index, 6, QTableWidgetItem(f"${row[6]:,}"))      # Average order value

    def filter_top_products_table(self):
        """Filter top products table by selected time period."""
        filter_date = self.ui.filter_products_comboBox.currentText()
        top_products_data = self.sales_data.get_top_products_data(filter_date)

        # Clear the current table
        self.ui.top_products_table.setRowCount(0)

        # Set the number of rows in the table to match the number of filtered records
        self.ui.top_products_table.setRowCount(len(top_products_data))

        # Loop through each matched record and insert into the table
        for row_index, row in enumerate(top_products_data):
            self.ui.top_products_table.setItem(row_index, 0, QTableWidgetItem(row[0]))              # Item name
            self.ui.top_products_table.setItem(row_index, 1, QTableWidgetItem(row[1]))              # Sku
            self.ui.top_products_table.setItem(row_index, 2, QTableWidgetItem(row[2]))              # Barcode
            self.ui.top_products_table.setItem(row_index, 3, QTableWidgetItem(str(row[3])))         # Quantity sold
            self.ui.top_products_table.setItem(row_index, 4, QTableWidgetItem(f"${row[4]:,}"))      # Total revenue

    def filter_top_employees_table(self):
        """Filter top employees table by selected time period."""
        filter_date = self.ui.filter_employees_comboBox.currentText()
        top_employees_data = self.sales_data.get_top_employees_data(filter_date)

        # Clear the current table
        self.ui.top_employees_table.setRowCount(0)

        # Set the number of rows in the table to match the number of filtered records
        self.ui.top_employees_table.setRowCount(len(top_employees_data))

        # Loop through each matched record and insert into the table
        for row_index, row in enumerate(top_employees_data):
            self.ui.top_employees_table.setItem(row_index, 0, QTableWidgetItem(row[0]))              # Username
            role = self.user_data.get_role(row[0])
            self.ui.top_employees_table.setItem(row_index, 1, QTableWidgetItem(str(role)))           # Role
            self.ui.top_employees_table.setItem(row_index, 2, QTableWidgetItem(str(row[1])))         # Transactions
            self.ui.top_employees_table.setItem(row_index, 3, QTableWidgetItem(str(row[2])))         # Items sold
            self.ui.top_employees_table.setItem(row_index, 4, QTableWidgetItem(f"${row[3]:,}"))      # Total revenue

    def add_popup_ui(self, popup_obj, table_widget, csv_file_path):
        """
        Show the add popup and reload the table after adding.
        
        Args:
            popup_obj: The popup window object to show
            table_widget: The table widget to reload after adding
            csv_file_path: Path to the CSV file to load into the table
        """
        # Display add popup window
        popup_obj.exec()
        # Reload the table to reflect changes
        self.load_csv_to_table(table_widget, csv_file_path)
        self.set_header_info_texts()  # Update summary information
        self.inventory_data.update_item_statuses()

    def update_ui(self, popup_obj, table_widget, csv_file_path):
        """
        Show the update popup for the selected item and reload the table.
        
        Args:
            popup_obj: The popup window object to show
            table_widget: The table widget containing the item to update
            csv_file_path: Path to the CSV file to load into the table
        """
        # Get the index of the currently selected row in the table
        selected_row = table_widget.currentRow()
        # Proceed only if a row is selected
        if selected_row != -1:
            # Determine which table is being updated
            if table_widget == self.ui.user_table:
                # For the user table, use the username as the key
                keyword = table_widget.item(selected_row, 0).text()
            elif table_widget == self.ui.inventory_table:
                # For the inventory table, use the batch number as the key
                keyword = table_widget.item(selected_row, 4).text()

            # Open the update dialog for the selected item
            popup_obj.perform_update(keyword)  # type: ignore
            popup_obj.exec()

            # Refresh the internal data statuses after update
            self.inventory_data.update_item_statuses()
            # Reload the table to reflect changes
            self.load_csv_to_table(table_widget, csv_file_path)
            self.set_header_info_texts() # Update summary information

            # Clear the selection to avoid confusion after reload
            table_widget.clearSelection()

        else:
            # Alert the user if no row was selected
            QMessageBox.warning(self, "No Selection", "Select a row before updating.")

    def delete_ui(self, data_obj, table_widget, csv_file_path):
        """
        Delete the selected item after confirmation and reload the table.
        
        Args:
            data_obj: The data handler object (UserDatabase or InventoryData)
            table_widget: The table widget containing the item to delete
            csv_file_path: Path to the CSV file to load into the table
        """
        # Get the index of the currently selected row in the table
        selected_row = table_widget.currentRow()

        # Proceed only if a row is selected
        if selected_row != -1:
            # Determine which table is being updated
            if table_widget == self.ui.user_table: 
                # For the user table, use the username as the key
                keyword = table_widget.item(selected_row, 0).text()
                # Set info text for user deletation
                info_text = f"user '{keyword}'"
            elif table_widget == self.ui.inventory_table:
                # For the inventory table, use the batch number as the key
                keyword = table_widget.item(selected_row, 4).text() 
                item_name = table_widget.item(selected_row, 1).text()  # type: ignore
                # Set info text for item deletation
                info_text = f"item '{item_name}' with batch number {keyword}"

            # Get confirmation
            confirm = QMessageBox.question(self, "Confirm Delete", 
                      f"Are you sure you want to remove the {info_text}?") #type: ignore
            
            if confirm == QMessageBox.StandardButton.Yes:
                # Remove it from the CSV file
                data_obj.delete(keyword) #type: ignore
                # Reload the table
                self.load_csv_to_table(table_widget, csv_file_path)
                self.set_header_info_texts()
                # Clear row selection
                table_widget.clearSelection()
                # Display information message
                QMessageBox.information(self, "Deleted", 
                f"The {info_text} was removed successfully.") #type: ignore

        # If no row is selected display a warning message
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before deleting.")

    def search_ui(self, data_obj, table_widget, csv_file_path, lineEdit):
        """
        Search for items matching the text in the search box.
        
        Args:
            data_obj: The data handler object (UserDatabase, InventoryData or SalesData)
            table_widget: The table widget to display results in
            csv_file_path: Path to the CSV file to load if search is empty
            lineEdit: The QLineEdit widget containing the search text
        """
        # Get search keyword
        keyword = lineEdit.text()

        # Show all data if search box is empty
        if keyword == "":
            # Load the entire table
            self.load_csv_to_table(table_widget, csv_file_path)
            return

        # Get matching data as a list
        matched_data = data_obj.search(keyword)

        if matched_data is not None: 
            table_widget.setRowCount(len(matched_data))
            # Fill the table by iterating over each row and each item in that row
            for row_index, row in enumerate(matched_data):
                for column_index, item in enumerate(row):
                    table_widget.setItem(row_index, column_index, QTableWidgetItem(item))

    def clear_search_ui(self, table_widget, csv_file_path, lineEdit):
        """
        Clear the search box and reload the full table.
        
        Args:
            table_widget: The table widget to reload
            csv_file_path: Path to the CSV file to load
            lineEdit: The QLineEdit widget to clear
        """
        # Reload the table
        self.load_csv_to_table(table_widget, csv_file_path)
        lineEdit.clear()  # Clear search input

    def list_by_status(self, status):
        """
        List inventory items by their status.
        
        Args:
            status (str): The status to filter by (Low Stock, Out of Stock, Expired)
        """
        self.inventory_data.update_item_statuses()
        matched_items = self.inventory_data.find_by_status(status)

        self.ui.inventory_table.setRowCount(len(matched_items))

        # Fill the table by iterating over each row and each item in that row
        for row_index, row_list in enumerate(matched_items):
            for column_index, item in enumerate(row_list):
                self.ui.inventory_table.setItem(row_index, column_index, QTableWidgetItem(item))

    def set_table(self, table_widget):
        """
        Configure the appearance and behavior of a table widget.
        
        Args:
            table_widget: The table widget to configure
        """
        # Make all columns stretch to evenly fill the table width
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # Disable the horizontal scroll bar for cleaner appearance
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Disable all table editing to prevent accidental changes
        table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # Make clicking any cell select the entire row for better UX
        table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def set_header_info_texts(self):
        """Update all the informational labels in the UI headers."""
        # Inventory summary information
        self.ui.total_items_lbl.setText(f"{self.inventory_data.count_items()}")
        self.ui.stock_value_lbl.setText(self.inventory_data.calculate_stock_value('Price'))
        self.ui.stock_cost_lbl.setText(self.inventory_data.calculate_stock_value('Cost'))
        self.ui.low_stock_lbl.setText(f"{self.inventory_data.count_items('Low Stock')}")
        self.ui.out_of_stock_lb.setText(f"{self.inventory_data.count_items('Out of Stock')}")
        self.ui.expired_lbl.setText(f"{self.inventory_data.count_items('Expired')}")
        # User summary information
        self.ui.total_users_lbl.setText(f"{self.user_data.count_users()}")
        self.ui.admins_lbl.setText(f"{self.user_data.count_users('Admin')}")
        self.ui.managers_lbl.setText(f"{self.user_data.count_users('Manager')}")
        self.ui.cashiers_lbl.setText(f"{self.user_data.count_users('Cashier')}")

    def load_csv_to_table(self, table_widget, csv_file_path):
        """
        Load data from a CSV file into a table widget.
        
        Args:
            table_widget: The table widget to populate
            csv_file_path: Path to the CSV file to load
        """
        # Open csv file and read the content as a list
        with open(csv_file_path, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Set number of rows (excluding header)
        table_widget.setRowCount(len(data) - 1)
        
        # Fill the table by iterating over each row and each item in that row (skip header row)
        for row_index, row_list in enumerate(data[1:]):
            for column_index, item in enumerate(row_list):
                table_widget.setItem(row_index, column_index, QTableWidgetItem(item))

    def account_popup_ui(self):
        """Show account information popup and handle logout."""
        # Local import to avoid circular import errors
        from log_in import LogInWindow
        self.account_popup.exec()

        # If user logged out from the popup
        if self.account_popup.log_out:
            # Create and show login window
            self.login_window = LogInWindow()
            self.login_window.show() 
            self.close()  # Close Main UI window

    def set_user_access(self, role):
        """
        Controls which UI pages are visible to the user based on their role.

        Args:
            role (str): User role.
        """
        if role == "Cashier":
            self.ui.inventory_btn.hide()
            self.ui.reports_btn.hide()
            self.ui.users_btn.hide()
        elif role == "Manager":
            self.ui.users_btn.hide()