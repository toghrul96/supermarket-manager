from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                               QTableWidgetItem, QAbstractItemView, QHeaderView,
                               QSizePolicy)
from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, Qt, QDate
from PySide6.QtGui import QFont
from ui.ui_main import Ui_MainWindow
from models.user import UserDatabase
from models.sales import SalesData
from models.inventory import InventoryData
from popups import (AddNewUser, UpdateUser, AddNewItem, UpdateItem, DiscountItem,
                    CheckoutDiscountItem, SetQuantity, AccountInfo, ProductsPopup,
                    ReturnItemPopup)
from worker import run_worker
from decimal import Decimal, InvalidOperation

USER_DATA = "users"
INVENTORY_DATA = "inventory"
SALES_DATA = "sales"


class MainWindow(QMainWindow):
    """
    Main application window for the supermarket management system.

    This class handles initialization of the user interface, connecting UI elements
    to their logic, and loading user, inventory, and sales data. It manages navigation,
    popups, checkout processing, filtering, and reports.
    """
    def __init__(self, username, user_data, role):
        """
        Initialize the main window with UI setup, data connections, and signal bindings.

        Args:
            username (str): Username of the logged-in user.
            user_data: Authenticated UserDatabase instance.
            role (str): Role of the logged-in user (fetched during login, passed in to
                        avoid a synchronous DB call on the main thread).
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Use the passed user_data instance (already logged in)
        self.user_data = user_data
        self.username = username
        self.role = role
        self.set_user_access(self.role)

        # Grab the logged-in user's UUID from the active Supabase session
        # (used later when recording sales so each transaction knows who made it)
        session = self.user_data.supabase.auth.get_session()
        self._user_uuid = session.user.id if session and session.user else None

        # Initialize data handlers
        self.inventory_data = InventoryData(
            access_token=self.user_data._access_token,
            refresh_token=self.user_data._refresh_token,
        )
        self.sales_data = SalesData(
            access_token=self.user_data._access_token,
            refresh_token=self.user_data._refresh_token,
        )

        # Initialize popup windows for user, item, and account operations
        self.add_user_popup = AddNewUser(user_data=self.user_data)
        self.update_user_popup = UpdateUser(user_data=self.user_data)
        self.add_item_popup = AddNewItem(inventory_data=self.inventory_data)
        self.update_item_popup = UpdateItem(inventory_data=self.inventory_data)
        self.account_popup = AccountInfo(self.username, self.role)
        self.products_popup = ProductsPopup(inventory_data=self.inventory_data)

        # Return Item popup — created once, reused on each open
        self.return_item_popup = ReturnItemPopup(
            sales_data=self.sales_data,
            user_uuid=self._user_uuid,
            on_return_complete=self._on_return_complete,
        )

        # Checkout-related variables
        self.checkout_list = []         # List of items added to checkout
        self.payment_method = None      # Selected payment method at checkout

        # Sidebar toggle state (collapsed by default)
        self.sidebar_expanded = False

        # Thread tracking — keeps references alive until threads finish
        self._threads = {}

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
        self.ui.available_btn.clicked.connect(lambda: self.list_by_status("Available"))
        self.ui.low_stock_btn.clicked.connect(lambda: self.list_by_status("Low Stock"))
        self.ui.out_of_stock_btn.clicked.connect(lambda: self.list_by_status("Out of Stock"))
        self.ui.expired_btn.clicked.connect(lambda: self.list_by_status("Expired"))
        self.ui.products_btn.clicked.connect(self.open_products_popup)

        # Checkout buttons and shortcuts
        self.ui.checkout_add_item.clicked.connect(self.checkout_add_item)
        self.ui.checkout_add_item.setShortcut("F1")
        self.ui.cancel_sale_btn.clicked.connect(self.checkout_cancel_sale)
        self.ui.cancel_sale_btn.setShortcut("Esc")

        self.ui.return_item_btn.clicked.connect(self.open_return_item_popup)
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
        self.load_table(self.ui.user_table, USER_DATA)
        self.set_table(self.ui.inventory_table)
        self.load_table(self.ui.inventory_table, INVENTORY_DATA)
        self.set_table(self.ui.sales_history_table)
        self.load_table(self.ui.sales_history_table, SALES_DATA)
        self.set_table(self.ui.sales_summary_table)
        self.filter_sales_summary_table()
        self.set_table(self.ui.top_products_table)
        self.filter_top_products_table()
        self.set_table(self.ui.top_employees_table)
        self.filter_top_employees_table()

        # Set up the Returned Items tab (already in ui_main.py) and load its data
        self.set_table(self.ui.returned_items_table)
        self.load_returned_items_table()

        # Wire up the returned items search and clear button
        self.ui.returned_search_lineEdit.textChanged.connect(
            lambda: self.load_returned_items_table(keyword=self.ui.returned_search_lineEdit.text() or None))
        self.ui.clear_returned_tbl_btn.clicked.connect(
            lambda: [self.ui.returned_search_lineEdit.clear(), self.load_returned_items_table()])

        # Set font size for better readability in tables
        font = QFont()
        font.setPointSize(12)
        self.ui.user_table.verticalHeader().setFont(font)
        self.ui.inventory_table.verticalHeader().setFont(font)
        self.ui.sales_history_table.verticalHeader().setFont(font)
        self.ui.sales_summary_table.verticalHeader().setFont(font)
        self.ui.top_products_table.verticalHeader().setFont(font)
        self.ui.top_employees_table.verticalHeader().setFont(font)
        self.ui.returned_items_table.verticalHeader().setFont(font)

        # Checkout table with larger font and hidden internal columns
        self.set_table(self.ui.checkout_table)
        font2 = QFont()
        font2.setPointSize(18)
        self.ui.checkout_table.verticalHeader().setFont(font2)
        self.ui.checkout_table.setColumnHidden(0, True)  # Hide barcode

        # Default "To Date" for reports = Today
        self.ui.to_date.setDate(QDate.currentDate())

        # Update dashboard info and item statuses in the background
        self.set_header_info_texts()
        self._fire_and_forget(self.inventory_data.update_item_statuses)


    def switch_to_checkout_page(self):
        """Switch the stacked widget to show the checkout page."""
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.barcode_lineEdit.setFocus()  # Immediate focus for scanning barcode

    # -- threading helpers -----------------------------------------------------

    def _run_worker(self, fn, *args, on_result=None, on_error=None, **kwargs):
        """Start a background worker and keep relay alive until it finishes."""
        key_holder = [None]

        def wrap(callback):
            def wrapped(value):
                # Remove the thread from tracking once it completes
                self._threads.pop(key_holder[0], None)
                if callback:
                    callback(value)
            return wrapped

        thread, relay = run_worker(
            fn, *args,
            on_result=wrap(on_result),
            on_error=wrap(on_error),
            **kwargs
        )
        key = id(relay)
        key_holder[0] = key #type: ignore
        # Store thread and relay to prevent garbage collection before completion
        self._threads[key] = (thread, relay)
        return thread

    def _fire_and_forget(self, fn, *args, **kwargs):
        """Run a DB operation in the background with no UI callback."""
        self._run_worker(fn, *args, **kwargs)

    # -------------------------------------------------------------------------
    
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
            self.ui.logo.setText("Supermarket\nManagement\n     System")
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
            self.ui.logo.setText("S.M.S")
            self.ui.logo.setMinimumWidth(80)
            self.ui.logo.setStyleSheet(""" font-size: 22px; """)
            for btn in (self.ui.checkout_btn, self.ui.inventory_btn, self.ui.reports_btn, 
            self.ui.users_btn, self.ui.exit_btn):
                btn.setText("")
                btn.setStyleSheet("""qproperty-iconSize: 33px 33px""")

        self.anim_group.start()

    def checkout_add_item(self):
        """Add an item to the checkout list based on barcode input."""
        barcode = self.ui.barcode_lineEdit.text()

        self.ui.barcode_lineEdit.setEnabled(False)
        self.ui.checkout_add_item.setEnabled(False)

        def fetch():
            return self.inventory_data.checkout_find(barcode)

        def on_result(item):
            self.ui.barcode_lineEdit.setEnabled(True)
            self.ui.checkout_add_item.setEnabled(True)

            repeated_item = False
            quantity = 1
            for index, row in enumerate(self.checkout_list):
                if barcode == row["Barcode"]:
                    # Item already in checkout — increment quantity and recalculate line total
                    repeated_item = True
                    quantity = int(row["Quantity"]) + 1
                    line_total = quantity * Decimal(item.get("Net Price").strip("$").replace(",", ""))  # type: ignore
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
                self.checkout_list.append({"Username": self.username,
                                           "SKU": item.get("SKU"),
                                           "Barcode": item.get("Barcode"),
                                           "Item Name": item.get("Item Name"),
                                           "Quantity": "1",
                                           "Unit Price": item.get("Price per Unit"),
                                           "Discount": item.get("Discount"),
                                           "Net Price": item.get("Net Price"),
                                           "Line Total": item.get("Net Price")})
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.clear()
            self.ui.barcode_lineEdit.setFocus()
            self._fire_and_forget(self.inventory_data.update_item_statuses)

        def on_error(msg):
            self.ui.barcode_lineEdit.setEnabled(True)
            self.ui.checkout_add_item.setEnabled(True)
            clean_msg = str(msg).strip().splitlines()[-1]
            QMessageBox.warning(self, "Add Item Failed", clean_msg)
            self.ui.barcode_lineEdit.clear()
            self.ui.barcode_lineEdit.setFocus()

        self._run_worker(fetch, on_result=on_result, on_error=on_error)

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

        if table_row_index == -1:
            QMessageBox.warning(self, "No Selection", "Select an item before changing its quantity.")
            self.ui.barcode_lineEdit.setFocus()
            return

        barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
        quantity = int(self.ui.checkout_table.item(table_row_index, 2).text())  # type: ignore

        if operation == "-":
            # No DB call needed — pure Python update
            quantity = max(1, quantity - 1)
            row = self.checkout_list[table_row_index]
            row["Quantity"] = str(quantity)
            net_price = Decimal(row["Net Price"].replace(",", "").strip("$"))
            row["Line Total"] = f"${(net_price * Decimal(quantity)).quantize(Decimal('0.01')):,}"
            self.load_checkout_table()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()
            return

        # "+" requires a DB stock check
        self.ui.increase_item_btn.setEnabled(False)
        checkout_quantity = self.checkout_count_item_quantity(barcode)

        def fetch():
            return self.inventory_data.count_item_quantity(barcode)

        def on_result(stock_quantity):
            self.ui.increase_item_btn.setEnabled(True)
            if (checkout_quantity + 1) > stock_quantity:
                QMessageBox.warning(self, "Stock Limit Reached",
                                    "Cannot add more of this item. It exceeds available stock.")
                return
            new_qty = quantity + 1
            row = self.checkout_list[table_row_index]
            row["Quantity"] = str(new_qty)
            net_price = Decimal(row["Net Price"].replace(",", "").strip("$"))
            row["Line Total"] = f"${(net_price * Decimal(new_qty)).quantize(Decimal('0.01')):,}"
            self.load_checkout_table()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()

        def on_error(msg):
            self.ui.increase_item_btn.setEnabled(True)
            QMessageBox.warning(self, "Stock Check Failed", msg)

        self._run_worker(fetch, on_result=on_result, on_error=on_error)
    
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

        if table_row_index == -1:
            QMessageBox.warning(self, "No Selection", "Select a row before setting quantity.")
            return

        barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
        current_row_quantity = int(self.ui.checkout_table.item(table_row_index, 2).text())  # type: ignore
        checkout_quantity = self.checkout_count_item_quantity(barcode)

        self.ui.set_quantity_btn.setEnabled(False)

        def fetch():
            return self.inventory_data.count_item_quantity(barcode)

        def on_result(stock_quantity):
            self.ui.set_quantity_btn.setEnabled(True)
            popup = SetQuantity(self.checkout_list, barcode,
                                current_row_quantity, checkout_quantity, stock_quantity, table_row_index)
            popup.exec()
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.setFocus()

        def on_error(msg):
            self.ui.set_quantity_btn.setEnabled(True)
            QMessageBox.warning(self, "Stock Check Failed", msg)

        self._run_worker(fetch, on_result=on_result, on_error=on_error)
    
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

        if table_row_index == -1:
            QMessageBox.warning(self, "No Selection", "Select an item before adding a free unit.")
            return

        item_name = self.ui.checkout_table.item(table_row_index, 1).text()  # type: ignore
        confirm = QMessageBox.question(self, "Add Free Unit",
            f"Add a free promotional unit of '{item_name}' to the checkout?")

        if confirm != QMessageBox.StandardButton.Yes:
            return

        barcode = self.ui.checkout_table.item(table_row_index, 0).text()  # type: ignore
        checkout_quantity = self.checkout_count_item_quantity(barcode)

        self.ui.add_free_unit_btn.setEnabled(False)

        def fetch():
            stock_quantity = self.inventory_data.count_item_quantity(barcode)
            item = self.inventory_data.checkout_find(barcode)
            return stock_quantity, item

        def on_result(result):
            self.ui.add_free_unit_btn.setEnabled(True)
            stock_quantity, item = result
            if checkout_quantity + 1 > stock_quantity:
                QMessageBox.warning(self, "Stock Limit Reached",
                                    "Cannot add more of this item. It exceeds available stock.")
                return
            # Free unit has 100% discount and $0 net price so it doesn't affect the total
            self.checkout_list.append({"Username": self.username,
                                       "SKU": item.get("SKU"),
                                       "Barcode": item.get("Barcode"),
                                       "Item Name": item.get("Item Name"),
                                       "Quantity": "1",
                                       "Unit Price": item.get("Price per Unit"),
                                       "Discount": "100%",
                                       "Net Price": "$0",
                                       "Line Total": "$0"})
            self.load_checkout_table()
            self.ui.checkout_table.clearSelection()
            self.checkout_get_total()
            self.ui.barcode_lineEdit.clear()
            self.ui.barcode_lineEdit.setFocus()
            self._fire_and_forget(self.inventory_data.update_item_statuses)

        def on_error(msg):
            self.ui.add_free_unit_btn.setEnabled(True)
            QMessageBox.warning(self, "Error", msg)

        self._run_worker(fetch, on_result=on_result, on_error=on_error)

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

        self.ui.checkout_btn_2.setEnabled(False)
        self.ui.checkout_btn_2.setText("Processing...")

        # Snapshot the list so the worker has a stable copy
        items_snapshot = list(self.checkout_list)

        def do_finalize():
            for item in items_snapshot:
                self.inventory_data.reduce_stock_quantity(
                    item["Barcode"], item["Quantity"], item["Item Name"])
            self.sales_data.record_sales(items_snapshot, self._user_uuid)
            self.inventory_data.update_item_statuses()

        def on_result(_):
            self.ui.checkout_btn_2.setEnabled(True)
            self.ui.checkout_btn_2.setText("Checkout")
            self.checkout_list = []
            self.checkout_payment_selection("Reset")
            self.load_checkout_table()
            self.checkout_get_total()
            self.load_table(self.ui.inventory_table, INVENTORY_DATA)
            self.set_header_info_texts()
            self.ui.barcode_lineEdit.setFocus()
            # Refresh all report tables to reflect the new sale
            self.filter_sales_history_table()
            self.filter_sales_summary_table()
            self.filter_top_employees_table()
            self.filter_top_products_table()
            QMessageBox.information(self, "Checkout Complete", "Checkout completed successfully.")

        def on_error(msg):
            self.ui.checkout_btn_2.setEnabled(True)
            self.ui.checkout_btn_2.setText("Checkout")
            QMessageBox.warning(self, "Checkout Failed", msg)

        self._run_worker(do_finalize, on_result=on_result, on_error=on_error)

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
            batch_number = self.ui.inventory_table.item(table_row_index, 1).text()  # col 1 = Batch Number #type: ignore
            popup = DiscountItem(batch_number, inventory_data=self.inventory_data)
            popup.exec()
            # Refresh inventory after discount change
            self.load_table(self.ui.inventory_table, INVENTORY_DATA)
            self.set_header_info_texts()
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before applying discount.")

    def open_products_popup(self):
        """Open the Products popup, refreshing data each time."""
        self.products_popup.load_products()
        self.products_popup.exec()
        # Reload inventory table and stats in case any product names/categories changed
        self.load_table(self.ui.inventory_table, INVENTORY_DATA)
        self.set_header_info_texts()

    def filter_sales_history_table(self):
        """Filter sales history table by date range."""
        from_date = self.ui.from_date.date().toPython()
        to_date   = self.ui.to_date.date().toPython()

        def fetch():
            return self.sales_data.sort_by_date_interval(from_date, to_date)

        def on_result(matched_data):
            self.ui.sales_history_table.setRowCount(len(matched_data))
            headers = ["Username", "SKU", "Barcode", "Order ID", "Item Name",
                       "Quantity", "Unit Price", "Discount",
                       "Net Price", "Line Total", "Sale Date"]
            for row_index, row_dict in enumerate(matched_data):
                for column_index, header in enumerate(headers):
                    value = row_dict.get(header, "")
                    self.ui.sales_history_table.setItem(
                        row_index, column_index, QTableWidgetItem(str(value)))

        self._run_worker(fetch, on_result=on_result)
            
    def reset_sales_history_table(self):
        """Reset sales history date filters to default range."""
        self.ui.from_date.setDate(QDate(2025, 1, 1))  # Arbitrary start date
        self.ui.to_date.setDate(QDate.currentDate())

    def filter_sales_summary_table(self):
        """Filter sales summary table by selected time period."""
        filter_date = self.ui.filter_summary_comboBox.currentText()

        def fetch():
            return self.sales_data.get_sales_summary_data(filter_date)

        def on_result(data):
            self.ui.sales_summary_table.setRowCount(0)
            self.ui.sales_summary_table.setRowCount(len(data))
            for row_index, row in enumerate(data):
                self.ui.sales_summary_table.setItem(row_index, 0, QTableWidgetItem(row[0]))              # Date
                self.ui.sales_summary_table.setItem(row_index, 1, QTableWidgetItem(str(row[1])))         # Total orders
                self.ui.sales_summary_table.setItem(row_index, 2, QTableWidgetItem(str(row[2])))         # Total quantity
                self.ui.sales_summary_table.setItem(row_index, 3, QTableWidgetItem(f"${row[3]:,}"))      # Gross sales
                self.ui.sales_summary_table.setItem(row_index, 4, QTableWidgetItem(f"${row[4]:,}"))      # Discounts
                self.ui.sales_summary_table.setItem(row_index, 5, QTableWidgetItem(f"${row[5]:,}"))      # Net sales
                self.ui.sales_summary_table.setItem(row_index, 6, QTableWidgetItem(f"${row[6]:,}"))      # Average order value

        self._run_worker(fetch, on_result=on_result)

    def filter_top_products_table(self):
        """Filter top products table by selected time period."""
        filter_date = self.ui.filter_products_comboBox.currentText()

        def fetch():
            return self.sales_data.get_top_products_data(filter_date)

        def on_result(data):
            self.ui.top_products_table.setRowCount(0)
            self.ui.top_products_table.setRowCount(len(data))
            for row_index, row in enumerate(data):
                self.ui.top_products_table.setItem(row_index, 0, QTableWidgetItem(row[0]))              # Item name
                self.ui.top_products_table.setItem(row_index, 1, QTableWidgetItem(row[1]))              # Sku
                self.ui.top_products_table.setItem(row_index, 2, QTableWidgetItem(row[2]))              # Barcode
                self.ui.top_products_table.setItem(row_index, 3, QTableWidgetItem(str(row[3])))         # Quantity sold
                self.ui.top_products_table.setItem(row_index, 4, QTableWidgetItem(f"${row[4]:,}"))      # Total revenue

        self._run_worker(fetch, on_result=on_result)

    def filter_top_employees_table(self):
        """Filter top employees table by selected time period."""
        filter_date = self.ui.filter_employees_comboBox.currentText()

        def fetch():
            rows = self.sales_data.get_top_employees_data(filter_date)
            # Augment each row with role from DB
            result = []
            for row in rows:
                role = self.user_data.get_role(row[0])
                result.append((row[0], str(role), str(row[1]), str(row[2]), row[3]))
            return result

        def on_result(data):
            self.ui.top_employees_table.setRowCount(0)
            self.ui.top_employees_table.setRowCount(len(data))
            for row_index, row in enumerate(data):
                self.ui.top_employees_table.setItem(row_index, 0, QTableWidgetItem(row[0]))
                self.ui.top_employees_table.setItem(row_index, 1, QTableWidgetItem(row[1]))
                self.ui.top_employees_table.setItem(row_index, 2, QTableWidgetItem(row[2]))
                self.ui.top_employees_table.setItem(row_index, 3, QTableWidgetItem(row[3]))
                self.ui.top_employees_table.setItem(row_index, 4, QTableWidgetItem(f"${row[4]:,}"))

        self._run_worker(fetch, on_result=on_result)

    def add_popup_ui(self, popup_obj, table_widget, table_name):
        """
        Show the add popup and reload the table after adding.

        Args:
            popup_obj: The popup window object to show.
            table_widget: The table widget to reload after adding.
            table_name (str): Table name passed to load_table for refresh.
        """
        popup_obj.exec()
        # Reload the table in the background after the popup closes
        self.load_table(table_widget, table_name)
        self.set_header_info_texts()
        self._fire_and_forget(self.inventory_data.update_item_statuses)

    def update_ui(self, popup_obj, table_widget, table_name):
        """
        Show the update popup for the selected item and reload the table.

        Args:
            popup_obj: The popup window object to show.
            table_widget: The table widget containing the item to update.
            table_name (str): Table name passed to load_table for refresh.
        """
        selected_row = table_widget.currentRow()
        if selected_row != -1:
            if table_widget == self.ui.user_table:
                keyword = table_widget.item(selected_row, 0).text()
            elif table_widget == self.ui.inventory_table:
                keyword = table_widget.item(selected_row, 1).text()  # col 1 = Batch Number

            popup_obj.perform_update(keyword)  # type: ignore
            popup_obj.exec()

            self._fire_and_forget(self.inventory_data.update_item_statuses)
            self.load_table(table_widget, table_name)
            self.set_header_info_texts()
            table_widget.clearSelection()
        else:
            QMessageBox.warning(self, "No Selection", "Select a row before updating.")

    def delete_ui(self, data_obj, table_widget, table_name):
        """
        Delete the selected item after confirmation and reload the table.

        Args:
            data_obj: The data handler object (UserDatabase or InventoryData).
            table_widget: The table widget containing the item to delete.
            table_name (str): Table name passed to load_table for refresh.
        """
        selected_row = table_widget.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Select a row before deleting.")
            return

        if table_widget == self.ui.user_table:
            keyword = table_widget.item(selected_row, 0).text()
            info_text = f"user '{keyword}'"
        elif table_widget == self.ui.inventory_table:
            keyword = table_widget.item(selected_row, 1).text()   # col 1 = Batch Number
            item_name = table_widget.item(selected_row, 0).text()  # col 0 = Item Name
            info_text = f"item '{item_name}' with batch number {keyword}"

        confirm = QMessageBox.question(self, "Confirm Delete",
                  f"Are you sure you want to remove the {info_text}?")  # type: ignore

        if confirm == QMessageBox.StandardButton.Yes:
            for btn in (self.ui.delete_user_btn, self.ui.delete_item_btn):
                btn.setEnabled(False)

            def do_delete():
                data_obj.delete(keyword)  # type: ignore

            def on_result(_):
                for btn in (self.ui.delete_user_btn, self.ui.delete_item_btn):
                    btn.setEnabled(True)
                self.load_table(table_widget, table_name)
                self.set_header_info_texts()
                table_widget.clearSelection()
                QMessageBox.information(self, "Deleted",
                    f"The {info_text} was removed successfully.")  # type: ignore

            def on_error(msg):
                for btn in (self.ui.delete_user_btn, self.ui.delete_item_btn):
                    btn.setEnabled(True)
                QMessageBox.warning(self, "Delete Failed", msg)

            self._run_worker(do_delete, on_result=on_result, on_error=on_error)

    def search_ui(self, data_obj, table_widget, table_name, lineEdit):
        """
        Search for items matching the text in the search box.

        Args:
            data_obj: The data handler object (UserDatabase, InventoryData, or SalesData).
            table_widget: The table widget to display results in.
            table_name (str): Table name passed to load_table when search is cleared.
            lineEdit: The QLineEdit widget containing the search text.
        """
        keyword = lineEdit.text()

        if keyword == "":
            self.load_table(table_widget, table_name)
            return

        # Snapshot keyword so the lambda captures the right value
        kw = keyword

        def fetch():
            return data_obj.search(kw)

        def on_result(matched_data):
            # Only apply if the search box still matches (user may have kept typing)
            if lineEdit.text() != kw:
                return
            if matched_data is not None:
                table_widget.setRowCount(len(matched_data))
                col_count = table_widget.columnCount()
                for row_index, row in enumerate(matched_data):
                    for column_index, item in enumerate(row):
                        if column_index >= col_count:
                            break
                        table_widget.setItem(row_index, column_index, QTableWidgetItem(item))
                    if table_widget is self.ui.inventory_table and len(row) > 9:
                        self._color_inventory_row(table_widget, row_index, row[9])

        self._run_worker(fetch, on_result=on_result)

    def clear_search_ui(self, table_widget, table_name, lineEdit):
        """
        Clear the search box and reload the full table.

        Args:
            table_widget: The table widget to reload.
            table_name (str): Table name passed to load_table for refresh.
            lineEdit: The QLineEdit widget to clear.
        """
        self.load_table(table_widget, table_name)
        lineEdit.clear()  # Clear search input

    def list_by_status(self, status):
        """
        List inventory items by their status.
        
        Args:
            status (str): The status to filter by (Low Stock, Out of Stock, Expired)
        """
        for btn in (self.ui.low_stock_btn, self.ui.out_of_stock_btn, self.ui.expired_btn):
            btn.setEnabled(False)

        def fetch():
            return self.inventory_data.find_by_status(status)

        def on_result(matched_items):
            for btn in (self.ui.low_stock_btn, self.ui.out_of_stock_btn, self.ui.expired_btn):
                btn.setEnabled(True)
            self.ui.inventory_table.setRowCount(len(matched_items))
            col_count = self.ui.inventory_table.columnCount()
            for row_index, row_list in enumerate(matched_items):
                for column_index, item in enumerate(row_list):
                    if column_index >= col_count:
                        break
                    self.ui.inventory_table.setItem(row_index, column_index, QTableWidgetItem(item))
                if len(row_list) > 9:
                    self._color_inventory_row(self.ui.inventory_table, row_index, row_list[9])

        def on_error(msg):
            for btn in (self.ui.low_stock_btn, self.ui.out_of_stock_btn, self.ui.expired_btn):
                btn.setEnabled(True)
            QMessageBox.warning(self, "Filter Failed", msg)

        self._run_worker(fetch, on_result=on_result, on_error=on_error)

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

    def _color_inventory_row(self, table_widget, row_index, status_value):
        """Apply foreground color to the Status cell (col 9) of an inventory row."""
        item = table_widget.item(row_index, 9)
        if item is None:
            return
        val = status_value.strip().lower()
        if val == "available":
            item.setForeground(Qt.GlobalColor.darkGreen)
        elif val == "low stock":
            item.setForeground(Qt.GlobalColor.darkYellow)
        elif val == "out of stock":
            item.setForeground(Qt.GlobalColor.red)
        elif val == "expired":
            from PySide6.QtGui import QColor
            item.setForeground(QColor("#7f8c8d"))

    def set_header_info_texts(self):
        """Update all the informational labels in the UI headers (runs DB queries in background)."""
        def fetch():
            return {
                'total_items':  self.inventory_data.count_items(),
                'stock_value':  self.inventory_data.calculate_stock_value('Price'),
                'stock_cost':   self.inventory_data.calculate_stock_value('Cost'),
                'low_stock':    self.inventory_data.count_items('Low Stock'),
                'out_of_stock': self.inventory_data.count_items('Out of Stock'),
                'expired':      self.inventory_data.count_items('Expired'),
                'total_users':  self.user_data.count_users(),
                'admins':       self.user_data.count_users('Admin'),
                'managers':     self.user_data.count_users('Manager'),
                'cashiers':     self.user_data.count_users('Cashier'),
            }

        def on_result(data):
            self.ui.total_items_lbl.setText(str(data['total_items']))
            self.ui.stock_value_lbl.setText(data['stock_value'])
            self.ui.stock_cost_lbl.setText(data['stock_cost'])
            self.ui.low_stock_lbl.setText(str(data['low_stock']))
            self.ui.out_of_stock_lb.setText(str(data['out_of_stock']))
            self.ui.expired_lbl.setText(str(data['expired']))
            self.ui.total_users_lbl.setText(str(data['total_users']))
            self.ui.admins_lbl.setText(str(data['admins']))
            self.ui.managers_lbl.setText(str(data['managers']))
            self.ui.cashiers_lbl.setText(str(data['cashiers']))

        self._run_worker(fetch, on_result=on_result)

    def load_table(self, table_widget, table_name):
        """
        Load data into a table widget from the database.

        Args:
            table_widget: The table widget to populate.
            table_name (str): One of "users", "inventory", or "sales".
        """
        def fetch():
            if table_name == "users":
                response = self.user_data.supabase.table("users").select("username, role, created_at").execute()
                return [
                    [row.get("username"), row.get("role").capitalize(), row.get("created_at")] #type: ignore
                    for row in (response.data or []) if isinstance(row, dict)
                ]
            elif table_name == "inventory":
                return self.inventory_data.search("")
            elif table_name == "sales":
                return self.sales_data.search("")

        def on_result(rows):
            if not rows:
                table_widget.setRowCount(0)
                return
            table_widget.setRowCount(len(rows))
            col_count = table_widget.columnCount()
            for row_index, row in enumerate(rows):
                for column_index, value in enumerate(row):
                    if column_index >= col_count:
                        break
                    display_value = str(value) if value is not None else ""
                    table_widget.setItem(row_index, column_index, QTableWidgetItem(display_value))
                # Apply status color coding only for the inventory table
                if table_widget is self.ui.inventory_table and len(row) > 9:
                    self._color_inventory_row(table_widget, row_index, str(row[9]))

        def on_error(msg):
            QMessageBox.warning(self, "Load Error", f"Failed to load data: {msg}")

        self._run_worker(fetch, on_result=on_result, on_error=on_error)

    def open_return_item_popup(self):
        """Open the Return Item dialog."""
        self.return_item_popup.exec()

    def _on_return_complete(self):
        """Refresh relevant tables after a return has been processed."""
        self.load_table(self.ui.sales_history_table, SALES_DATA)
        self.load_returned_items_table()
        self.filter_sales_summary_table()
        self.filter_top_products_table()
        self.filter_top_employees_table()

    def load_returned_items_table(self, keyword=None):
        """Load (or search) the Returned Items report table."""
        def fetch():
            return self.sales_data.get_returned_items_display(keyword=keyword)

        def on_result(rows):
            self.ui.returned_items_table.setRowCount(0)
            if not rows:
                return
            self.ui.returned_items_table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    self.ui.returned_items_table.setItem(
                        row_index, col_index,
                        QTableWidgetItem(str(value) if value is not None else ""))

        def on_error(msg):
            QMessageBox.warning(self, "Load Error",
                                f"Failed to load returned items: {msg}")

        self._run_worker(fetch, on_result=on_result, on_error=on_error)

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
        if role == "cashier":
            self.ui.inventory_btn.hide()
            self.ui.reports_btn.hide()
            self.ui.users_btn.hide()
        elif role == "manager":
            self.ui.inventory_btn.show()
            self.ui.reports_btn.show()
            self.ui.users_btn.hide()
        else:  # Admin
            self.ui.inventory_btn.show()
            self.ui.reports_btn.show()
            self.ui.users_btn.show()