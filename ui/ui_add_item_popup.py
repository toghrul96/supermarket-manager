# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_item_popupJMbfRs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDialog,
    QDoubleSpinBox, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_AddItemPopup(object):
    def setupUi(self, AddItemPopup):
        if not AddItemPopup.objectName():
            AddItemPopup.setObjectName(u"AddItemPopup")
        AddItemPopup.resize(514, 733)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddItemPopup.sizePolicy().hasHeightForWidth())
        AddItemPopup.setSizePolicy(sizePolicy)
        AddItemPopup.setMinimumSize(QSize(514, 733))
        AddItemPopup.setMaximumSize(QSize(514, 733))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        AddItemPopup.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AddItemPopup.setWindowIcon(icon)
        AddItemPopup.setStyleSheet(u"QMainWindow {\n"
"background-color: qlineargradient(\n"
"    x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #FFFFFF,\n"
"    stop:1 #E8E8E8\n"
");\n"
"}\n"
"\n"
"QLabel {\n"
"	color: #34495e;\n"
"	font-family: \"Segoe UI\";\n"
"	font-weight: medium;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	border: none;\n"
"	border-bottom: 1px solid #cccccc;\n"
"\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"	border-bottom: 1px solid #34495e;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border: 2px solid #34495e;\n"
"    border-radius: 5px;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2c3e50;\n"
"    border-color: #2c3e50;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #22313f;\n"
"    border-color: #22313f;\n"
"}\n"
"\n"
"\n"
"")
        self.gridLayout_2 = QGridLayout(AddItemPopup)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget = QWidget(AddItemPopup)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(6)
        self.main_layout.setObjectName(u"main_layout")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, -1, -1, 16)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.category_comboBox = QComboBox(self.widget)
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.addItem("")
        self.category_comboBox.setObjectName(u"category_comboBox")
        self.category_comboBox.setMinimumSize(QSize(460, 35))
        font1 = QFont()
        font1.setPointSize(12)
        self.category_comboBox.setFont(font1)

        self.verticalLayout_3.addWidget(self.category_comboBox)


        self.verticalLayout_10.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.item_name_label = QLabel(self.widget)
        self.item_name_label.setObjectName(u"item_name_label")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        font2.setBold(False)
        self.item_name_label.setFont(font2)

        self.verticalLayout.addWidget(self.item_name_label)

        self.item_name_lineEdit = QLineEdit(self.widget)
        self.item_name_lineEdit.setObjectName(u"item_name_lineEdit")
        self.item_name_lineEdit.setMinimumSize(QSize(450, 35))
        self.item_name_lineEdit.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(14)
        self.item_name_lineEdit.setFont(font3)

        self.verticalLayout.addWidget(self.item_name_lineEdit)


        self.verticalLayout_10.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.barcode_label = QLabel(self.widget)
        self.barcode_label.setObjectName(u"barcode_label")

        self.verticalLayout_2.addWidget(self.barcode_label)

        self.barcode_lineEdit = QLineEdit(self.widget)
        self.barcode_lineEdit.setObjectName(u"barcode_lineEdit")
        self.barcode_lineEdit.setMinimumSize(QSize(460, 35))
        self.barcode_lineEdit.setFont(font3)

        self.verticalLayout_2.addWidget(self.barcode_lineEdit)


        self.verticalLayout_10.addLayout(self.verticalLayout_2)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.batch_no_label = QLabel(self.widget)
        self.batch_no_label.setObjectName(u"batch_no_label")

        self.verticalLayout_9.addWidget(self.batch_no_label)

        self.batch_no_lineEdit = QLineEdit(self.widget)
        self.batch_no_lineEdit.setObjectName(u"batch_no_lineEdit")
        self.batch_no_lineEdit.setMinimumSize(QSize(460, 35))
        self.batch_no_lineEdit.setFont(font3)

        self.verticalLayout_9.addWidget(self.batch_no_lineEdit)


        self.verticalLayout_10.addLayout(self.verticalLayout_9)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.quantity_label = QLabel(self.widget)
        self.quantity_label.setObjectName(u"quantity_label")

        self.verticalLayout_4.addWidget(self.quantity_label)

        self.quantity_spinBox = QSpinBox(self.widget)
        self.quantity_spinBox.setObjectName(u"quantity_spinBox")
        self.quantity_spinBox.setMinimumSize(QSize(460, 30))
        self.quantity_spinBox.setFont(font3)

        self.verticalLayout_4.addWidget(self.quantity_spinBox)


        self.verticalLayout_10.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.minimum_stock_label = QLabel(self.widget)
        self.minimum_stock_label.setObjectName(u"minimum_stock_label")

        self.verticalLayout_5.addWidget(self.minimum_stock_label)

        self.minimum_stock_spinBox = QSpinBox(self.widget)
        self.minimum_stock_spinBox.setObjectName(u"minimum_stock_spinBox")
        self.minimum_stock_spinBox.setMinimumSize(QSize(460, 30))
        self.minimum_stock_spinBox.setFont(font3)

        self.verticalLayout_5.addWidget(self.minimum_stock_spinBox)


        self.verticalLayout_10.addLayout(self.verticalLayout_5)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.cost_label = QLabel(self.widget)
        self.cost_label.setObjectName(u"cost_label")

        self.verticalLayout_7.addWidget(self.cost_label)

        self.cost_doubleSpinBox = QDoubleSpinBox(self.widget)
        self.cost_doubleSpinBox.setObjectName(u"cost_doubleSpinBox")
        self.cost_doubleSpinBox.setMinimumSize(QSize(460, 30))
        self.cost_doubleSpinBox.setFont(font3)

        self.verticalLayout_7.addWidget(self.cost_doubleSpinBox)


        self.verticalLayout_10.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.price_label = QLabel(self.widget)
        self.price_label.setObjectName(u"price_label")

        self.verticalLayout_8.addWidget(self.price_label)

        self.price_doubleSpinBox = QDoubleSpinBox(self.widget)
        self.price_doubleSpinBox.setObjectName(u"price_doubleSpinBox")
        self.price_doubleSpinBox.setMinimumSize(QSize(460, 30))
        self.price_doubleSpinBox.setFont(font3)

        self.verticalLayout_8.addWidget(self.price_doubleSpinBox)


        self.verticalLayout_10.addLayout(self.verticalLayout_8)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.expiry_date_label = QLabel(self.widget)
        self.expiry_date_label.setObjectName(u"expiry_date_label")

        self.verticalLayout_6.addWidget(self.expiry_date_label)

        self.expiry_dateEdit = QDateEdit(self.widget)
        self.expiry_dateEdit.setObjectName(u"expiry_dateEdit")
        self.expiry_dateEdit.setMinimumSize(QSize(460, 30))
        self.expiry_dateEdit.setFont(font3)
        self.expiry_dateEdit.setDateTime(QDateTime(QDate(2024, 12, 27), QTime(0, 0, 0)))
        self.expiry_dateEdit.setCalendarPopup(True)

        self.verticalLayout_6.addWidget(self.expiry_dateEdit)


        self.verticalLayout_10.addLayout(self.verticalLayout_6)


        self.main_layout.addLayout(self.verticalLayout_10)

        self.add_item_btn = QPushButton(self.widget)
        self.add_item_btn.setObjectName(u"add_item_btn")
        self.add_item_btn.setMinimumSize(QSize(460, 45))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.add_item_btn.setFont(font4)

        self.main_layout.addWidget(self.add_item_btn)


        self.gridLayout.addLayout(self.main_layout, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(8, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(AddItemPopup)

        QMetaObject.connectSlotsByName(AddItemPopup)
    # setupUi

    def retranslateUi(self, AddItemPopup):
        AddItemPopup.setWindowTitle(QCoreApplication.translate("AddItemPopup", u"Add New Item", None))
        self.label.setText(QCoreApplication.translate("AddItemPopup", u"Category:", None))
        self.category_comboBox.setItemText(0, QCoreApplication.translate("AddItemPopup", u"Dairy", None))
        self.category_comboBox.setItemText(1, QCoreApplication.translate("AddItemPopup", u"Bakery", None))
        self.category_comboBox.setItemText(2, QCoreApplication.translate("AddItemPopup", u"Meat", None))
        self.category_comboBox.setItemText(3, QCoreApplication.translate("AddItemPopup", u"Produce", None))
        self.category_comboBox.setItemText(4, QCoreApplication.translate("AddItemPopup", u"Frozen Foods", None))
        self.category_comboBox.setItemText(5, QCoreApplication.translate("AddItemPopup", u"Beverages", None))
        self.category_comboBox.setItemText(6, QCoreApplication.translate("AddItemPopup", u"Snacks", None))
        self.category_comboBox.setItemText(7, QCoreApplication.translate("AddItemPopup", u"Household", None))
        self.category_comboBox.setItemText(8, QCoreApplication.translate("AddItemPopup", u"Personal Care", None))
        self.category_comboBox.setItemText(9, QCoreApplication.translate("AddItemPopup", u"Health Care", None))
        self.category_comboBox.setItemText(10, QCoreApplication.translate("AddItemPopup", u"Baby Products", None))
        self.category_comboBox.setItemText(11, QCoreApplication.translate("AddItemPopup", u"Pet Supplies", None))
        self.category_comboBox.setItemText(12, QCoreApplication.translate("AddItemPopup", u"Electronics", None))
        self.category_comboBox.setItemText(13, QCoreApplication.translate("AddItemPopup", u"Clothing", None))
        self.category_comboBox.setItemText(14, QCoreApplication.translate("AddItemPopup", u"Stationery", None))
        self.category_comboBox.setItemText(15, QCoreApplication.translate("AddItemPopup", u"Garden", None))
        self.category_comboBox.setItemText(16, QCoreApplication.translate("AddItemPopup", u"Automotive", None))
        self.category_comboBox.setItemText(17, QCoreApplication.translate("AddItemPopup", u"Toys", None))
        self.category_comboBox.setItemText(18, QCoreApplication.translate("AddItemPopup", u"Kitchenware", None))
        self.category_comboBox.setItemText(19, QCoreApplication.translate("AddItemPopup", u"Cleaning Supplies", None))
        self.category_comboBox.setItemText(20, QCoreApplication.translate("AddItemPopup", u"Paper Products", None))
        self.category_comboBox.setItemText(21, QCoreApplication.translate("AddItemPopup", u"Confectionery", None))
        self.category_comboBox.setItemText(22, QCoreApplication.translate("AddItemPopup", u"Seafood", None))
        self.category_comboBox.setItemText(23, QCoreApplication.translate("AddItemPopup", u"Breakfast Foods", None))
        self.category_comboBox.setItemText(24, QCoreApplication.translate("AddItemPopup", u"Spices", None))
        self.category_comboBox.setItemText(25, QCoreApplication.translate("AddItemPopup", u"Grains", None))
        self.category_comboBox.setItemText(26, QCoreApplication.translate("AddItemPopup", u"Oils", None))
        self.category_comboBox.setItemText(27, QCoreApplication.translate("AddItemPopup", u"Canned Goods", None))

        self.category_comboBox.setCurrentText("")
        self.category_comboBox.setPlaceholderText(QCoreApplication.translate("AddItemPopup", u"Select a category", None))
        self.item_name_label.setText(QCoreApplication.translate("AddItemPopup", u"Item Name:", None))
        self.barcode_label.setText(QCoreApplication.translate("AddItemPopup", u"Barcode (EAN-13):", None))
        self.batch_no_label.setText(QCoreApplication.translate("AddItemPopup", u"Batch Number:", None))
        self.quantity_label.setText(QCoreApplication.translate("AddItemPopup", u"Quantity:", None))
        self.minimum_stock_label.setText(QCoreApplication.translate("AddItemPopup", u"Minimum Stock:", None))
        self.cost_label.setText(QCoreApplication.translate("AddItemPopup", u"Cost Per Unit:", None))
        self.cost_doubleSpinBox.setPrefix(QCoreApplication.translate("AddItemPopup", u"$ ", None))
        self.cost_doubleSpinBox.setSuffix("")
        self.price_label.setText(QCoreApplication.translate("AddItemPopup", u"Price Per Unit:", None))
        self.price_doubleSpinBox.setPrefix(QCoreApplication.translate("AddItemPopup", u"$ ", None))
        self.price_doubleSpinBox.setSuffix("")
        self.expiry_date_label.setText(QCoreApplication.translate("AddItemPopup", u"Expiry Date (DD/MM/YYYY):", None))
        self.expiry_dateEdit.setDisplayFormat(QCoreApplication.translate("AddItemPopup", u"dd/MM/yyyy", None))
        self.add_item_btn.setText(QCoreApplication.translate("AddItemPopup", u"Add Item", None))
    # retranslateUi

