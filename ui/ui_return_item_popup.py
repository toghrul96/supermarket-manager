# -*- coding: utf-8 -*-

################################################################################
## UI definition for ReturnItemPopup
## Hand-authored to match the project's Qt Designer file conventions.
## WARNING: All changes made in this file will be lost if regenerated.
################################################################################

from PySide6.QtCore import QCoreApplication, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QVBoxLayout, QWidget,
)

_RETURN_COLS = ["Item Name", "Qty Sold", "Unit Price", "Discount", "Line Total", "Return Qty"]


class Ui_ReturnItemPopup:
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"ReturnItemPopup")

        outer = QVBoxLayout(Dialog)
        outer.setContentsMargins(20, 20, 20, 16)
        outer.setSpacing(0)

        self.stacked = QStackedWidget(Dialog)
        self.stacked.setObjectName(u"stacked")
        outer.addWidget(self.stacked)

        # ── Page 1: Order ID lookup ───────────────────────────────────────────
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        p1_layout = QVBoxLayout(self.page1)
        p1_layout.setSpacing(14)
        p1_layout.setContentsMargins(0, 0, 0, 0)

        self.page1_title = QLabel(self.page1)
        self.page1_title.setObjectName(u"page1_title")
        font_title = QFont(u"Segoe UI", 14)
        font_title.setBold(True)
        self.page1_title.setFont(font_title)
        self.page1_title.setStyleSheet(u"color: #34495e; margin-bottom: 6px;")
        p1_layout.addWidget(self.page1_title)

        self.page1_instr = QLabel(self.page1)
        self.page1_instr.setObjectName(u"page1_instr")
        self.page1_instr.setStyleSheet(u"color: #555; font-size: 11pt;")
        p1_layout.addWidget(self.page1_instr)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.order_id_edit = QLineEdit(self.page1)
        self.order_id_edit.setObjectName(u"order_id_edit")
        self.order_id_edit.setMinimumHeight(40)
        input_row.addWidget(self.order_id_edit)

        self.lookup_btn = QPushButton(self.page1)
        self.lookup_btn.setObjectName(u"lookup_btn")
        self.lookup_btn.setMinimumSize(QSize(120, 40))
        input_row.addWidget(self.lookup_btn)

        p1_layout.addLayout(input_row)

        self.page1_status = QLabel(self.page1)
        self.page1_status.setObjectName(u"page1_status")
        self.page1_status.setWordWrap(True)
        self.page1_status.setStyleSheet(
            u"font-size: 11pt; font-weight: bold; padding: 2px 0;")
        p1_layout.addWidget(self.page1_status)

        p1_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.stacked.addWidget(self.page1)

        # ── Page 2: Item selection table ──────────────────────────────────────
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        p2_layout = QVBoxLayout(self.page2)
        p2_layout.setSpacing(10)
        p2_layout.setContentsMargins(0, 0, 0, 0)

        self.page2_title = QLabel(self.page2)
        self.page2_title.setObjectName(u"page2_title")
        font_p2 = QFont(u"Segoe UI", 13)
        font_p2.setBold(True)
        self.page2_title.setFont(font_p2)
        self.page2_title.setStyleSheet(u"color: #34495e; margin-bottom: 4px;")
        p2_layout.addWidget(self.page2_title)

        self.items_table = QTableWidget(self.page2)
        self.items_table.setObjectName(u"items_table")
        self.items_table.setColumnCount(len(_RETURN_COLS))
        self.items_table.setHorizontalHeaderLabels(_RETURN_COLS)
        self.items_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, len(_RETURN_COLS)):
            self.items_table.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.items_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setMinimumHeight(220)
        p2_layout.addWidget(self.items_table)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.back_btn = QPushButton(self.page2)
        self.back_btn.setObjectName(u"back_btn")
        self.back_btn.setMinimumSize(QSize(100, 40))
        self.back_btn.setStyleSheet(
            u"background-color: #7f8c8d; border-color: #7f8c8d;"
            u"min-width: 100px; min-height: 40px;")
        btn_row.addWidget(self.back_btn)

        btn_row.addItem(
            QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.return_btn = QPushButton(self.page2)
        self.return_btn.setObjectName(u"return_btn")
        self.return_btn.setMinimumSize(QSize(160, 40))
        btn_row.addWidget(self.return_btn)

        p2_layout.addLayout(btn_row)

        self.stacked.addWidget(self.page2)

        # Page2 should not inflate height when page1 is active.
        # Swap size policies on page change so stacked fits the current page.
        self.page2.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.stacked.currentChanged.connect(self._on_page_changed)

        self.retranslateUi(Dialog)
        self.stacked.setCurrentIndex(0)

    def _on_page_changed(self, index):
        for i in range(self.stacked.count()):
            page = self.stacked.widget(i)
            if i == index:
                page.setSizePolicy(
                    QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            else:
                page.setSizePolicy(
                    QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.stacked.adjustSize()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("ReturnItemPopup", u"Return Item", None))
        self.page1_title.setText(
            QCoreApplication.translate("ReturnItemPopup", u"Return Item", None))
        self.page1_instr.setText(
            QCoreApplication.translate(
                "ReturnItemPopup", u"Enter the Order ID from the customer's receipt:", None))
        self.order_id_edit.setPlaceholderText(
            QCoreApplication.translate("ReturnItemPopup", u"e.g. ORD-A1B2C3D4", None))
        self.lookup_btn.setText(
            QCoreApplication.translate("ReturnItemPopup", u"Look Up", None))
        self.page1_status.setText(u"")
        self.page2_title.setText(
            QCoreApplication.translate("ReturnItemPopup", u"Return Items", None))
        self.back_btn.setText(
            QCoreApplication.translate("ReturnItemPopup", u"\u2190 Back", None))
        self.return_btn.setText(
            QCoreApplication.translate("ReturnItemPopup", u"Return Item(s)", None))
    # retranslateUi