from PySide6.QtGui import QIcon
import resource_rc
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QHeaderView, QAbstractItemView, QLabel,
    QLineEdit, QComboBox, QSpinBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


CATEGORIES = [
    "Bakery", "Beverages", "Canned Goods", "Dairy", "Deli",
    "Frozen", "Grains & Pasta", "Household", "Meat & Seafood",
    "Personal Care", "Produce", "Snacks & Confectionery", "Other"
]

COLUMNS = ["Category", "Item Name", "SKU", "Barcode", "Minimum Stock", "Availability"]

DIALOG_STYLE = """
    QDialog {
        background-color: #F5F7F9;
    }
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
    QPushButton:hover {
        background-color: #2c3e50;
        border-color: #2c3e50;
    }
    QPushButton:pressed {
        background-color: #22313f;
        border-color: #22313f;
    }
    QPushButton:disabled {
        background-color: #7f8c8d;
        border-color: #7f8c8d;
    }
    QLineEdit, QSpinBox, QComboBox {
        border: 1px solid #34495e;
        background: #F5F7F9;
        padding: 6px 8px;
        border-radius: 4px;
        font-family: "Segoe UI";
        font-size: 11pt;
        min-height: 32px;
    }
    QLabel {
        font-family: "Segoe UI";
        font-size: 11pt;
        color: #2c3e50;
    }
    QTableWidget {
        border: 1px solid #34495e;
        background-color: white;
        gridline-color: #dce1e7;
        font-family: "Segoe UI";
        font-size: 11pt;
    }
    QTableWidget::item:selected {
        background-color: #34495e;
        color: white;
    }
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


def _form_row(label_text, widget):
    """Return a label + widget pair in an HBoxLayout."""
    lbl = QLabel(label_text)
    lbl.setMinimumWidth(130)
    row = QHBoxLayout()
    row.addWidget(lbl)
    row.addWidget(widget)
    return row


class Ui_AddProduct:
    def setupUi(self, dialog):
        dialog.setWindowTitle("Add Product")
        _icon = QIcon()
        _icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialog.setWindowIcon(_icon)
        dialog.setMinimumWidth(420)
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 20)

        title = QLabel("Add New Product")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e; margin-bottom: 4px;")
        layout.addWidget(title)

        self.category_cb = QComboBox()
        self.category_cb.addItems(CATEGORIES)
        layout.addLayout(_form_row("Category:", self.category_cb))

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Whole Milk")
        layout.addLayout(_form_row("Item Name:", self.name_edit))

        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("13-digit EAN barcode")
        layout.addLayout(_form_row("Barcode:", self.barcode_edit))

        self.min_stock_spin = QSpinBox()
        self.min_stock_spin.setRange(0, 999999)
        self.min_stock_spin.setValue(10)
        layout.addLayout(_form_row("Minimum Stock:", self.min_stock_spin))

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(dialog.reject)
        self.add_btn = QPushButton("Add Product")
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.add_btn)
        layout.addLayout(btn_row)


class Ui_UpdateProduct:
    def setupUi(self, dialog):
        dialog.setWindowTitle("Update Product")
        _icon = QIcon()
        _icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialog.setWindowIcon(_icon)
        dialog.setMinimumWidth(420)
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 20)

        title = QLabel("Update Product")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e; margin-bottom: 4px;")
        layout.addWidget(title)

        self.category_cb = QComboBox()
        self.category_cb.addItems(CATEGORIES)
        layout.addLayout(_form_row("Category:", self.category_cb))

        self.name_edit = QLineEdit()
        layout.addLayout(_form_row("Item Name:", self.name_edit))

        self.barcode_lbl = QLabel()
        self.barcode_lbl.setStyleSheet("font-size: 11pt; color: #555;")
        layout.addLayout(_form_row("Barcode (fixed):", self.barcode_lbl))

        self.min_stock_spin = QSpinBox()
        self.min_stock_spin.setRange(0, 999999)
        layout.addLayout(_form_row("Minimum Stock:", self.min_stock_spin))

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #7f8c8d; border-color: #7f8c8d;")
        self.cancel_btn.clicked.connect(dialog.reject)
        self.update_btn = QPushButton("Update Product")
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.update_btn)
        layout.addLayout(btn_row)


class Ui_ProductsPopup:
    def setupUi(self, dialog):
        dialog.setWindowTitle("Products")
        _icon = QIcon()
        _icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialog.setWindowIcon(_icon)
        dialog.setMinimumSize(900, 560)
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 16)

        title = QLabel("Product Catalog")
        font = QFont("Segoe UI", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #34495e;")
        layout.addWidget(title)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.add_product_btn = QPushButton("Add Product")
        self.add_product_btn.setMinimumSize(140, 44)
        btn_row.addWidget(self.add_product_btn)

        self.update_product_btn = QPushButton("Update Product")
        self.update_product_btn.setMinimumSize(160, 44)
        btn_row.addWidget(self.update_product_btn)

        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumSize(100, 44)
        btn_row.addWidget(self.refresh_btn)

        layout.addLayout(btn_row)

        # Search row
        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Enter an Item Name, SKU, Barcode, or Category to Search...")
        self.search_edit.setMinimumHeight(40)
        search_row.addWidget(self.search_edit)

        self.clear_search_btn = QPushButton("Clear")
        self.clear_search_btn.setMinimumSize(100, 40)
        search_row.addWidget(self.clear_search_btn)

        layout.addLayout(search_row)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
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

        # Status label
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: #7f8c8d; font-size: 10pt;")
        layout.addWidget(self.status_lbl)