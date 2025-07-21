# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainaQSTGP.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1184, 862)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"#MainWindow {\n"
"	background-color: #F5F7F9\n"
"}\n"
"\n"
"QPushButton#menu_btn:hover,\n"
"QPushButton#account_btn:hover {\n"
"    background-color: #e0e3e5;\n"
"    border-color: #bfc2c4;\n"
"}\n"
"\n"
"QPushButton#menu_btn:pressed,\n"
"QPushButton#account_btn:pressed {\n"
"    background-color: #cfd2d4;\n"
"    border-color: #aeb1b2;\n"
"}\n"
"\n"
"\n"
"#top_widget {\n"
"	background-color: #F5F7F9\n"
"}\n"
"\n"
"\n"
"#logo {\n"
"		padding: 3px;\n"
"		color: #F5F1E9;\n"
"}\n"
"\n"
"\n"
"#account_btn {\n"
"		border: none;\n"
"	}\n"
"\n"
"#MainWindow  QPushButton{\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border: 2px solid #34495e;\n"
"    border-radius: 5px;\n"
"	font-family: \"Segoe UI\";\n"
"	font-weight: 600;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#MainWindow  QPushButton:hover {\n"
"    background-color: #2c3e50;\n"
"    border-color: #2c3e50;\n"
"}\n"
"\n"
"#MainWindow  QPushButton:pressed {\n"
"    background-color: #22313f;\n"
"    border-color: #22313f;\n"
"}\n"
"\n"
"\n"
"QPus"
                        "hButton#delete_item_btn, \n"
"QPushButton#delete_user_btn,\n"
"QPushButton#remove_item_btn,\n"
"QPushButton#cancel_sale_btn,\n"
"QPushButton#delete_record_btn {\n"
"    background-color: #b03a2e; \n"
"    color: white;\n"
"    border: 2px solid #b03a2e;\n"
"    border-radius: 5px;\n"
"	font-family: \"Segoe UI\";\n"
"	font-weight: 600;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"QPushButton#delete_item_btn:hover, \n"
"QPushButton#delete_user_btn:hover,\n"
"QPushButton#remove_item_btn:hover,\n"
"QPushButton#cancel_sale_btn:hover,\n"
"QPushButton#delete_record_btn:hover{\n"
"    background-color: #8c2f24;  \n"
"    border-color: #8c2f24;\n"
"}\n"
"\n"
"QPushButton#delete_item_btn:pressed, \n"
"QPushButton#delete_user_btn:pressed,\n"
"QPushButton#remove_item_btn:pressed,\n"
" QPushButton#cancel_sale_btn:pressed,\n"
"QPushButton#delete_record_btn:pressed{\n"
"    background-color: #6f241c;\n"
"    border-color: #6f241c;\n"
"}\n"
"\n"
"\n"
"#info_widget {\n"
"    background-color: #34495e;\n"
"    border-radius: 5px;\n"
""
                        "    border: 2px solid #2c3e50;\n"
"}\n"
"\n"
"#header_widget QWidget,\n"
"#header_widget_2 QWidget {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border: 2px solid #34495e;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	border: 1px solid #34495e;\n"
"	background: #F5F7F9;\n"
"	padding: 6px 8px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton#checkout_btn_2 {\n"
"    background-color: #2a5d9f;\n"
"    color: white;\n"
"    border: 2px solid #2a5d9f;\n"
"    border-radius: 5px;\n"
"    font-family: \"Segoe UI\";\n"
"    font-weight: 600;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"QPushButton#checkout_btn_2:hover {\n"
"    background-color: #234e86;\n"
"    border-color: #234e86;\n"
"}\n"
"\n"
"QPushButton#checkout_btn_2:pressed {\n"
"    background-color: #1c3e6c;\n"
"    border-color: #1c3e6c;\n"
"}\n"
"\n"
"QLabel#total_lbl {\n"
"	color: #F5F7F9;;\n"
"}\n"
"\n"
"#total_widget,\n"
"#change_due_widget {\n"
"	border: 2px solid #F5F7F9;\n"
"	border-radius: 5px\n"
"}\n"
"\n"
"\n"
""
                        "QTabWidget::pane {\n"
"    border: 2px solid #22313f;\n"
"    top: -1px;\n"
"}\n"
"\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    border: 2px solid #34495e;\n"
"    border-bottom: none;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"    padding: 12px 60px; \n"
"    font-family: \"Segoe UI\";\n"
"    font-weight: 600;\n"
"    font-size: 13pt; \n"
"    margin-right: 6px;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #2c3e50;\n"
"    border-color: #2c3e50;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #22313f;\n"
"    border: 2px solid #22313f;\n"
"    border-bottom: none;\n"
"    color: white;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 2px solid #22313f;\n"
"    top: -1px;\n"
"}\n"
"\n"
"QPushButton#menu_btn,\n"
"QPushButton#account_btn {\n"
"    background-color: #F5F7F9;\n"
"    color: black;\n"
"	border: none;\n"
"    border-radius: 5px;\n"
"    font-family: \"Segoe UI\";\n"
"    font-weight: 6"
                        "00;\n"
"    font-size: 11pt;\n"
"    padding: 5px;\n"
"    width: 30px;\n"
"    height: 30px;\n"
"}\n"
"\n"
"QPushButton#menu_btn:hover,\n"
"QPushButton#account_btn:hover {\n"
"    background-color: #e0e3e5;\n"
"    border-color: #bfc2c4;\n"
"}\n"
"\n"
"QPushButton#menu_btn:pressed,\n"
"QPushButton#account_btn:pressed {\n"
"    background-color: #cfd2d4;\n"
"    border-color: #aeb1b2;\n"
"}\n"
"\n"
"#sidebar {\n"
"	background-color: #34495e;\n"
"	width: 60px;\n"
"}\n"
"\n"
"#sidebar QPushButton, QLabel {\n"
"		height:55px;\n"
"		border:none;\n"
"	}\n"
"\n"
"#sidebar QPushButton {\n"
"		color: #F9E79F;\n"
"		font-size: 13pt;\n"
"}\n"
"\n"
"#sidebar QPushButton:hover {\n"
"		background-color: rgba( 86, 101, 115, 0.5);\n"
"		border-top-left-radius: 5px;\n"
"   		border-bottom-left-radius: 5px;\n"
"   		border-top-right-radius: 0px;\n"
"    	border-bottom-right-radius: 0px\n"
"	}\n"
"\n"
"#sidebar QPushButton:checked {\n"
"		background-color: #F5F7F9;\n"
"    	color: #34495e;\n"
"    	border-top-left-radius: 5px;\n"
""
                        "   		border-bottom-left-radius: 5px;\n"
"   		border-top-right-radius: 0px;\n"
"    	border-bottom-right-radius: 0px\n"
"	}\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pages_widget = QWidget(self.centralwidget)
        self.pages_widget.setObjectName(u"pages_widget")
        self.pages_widget.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.pages_widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.top_widget = QWidget(self.pages_widget)
        self.top_widget.setObjectName(u"top_widget")
        self.top_widget.setMinimumSize(QSize(0, 0))
        self.top_widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.top_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.menu_btn = QPushButton(self.top_widget)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setMinimumSize(QSize(45, 45))
        self.menu_btn.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/menu_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/menu_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.menu_btn.setIcon(icon1)
        self.menu_btn.setIconSize(QSize(25, 25))
        self.menu_btn.setCheckable(True)

        self.horizontalLayout.addWidget(self.menu_btn)

        self.horizontalSpacer = QSpacerItem(851, 18, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.account_btn = QPushButton(self.top_widget)
        self.account_btn.setObjectName(u"account_btn")
        self.account_btn.setMinimumSize(QSize(45, 45))
        icon2 = QIcon()
        icon2.addFile(u":/icons/account_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/account_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.account_btn.setIcon(icon2)
        self.account_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.account_btn)


        self.verticalLayout_7.addWidget(self.top_widget)

        self.stackedWidget = QStackedWidget(self.pages_widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.checkout_page = QWidget()
        self.checkout_page.setObjectName(u"checkout_page")
        self.checkout_page.setStyleSheet(u"")
        self.gridLayout_16 = QGridLayout(self.checkout_page)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(2, 40, 2, 16)
        self.middle_layout_2 = QVBoxLayout()
        self.middle_layout_2.setObjectName(u"middle_layout_2")
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.barcode_lineEdit = QLineEdit(self.checkout_page)
        self.barcode_lineEdit.setObjectName(u"barcode_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.barcode_lineEdit.sizePolicy().hasHeightForWidth())
        self.barcode_lineEdit.setSizePolicy(sizePolicy)
        self.barcode_lineEdit.setMinimumSize(QSize(310, 44))
        font1 = QFont()
        font1.setPointSize(14)
        self.barcode_lineEdit.setFont(font1)

        self.horizontalLayout_14.addWidget(self.barcode_lineEdit)

        self.checkout_add_item = QPushButton(self.checkout_page)
        self.checkout_add_item.setObjectName(u"checkout_add_item")
        self.checkout_add_item.setMinimumSize(QSize(140, 44))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        font2.setWeight(QFont.DemiBold)
        self.checkout_add_item.setFont(font2)

        self.horizontalLayout_14.addWidget(self.checkout_add_item)


        self.top_layout.addLayout(self.horizontalLayout_14)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.top_layout.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.cancel_sale_btn = QPushButton(self.checkout_page)
        self.cancel_sale_btn.setObjectName(u"cancel_sale_btn")
        self.cancel_sale_btn.setMinimumSize(QSize(140, 44))
        self.cancel_sale_btn.setFont(font2)

        self.horizontalLayout_13.addWidget(self.cancel_sale_btn)


        self.top_layout.addLayout(self.horizontalLayout_13)


        self.middle_layout_2.addLayout(self.top_layout)

        self.checkout_table = QTableWidget(self.checkout_page)
        if (self.checkout_table.columnCount() < 7):
            self.checkout_table.setColumnCount(7)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setWeight(QFont.DemiBold)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font2);
        __qtablewidgetitem1.setBackground(QColor(255, 255, 255));
        self.checkout_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font3);
        self.checkout_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.checkout_table.setObjectName(u"checkout_table")
        self.checkout_table.setMinimumSize(QSize(800, 400))
        font4 = QFont()
        font4.setPointSize(18)
        font4.setBold(False)
        self.checkout_table.setFont(font4)
        self.checkout_table.horizontalHeader().setMinimumSectionSize(100)
        self.checkout_table.verticalHeader().setVisible(True)
        self.checkout_table.verticalHeader().setMinimumSectionSize(30)

        self.middle_layout_2.addWidget(self.checkout_table)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.increase_item_btn = QPushButton(self.checkout_page)
        self.increase_item_btn.setObjectName(u"increase_item_btn")
        self.increase_item_btn.setMinimumSize(QSize(50, 30))
        self.increase_item_btn.setFont(font2)
        icon3 = QIcon()
        icon3.addFile(u":/icons/add_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.increase_item_btn.setIcon(icon3)
        self.increase_item_btn.setIconSize(QSize(23, 23))

        self.bottom_layout.addWidget(self.increase_item_btn)

        self.decrease_item_btn = QPushButton(self.checkout_page)
        self.decrease_item_btn.setObjectName(u"decrease_item_btn")
        self.decrease_item_btn.setMinimumSize(QSize(50, 30))
        self.decrease_item_btn.setFont(font2)
        icon4 = QIcon()
        icon4.addFile(u":/icons/subtract_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.decrease_item_btn.setIcon(icon4)
        self.decrease_item_btn.setIconSize(QSize(25, 25))

        self.bottom_layout.addWidget(self.decrease_item_btn)

        self.set_quantity_btn = QPushButton(self.checkout_page)
        self.set_quantity_btn.setObjectName(u"set_quantity_btn")
        self.set_quantity_btn.setMinimumSize(QSize(120, 30))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(11)
        font5.setWeight(QFont.DemiBold)
        self.set_quantity_btn.setFont(font5)
        self.set_quantity_btn.setStyleSheet(u" font-size: 11pt;")

        self.bottom_layout.addWidget(self.set_quantity_btn)

        self.apply_discount_btn = QPushButton(self.checkout_page)
        self.apply_discount_btn.setObjectName(u"apply_discount_btn")
        self.apply_discount_btn.setMinimumSize(QSize(120, 30))
        self.apply_discount_btn.setStyleSheet(u" font-size: 11pt;")

        self.bottom_layout.addWidget(self.apply_discount_btn)

        self.add_free_unit_btn = QPushButton(self.checkout_page)
        self.add_free_unit_btn.setObjectName(u"add_free_unit_btn")
        self.add_free_unit_btn.setMinimumSize(QSize(120, 30))
        self.add_free_unit_btn.setFont(font5)
        self.add_free_unit_btn.setStyleSheet(u" font-size: 11pt;")

        self.bottom_layout.addWidget(self.add_free_unit_btn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_layout.addItem(self.horizontalSpacer_5)

        self.remove_item_btn = QPushButton(self.checkout_page)
        self.remove_item_btn.setObjectName(u"remove_item_btn")
        self.remove_item_btn.setMinimumSize(QSize(50, 30))
        self.remove_item_btn.setFont(font2)
        icon5 = QIcon()
        icon5.addFile(u":/icons/close_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.remove_item_btn.setIcon(icon5)
        self.remove_item_btn.setIconSize(QSize(30, 30))

        self.bottom_layout.addWidget(self.remove_item_btn)


        self.middle_layout_2.addLayout(self.bottom_layout)


        self.main_layout.addLayout(self.middle_layout_2)

        self.side_layout = QVBoxLayout()
        self.side_layout.setObjectName(u"side_layout")
        self.side_layout.setContentsMargins(2, 49, -1, 48)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")

        self.side_layout.addLayout(self.verticalLayout_10)

        self.info_widget = QWidget(self.checkout_page)
        self.info_widget.setObjectName(u"info_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.info_widget.sizePolicy().hasHeightForWidth())
        self.info_widget.setSizePolicy(sizePolicy1)
        self.verticalLayout_21 = QVBoxLayout(self.info_widget)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 26)
        self.total_layout = QVBoxLayout()
        self.total_layout.setSpacing(6)
        self.total_layout.setObjectName(u"total_layout")
        self.total_layout.setContentsMargins(40, 15, 40, -1)
        self.label = QLabel(self.info_widget)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setPointSize(20)
        font6.setWeight(QFont.DemiBold)
        self.label.setFont(font6)
        self.label.setStyleSheet(u"color: #F5F7F9;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.total_layout.addWidget(self.label)

        self.total_widget = QWidget(self.info_widget)
        self.total_widget.setObjectName(u"total_widget")
        self.total_widget.setMinimumSize(QSize(150, 50))
        self.total_widget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_17 = QGridLayout(self.total_widget)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.total_lbl = QLabel(self.total_widget)
        self.total_lbl.setObjectName(u"total_lbl")
        font7 = QFont()
        font7.setFamilies([u"Segoe UI"])
        font7.setPointSize(22)
        font7.setBold(True)
        self.total_lbl.setFont(font7)
        self.total_lbl.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.total_lbl, 0, 0, 1, 1)


        self.total_layout.addWidget(self.total_widget)


        self.verticalLayout_21.addLayout(self.total_layout)

        self.cash_received_layout = QVBoxLayout()
        self.cash_received_layout.setSpacing(6)
        self.cash_received_layout.setObjectName(u"cash_received_layout")
        self.cash_received_layout.setContentsMargins(40, 14, 40, -1)
        self.label_2 = QLabel(self.info_widget)
        self.label_2.setObjectName(u"label_2")
        font8 = QFont()
        font8.setFamilies([u"Segoe UI"])
        font8.setPointSize(16)
        font8.setWeight(QFont.DemiBold)
        self.label_2.setFont(font8)
        self.label_2.setStyleSheet(u"color: #F5F7F9;")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.cash_received_layout.addWidget(self.label_2)

        self.cash_received_lineEdit = QLineEdit(self.info_widget)
        self.cash_received_lineEdit.setObjectName(u"cash_received_lineEdit")
        sizePolicy1.setHeightForWidth(self.cash_received_lineEdit.sizePolicy().hasHeightForWidth())
        self.cash_received_lineEdit.setSizePolicy(sizePolicy1)
        self.cash_received_lineEdit.setMinimumSize(QSize(150, 60))
        font9 = QFont()
        font9.setPointSize(18)
        self.cash_received_lineEdit.setFont(font9)
        self.cash_received_lineEdit.setStyleSheet(u"border: 2px solid #34495e;\n"
"border-radius: 5px;\n"
"background-color: #F5F7F9;")
        self.cash_received_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cash_received_layout.addWidget(self.cash_received_lineEdit)


        self.verticalLayout_21.addLayout(self.cash_received_layout)

        self.change_due_layout = QVBoxLayout()
        self.change_due_layout.setSpacing(6)
        self.change_due_layout.setObjectName(u"change_due_layout")
        self.change_due_layout.setContentsMargins(40, 15, 40, -1)
        self.label_4 = QLabel(self.info_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font8)
        self.label_4.setStyleSheet(u"color:#F5F7F9")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.change_due_layout.addWidget(self.label_4)

        self.change_due_widget = QWidget(self.info_widget)
        self.change_due_widget.setObjectName(u"change_due_widget")
        self.change_due_widget.setMinimumSize(QSize(150, 50))
        self.gridLayout_18 = QGridLayout(self.change_due_widget)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.change_due_lbl = QLabel(self.change_due_widget)
        self.change_due_lbl.setObjectName(u"change_due_lbl")
        self.change_due_lbl.setFont(font7)
        self.change_due_lbl.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.change_due_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.change_due_lbl, 0, 0, 1, 1)


        self.change_due_layout.addWidget(self.change_due_widget)


        self.verticalLayout_21.addLayout(self.change_due_layout)


        self.side_layout.addWidget(self.info_widget)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.side_layout.addItem(self.verticalSpacer_2)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setSpacing(12)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.cash_btn = QPushButton(self.checkout_page)
        self.cash_btn.setObjectName(u"cash_btn")
        self.cash_btn.setMinimumSize(QSize(120, 44))
        self.cash_btn.setFont(font2)
        self.cash_btn.setStyleSheet(u"# Define the grayscale (disabled) look\n"
"disabled_button_style = \"\"\"\n"
"background-color: #e0e0e0;\n"
"color: #7f8c8d;\n"
"border: 2px solid #bdc3c7;\n"
"border-radius: 5px;\n"
"font-family: \"Segoe UI\";\n"
"font-weight: 600;\n"
"font-size: 12pt;\n"
"\"\"\"")

        self.horizontalLayout_8.addWidget(self.cash_btn)

        self.card_btn = QPushButton(self.checkout_page)
        self.card_btn.setObjectName(u"card_btn")
        self.card_btn.setMinimumSize(QSize(120, 44))
        self.card_btn.setFont(font2)
        self.card_btn.setStyleSheet(u"# Define the grayscale (disabled) look\n"
"disabled_button_style = \"\"\"\n"
"background-color: #e0e0e0;\n"
"color: #7f8c8d;\n"
"border: 2px solid #bdc3c7;\n"
"border-radius: 5px;\n"
"font-family: \"Segoe UI\";\n"
"font-weight: 600;\n"
"font-size: 12pt;\n"
"\"\"\"")

        self.horizontalLayout_8.addWidget(self.card_btn)


        self.verticalLayout_15.addLayout(self.horizontalLayout_8)

        self.checkout_btn_2 = QPushButton(self.checkout_page)
        self.checkout_btn_2.setObjectName(u"checkout_btn_2")
        self.checkout_btn_2.setMinimumSize(QSize(150, 50))
        self.checkout_btn_2.setFont(font2)

        self.verticalLayout_15.addWidget(self.checkout_btn_2)


        self.side_layout.addLayout(self.verticalLayout_15)


        self.main_layout.addLayout(self.side_layout)


        self.gridLayout_16.addLayout(self.main_layout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.checkout_page)
        self.inventory_page = QWidget()
        self.inventory_page.setObjectName(u"inventory_page")
        self.gridLayout_10 = QGridLayout(self.inventory_page)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(30)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(-1, 26, -1, 5)
        self.header_widget = QWidget(self.inventory_page)
        self.header_widget.setObjectName(u"header_widget")
        self.horizontalLayout_6 = QHBoxLayout(self.header_widget)
        self.horizontalLayout_6.setSpacing(14)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.widget_5 = QWidget(self.header_widget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(150, 100))
        self.gridLayout_4 = QGridLayout(self.widget_5)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 20, 5, 20)
        self.current_stock_header_lbl_3 = QLabel(self.widget_5)
        self.current_stock_header_lbl_3.setObjectName(u"current_stock_header_lbl_3")
        self.current_stock_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.current_stock_header_lbl_3.setMaximumSize(QSize(16777215, 16777215))
        font10 = QFont()
        font10.setPointSize(13)
        font10.setBold(True)
        self.current_stock_header_lbl_3.setFont(font10)
        self.current_stock_header_lbl_3.setStyleSheet(u"")
        self.current_stock_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.current_stock_header_lbl_3)

        self.total_items_lbl = QLabel(self.widget_5)
        self.total_items_lbl.setObjectName(u"total_items_lbl")
        self.total_items_lbl.setMinimumSize(QSize(140, 20))
        self.total_items_lbl.setMaximumSize(QSize(16777215, 16777215))
        font11 = QFont()
        font11.setPointSize(12)
        font11.setBold(True)
        font11.setItalic(False)
        font11.setUnderline(False)
        self.total_items_lbl.setFont(font11)
        self.total_items_lbl.setStyleSheet(u"color: #F9E79F	")
        self.total_items_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.total_items_lbl)


        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.header_widget)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMinimumSize(QSize(150, 100))
        self.gridLayout_14 = QGridLayout(self.widget_6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 20, 5, 20)
        self.reorder_header_lbl_3 = QLabel(self.widget_6)
        self.reorder_header_lbl_3.setObjectName(u"reorder_header_lbl_3")
        self.reorder_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.reorder_header_lbl_3.setFont(font10)
        self.reorder_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.reorder_header_lbl_3)

        self.low_stock_lbl = QLabel(self.widget_6)
        self.low_stock_lbl.setObjectName(u"low_stock_lbl")
        self.low_stock_lbl.setMinimumSize(QSize(140, 20))
        font12 = QFont()
        font12.setPointSize(12)
        font12.setBold(True)
        self.low_stock_lbl.setFont(font12)
        self.low_stock_lbl.setStyleSheet(u"color: #F9E79F")
        self.low_stock_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.low_stock_lbl)


        self.gridLayout_14.addLayout(self.verticalLayout_9, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_6)

        self.widget_4 = QWidget(self.header_widget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(150, 100))
        self.gridLayout_8 = QGridLayout(self.widget_4)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(5, 20, 5, 20)
        self.out_of_stock_header_lbl_3 = QLabel(self.widget_4)
        self.out_of_stock_header_lbl_3.setObjectName(u"out_of_stock_header_lbl_3")
        self.out_of_stock_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.out_of_stock_header_lbl_3.setFont(font10)
        self.out_of_stock_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.out_of_stock_header_lbl_3)

        self.out_of_stock_lb = QLabel(self.widget_4)
        self.out_of_stock_lb.setObjectName(u"out_of_stock_lb")
        self.out_of_stock_lb.setMinimumSize(QSize(140, 20))
        self.out_of_stock_lb.setFont(font12)
        self.out_of_stock_lb.setStyleSheet(u"color: #F9E79F")
        self.out_of_stock_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.out_of_stock_lb)


        self.gridLayout_8.addLayout(self.verticalLayout_11, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_4)

        self.widget_7 = QWidget(self.header_widget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(150, 100))
        self.gridLayout_9 = QGridLayout(self.widget_7)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(5, 20, 5, 20)
        self.expired_header_lbl_3 = QLabel(self.widget_7)
        self.expired_header_lbl_3.setObjectName(u"expired_header_lbl_3")
        self.expired_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.expired_header_lbl_3.setFont(font10)
        self.expired_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.expired_header_lbl_3)

        self.expired_lbl = QLabel(self.widget_7)
        self.expired_lbl.setObjectName(u"expired_lbl")
        self.expired_lbl.setMinimumSize(QSize(140, 20))
        self.expired_lbl.setFont(font12)
        self.expired_lbl.setStyleSheet(u"color: #F9E79F")
        self.expired_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.expired_lbl)


        self.gridLayout_9.addLayout(self.verticalLayout_12, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_7)

        self.widget_2 = QWidget(self.header_widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(150, 100))
        self.gridLayout_6 = QGridLayout(self.widget_2)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 20, 5, 20)
        self.stock_header_lbl_3 = QLabel(self.widget_2)
        self.stock_header_lbl_3.setObjectName(u"stock_header_lbl_3")
        self.stock_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.stock_header_lbl_3.setMaximumSize(QSize(16777215, 16777215))
        self.stock_header_lbl_3.setFont(font10)
        self.stock_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.stock_header_lbl_3)

        self.stock_value_lbl = QLabel(self.widget_2)
        self.stock_value_lbl.setObjectName(u"stock_value_lbl")
        self.stock_value_lbl.setMinimumSize(QSize(140, 20))
        font13 = QFont()
        font13.setPointSize(12)
        font13.setBold(True)
        font13.setItalic(False)
        self.stock_value_lbl.setFont(font13)
        self.stock_value_lbl.setStyleSheet(u"color: #F9E79F")
        self.stock_value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.stock_value_lbl)


        self.gridLayout_6.addLayout(self.verticalLayout_6, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.header_widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(150, 100))
        self.gridLayout_7 = QGridLayout(self.widget_3)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, 20, 5, 20)
        self.stock_cost_header_lbl_3 = QLabel(self.widget_3)
        self.stock_cost_header_lbl_3.setObjectName(u"stock_cost_header_lbl_3")
        self.stock_cost_header_lbl_3.setMinimumSize(QSize(140, 20))
        self.stock_cost_header_lbl_3.setFont(font10)
        self.stock_cost_header_lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.stock_cost_header_lbl_3)

        self.stock_cost_lbl = QLabel(self.widget_3)
        self.stock_cost_lbl.setObjectName(u"stock_cost_lbl")
        self.stock_cost_lbl.setMinimumSize(QSize(140, 20))
        self.stock_cost_lbl.setFont(font12)
        self.stock_cost_lbl.setStyleSheet(u"color: #F9E79F")
        self.stock_cost_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.stock_cost_lbl)


        self.gridLayout_7.addLayout(self.verticalLayout_8, 0, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.widget_3)


        self.verticalLayout_13.addWidget(self.header_widget)

        self.middle_layout = QVBoxLayout()
        self.middle_layout.setSpacing(8)
        self.middle_layout.setObjectName(u"middle_layout")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(10)
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_item_btn = QPushButton(self.inventory_page)
        self.add_item_btn.setObjectName(u"add_item_btn")
        self.add_item_btn.setMinimumSize(QSize(120, 44))
        self.add_item_btn.setFont(font2)

        self.buttons_layout.addWidget(self.add_item_btn)

        self.update_item_btn = QPushButton(self.inventory_page)
        self.update_item_btn.setObjectName(u"update_item_btn")
        self.update_item_btn.setMinimumSize(QSize(120, 44))

        self.buttons_layout.addWidget(self.update_item_btn)

        self.discount_item_btn = QPushButton(self.inventory_page)
        self.discount_item_btn.setObjectName(u"discount_item_btn")
        self.discount_item_btn.setMinimumSize(QSize(120, 44))

        self.buttons_layout.addWidget(self.discount_item_btn)

        self.horizontalSpacer_10 = QSpacerItem(150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.horizontalSpacer_10)

        self.delete_item_btn = QPushButton(self.inventory_page)
        self.delete_item_btn.setObjectName(u"delete_item_btn")
        self.delete_item_btn.setMinimumSize(QSize(120, 44))
        self.delete_item_btn.setFont(font2)

        self.buttons_layout.addWidget(self.delete_item_btn)


        self.middle_layout.addLayout(self.buttons_layout)

        self.inventory_table = QTableWidget(self.inventory_page)
        if (self.inventory_table.columnCount() < 14):
            self.inventory_table.setColumnCount(14)
        font14 = QFont()
        font14.setPointSize(11)
        font14.setWeight(QFont.DemiBold)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font5);
        __qtablewidgetitem8.setBackground(QColor(255, 255, 255));
        self.inventory_table.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font5);
        self.inventory_table.setHorizontalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font5);
        self.inventory_table.setHorizontalHeaderItem(3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font5);
        self.inventory_table.setHorizontalHeaderItem(4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(5, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(6, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(7, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(8, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(9, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(10, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(11, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(12, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font14);
        self.inventory_table.setHorizontalHeaderItem(13, __qtablewidgetitem20)
        self.inventory_table.setObjectName(u"inventory_table")
        self.inventory_table.setMinimumSize(QSize(1000, 400))
        font15 = QFont()
        font15.setPointSize(12)
        self.inventory_table.setFont(font15)
        self.inventory_table.horizontalHeader().setMinimumSectionSize(100)
        self.inventory_table.verticalHeader().setMinimumSectionSize(30)

        self.middle_layout.addWidget(self.inventory_table)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.item_search_lineEdit = QLineEdit(self.inventory_page)
        self.item_search_lineEdit.setObjectName(u"item_search_lineEdit")
        self.item_search_lineEdit.setMinimumSize(QSize(310, 40))
        self.item_search_lineEdit.setFont(font1)

        self.horizontalLayout_10.addWidget(self.item_search_lineEdit)

        self.clear_inventory_tb_btn = QPushButton(self.inventory_page)
        self.clear_inventory_tb_btn.setObjectName(u"clear_inventory_tb_btn")
        self.clear_inventory_tb_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_10.addWidget(self.clear_inventory_tb_btn)

        self.low_stock_btn = QPushButton(self.inventory_page)
        self.low_stock_btn.setObjectName(u"low_stock_btn")
        self.low_stock_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_10.addWidget(self.low_stock_btn)

        self.out_of_stock_btn = QPushButton(self.inventory_page)
        self.out_of_stock_btn.setObjectName(u"out_of_stock_btn")
        self.out_of_stock_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_10.addWidget(self.out_of_stock_btn)

        self.expired_btn = QPushButton(self.inventory_page)
        self.expired_btn.setObjectName(u"expired_btn")
        self.expired_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_10.addWidget(self.expired_btn)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)


        self.middle_layout.addLayout(self.horizontalLayout_9)


        self.verticalLayout_13.addLayout(self.middle_layout)


        self.gridLayout_10.addLayout(self.verticalLayout_13, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.inventory_page)
        self.reports_page = QWidget()
        self.reports_page.setObjectName(u"reports_page")
        self.gridLayout_5 = QGridLayout(self.reports_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, 35, -1, 10)
        self.reports_tab = QTabWidget(self.reports_page)
        self.reports_tab.setObjectName(u"reports_tab")
        self.reports_tab.setMinimumSize(QSize(110, 0))
        self.reports_tab.setFont(font1)
        self.reports_tab.setIconSize(QSize(16, 16))
        self.sales_history_tab = QWidget()
        self.sales_history_tab.setObjectName(u"sales_history_tab")
        self.gridLayout_20 = QGridLayout(self.sales_history_tab)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(4)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(6, 3, 4, -1)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setSpacing(6)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(5)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, -1, 6, -1)
        self.from_lbl = QLabel(self.sales_history_tab)
        self.from_lbl.setObjectName(u"from_lbl")
        font16 = QFont()
        font16.setPointSize(16)
        self.from_lbl.setFont(font16)

        self.horizontalLayout_16.addWidget(self.from_lbl)

        self.from_date = QDateEdit(self.sales_history_tab)
        self.from_date.setObjectName(u"from_date")
        self.from_date.setMinimumSize(QSize(130, 30))
        self.from_date.setFont(font1)
        self.from_date.setDateTime(QDateTime(QDate(2025, 1, 1), QTime(0, 0, 0)))
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate(2025, 1, 1))

        self.horizontalLayout_16.addWidget(self.from_date)


        self.horizontalLayout_18.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setSpacing(5)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, -1, 6, -1)
        self.to_lbl = QLabel(self.sales_history_tab)
        self.to_lbl.setObjectName(u"to_lbl")
        self.to_lbl.setFont(font16)

        self.horizontalLayout_17.addWidget(self.to_lbl)

        self.to_date = QDateEdit(self.sales_history_tab)
        self.to_date.setObjectName(u"to_date")
        self.to_date.setMinimumSize(QSize(130, 30))
        self.to_date.setFont(font1)
        self.to_date.setDateTime(QDateTime(QDate(2024, 12, 15), QTime(0, 0, 0)))
        self.to_date.setCalendarPopup(True)

        self.horizontalLayout_17.addWidget(self.to_date)


        self.horizontalLayout_18.addLayout(self.horizontalLayout_17)

        self.sales_history_reset_btn = QPushButton(self.sales_history_tab)
        self.sales_history_reset_btn.setObjectName(u"sales_history_reset_btn")
        self.sales_history_reset_btn.setMinimumSize(QSize(100, 35))

        self.horizontalLayout_18.addWidget(self.sales_history_reset_btn)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_18)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_6)


        self.gridLayout_20.addLayout(self.horizontalLayout_15, 0, 0, 1, 1)

        self.sales_history_table = QTableWidget(self.sales_history_tab)
        if (self.sales_history_table.columnCount() < 11):
            self.sales_history_table.setColumnCount(11)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(5, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(6, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(7, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(8, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(9, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setFont(font14);
        self.sales_history_table.setHorizontalHeaderItem(10, __qtablewidgetitem31)
        self.sales_history_table.setObjectName(u"sales_history_table")
        self.sales_history_table.setFont(font15)

        self.gridLayout_20.addWidget(self.sales_history_table, 1, 0, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(8)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.sales_search_lineEdit = QLineEdit(self.sales_history_tab)
        self.sales_search_lineEdit.setObjectName(u"sales_search_lineEdit")
        self.sales_search_lineEdit.setMinimumSize(QSize(310, 40))
        self.sales_search_lineEdit.setFont(font1)

        self.horizontalLayout_19.addWidget(self.sales_search_lineEdit)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setSpacing(4)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.clear_sales_tbl = QPushButton(self.sales_history_tab)
        self.clear_sales_tbl.setObjectName(u"clear_sales_tbl")
        self.clear_sales_tbl.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_20.addWidget(self.clear_sales_tbl)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_20)


        self.gridLayout_20.addLayout(self.horizontalLayout_19, 2, 0, 1, 1)

        self.reports_tab.addTab(self.sales_history_tab, "")
        self.sales_summary_tab = QWidget()
        self.sales_summary_tab.setObjectName(u"sales_summary_tab")
        self.gridLayout_19 = QGridLayout(self.sales_summary_tab)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(4)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(6, 14, 4, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.view_summary_lbl = QLabel(self.sales_summary_tab)
        self.view_summary_lbl.setObjectName(u"view_summary_lbl")
        self.view_summary_lbl.setFont(font16)

        self.horizontalLayout_11.addWidget(self.view_summary_lbl)

        self.filter_summary_comboBox = QComboBox(self.sales_summary_tab)
        self.filter_summary_comboBox.addItem("")
        self.filter_summary_comboBox.addItem("")
        self.filter_summary_comboBox.addItem("")
        self.filter_summary_comboBox.addItem("")
        self.filter_summary_comboBox.addItem("")
        self.filter_summary_comboBox.setObjectName(u"filter_summary_comboBox")
        self.filter_summary_comboBox.setMinimumSize(QSize(110, 0))
        self.filter_summary_comboBox.setFont(font16)

        self.horizontalLayout_11.addWidget(self.filter_summary_comboBox)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_4)


        self.verticalLayout_19.addLayout(self.horizontalLayout_12)

        self.sales_summary_table = QTableWidget(self.sales_summary_tab)
        if (self.sales_summary_table.columnCount() < 7):
            self.sales_summary_table.setColumnCount(7)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(0, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(1, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(2, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        __qtablewidgetitem35.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(3, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        __qtablewidgetitem36.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(4, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(5, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        __qtablewidgetitem38.setFont(font14);
        self.sales_summary_table.setHorizontalHeaderItem(6, __qtablewidgetitem38)
        self.sales_summary_table.setObjectName(u"sales_summary_table")
        self.sales_summary_table.setFont(font15)

        self.verticalLayout_19.addWidget(self.sales_summary_table)


        self.gridLayout_19.addLayout(self.verticalLayout_19, 0, 0, 1, 1)

        self.reports_tab.addTab(self.sales_summary_tab, "")
        self.top_products_tab = QWidget()
        self.top_products_tab.setObjectName(u"top_products_tab")
        self.gridLayout_22 = QGridLayout(self.top_products_tab)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.top_products_table = QTableWidget(self.top_products_tab)
        if (self.top_products_table.columnCount() < 5):
            self.top_products_table.setColumnCount(5)
        __qtablewidgetitem39 = QTableWidgetItem()
        __qtablewidgetitem39.setFont(font14);
        self.top_products_table.setHorizontalHeaderItem(0, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setFont(font14);
        self.top_products_table.setHorizontalHeaderItem(1, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        __qtablewidgetitem41.setFont(font14);
        self.top_products_table.setHorizontalHeaderItem(2, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        __qtablewidgetitem42.setFont(font14);
        self.top_products_table.setHorizontalHeaderItem(3, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        __qtablewidgetitem43.setFont(font14);
        self.top_products_table.setHorizontalHeaderItem(4, __qtablewidgetitem43)
        self.top_products_table.setObjectName(u"top_products_table")
        self.top_products_table.setFont(font15)

        self.gridLayout_21.addWidget(self.top_products_table, 1, 0, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setSpacing(4)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(6, 14, 4, -1)
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.view_prodcuts_lbl = QLabel(self.top_products_tab)
        self.view_prodcuts_lbl.setObjectName(u"view_prodcuts_lbl")
        self.view_prodcuts_lbl.setFont(font16)

        self.horizontalLayout_22.addWidget(self.view_prodcuts_lbl)

        self.filter_products_comboBox = QComboBox(self.top_products_tab)
        self.filter_products_comboBox.addItem("")
        self.filter_products_comboBox.addItem("")
        self.filter_products_comboBox.addItem("")
        self.filter_products_comboBox.addItem("")
        self.filter_products_comboBox.addItem("")
        self.filter_products_comboBox.setObjectName(u"filter_products_comboBox")
        self.filter_products_comboBox.setMinimumSize(QSize(110, 0))
        self.filter_products_comboBox.setFont(font16)

        self.horizontalLayout_22.addWidget(self.filter_products_comboBox)


        self.horizontalLayout_21.addLayout(self.horizontalLayout_22)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_7)


        self.gridLayout_21.addLayout(self.horizontalLayout_21, 0, 0, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_21, 0, 0, 1, 1)

        self.reports_tab.addTab(self.top_products_tab, "")
        self.top_employees_tab = QWidget()
        self.top_employees_tab.setObjectName(u"top_employees_tab")
        font17 = QFont()
        font17.setPointSize(8)
        self.top_employees_tab.setFont(font17)
        self.gridLayout_24 = QGridLayout(self.top_employees_tab)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_23 = QGridLayout()
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.top_employees_table = QTableWidget(self.top_employees_tab)
        if (self.top_employees_table.columnCount() < 5):
            self.top_employees_table.setColumnCount(5)
        __qtablewidgetitem44 = QTableWidgetItem()
        __qtablewidgetitem44.setFont(font14);
        self.top_employees_table.setHorizontalHeaderItem(0, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        __qtablewidgetitem45.setFont(font14);
        self.top_employees_table.setHorizontalHeaderItem(1, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        __qtablewidgetitem46.setFont(font14);
        self.top_employees_table.setHorizontalHeaderItem(2, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        __qtablewidgetitem47.setFont(font14);
        self.top_employees_table.setHorizontalHeaderItem(3, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        __qtablewidgetitem48.setFont(font14);
        self.top_employees_table.setHorizontalHeaderItem(4, __qtablewidgetitem48)
        self.top_employees_table.setObjectName(u"top_employees_table")
        self.top_employees_table.setFont(font15)

        self.gridLayout_23.addWidget(self.top_employees_table, 1, 0, 1, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setSpacing(4)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(6, 14, 4, -1)
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.view_employees_lbl = QLabel(self.top_employees_tab)
        self.view_employees_lbl.setObjectName(u"view_employees_lbl")
        self.view_employees_lbl.setFont(font16)

        self.horizontalLayout_24.addWidget(self.view_employees_lbl)

        self.filter_employees_comboBox = QComboBox(self.top_employees_tab)
        self.filter_employees_comboBox.addItem("")
        self.filter_employees_comboBox.addItem("")
        self.filter_employees_comboBox.addItem("")
        self.filter_employees_comboBox.addItem("")
        self.filter_employees_comboBox.addItem("")
        self.filter_employees_comboBox.setObjectName(u"filter_employees_comboBox")
        self.filter_employees_comboBox.setMinimumSize(QSize(110, 0))
        self.filter_employees_comboBox.setFont(font16)

        self.horizontalLayout_24.addWidget(self.filter_employees_comboBox)


        self.horizontalLayout_23.addLayout(self.horizontalLayout_24)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_8)


        self.gridLayout_23.addLayout(self.horizontalLayout_23, 0, 0, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_23, 0, 0, 1, 1)

        self.reports_tab.addTab(self.top_employees_tab, "")

        self.gridLayout_5.addWidget(self.reports_tab, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.reports_page)
        self.users_page = QWidget()
        self.users_page.setObjectName(u"users_page")
        self.gridLayout_15 = QGridLayout(self.users_page)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 26, -1, 5)
        self.header_widget_2 = QWidget(self.users_page)
        self.header_widget_2.setObjectName(u"header_widget_2")
        self.horizontalLayout_7 = QHBoxLayout(self.header_widget_2)
        self.horizontalLayout_7.setSpacing(14)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(140, -1, 140, 25)
        self.widget_8 = QWidget(self.header_widget_2)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy1.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy1)
        self.widget_8.setMinimumSize(QSize(150, 100))
        self.gridLayout_11 = QGridLayout(self.widget_8)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(5, 20, 5, 20)
        self.total_users_header_lbl = QLabel(self.widget_8)
        self.total_users_header_lbl.setObjectName(u"total_users_header_lbl")
        self.total_users_header_lbl.setMinimumSize(QSize(140, 20))
        self.total_users_header_lbl.setMaximumSize(QSize(16777215, 16777215))
        self.total_users_header_lbl.setFont(font10)
        self.total_users_header_lbl.setStyleSheet(u"")
        self.total_users_header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.total_users_header_lbl)

        self.total_users_lbl = QLabel(self.widget_8)
        self.total_users_lbl.setObjectName(u"total_users_lbl")
        self.total_users_lbl.setMinimumSize(QSize(140, 20))
        self.total_users_lbl.setMaximumSize(QSize(16777215, 16777215))
        self.total_users_lbl.setFont(font11)
        self.total_users_lbl.setStyleSheet(u"color: #F9E79F	")
        self.total_users_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.total_users_lbl)


        self.gridLayout_11.addLayout(self.verticalLayout_14, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_8)

        self.widget_9 = QWidget(self.header_widget_2)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setMinimumSize(QSize(150, 100))
        self.gridLayout_3 = QGridLayout(self.widget_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(5, 20, 5, 20)
        self.admins_header_lbl = QLabel(self.widget_9)
        self.admins_header_lbl.setObjectName(u"admins_header_lbl")
        self.admins_header_lbl.setMinimumSize(QSize(140, 20))
        self.admins_header_lbl.setFont(font10)
        self.admins_header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_16.addWidget(self.admins_header_lbl)

        self.admins_lbl = QLabel(self.widget_9)
        self.admins_lbl.setObjectName(u"admins_lbl")
        self.admins_lbl.setMinimumSize(QSize(140, 20))
        self.admins_lbl.setFont(font12)
        self.admins_lbl.setStyleSheet(u"color: #F9E79F")
        self.admins_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_16.addWidget(self.admins_lbl)


        self.gridLayout_3.addLayout(self.verticalLayout_16, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_9)

        self.widget_10 = QWidget(self.header_widget_2)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setMinimumSize(QSize(150, 100))
        self.gridLayout_12 = QGridLayout(self.widget_10)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(5, 20, 5, 20)
        self.managers_header_lbl = QLabel(self.widget_10)
        self.managers_header_lbl.setObjectName(u"managers_header_lbl")
        self.managers_header_lbl.setMinimumSize(QSize(140, 20))
        self.managers_header_lbl.setFont(font10)
        self.managers_header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_17.addWidget(self.managers_header_lbl)

        self.managers_lbl = QLabel(self.widget_10)
        self.managers_lbl.setObjectName(u"managers_lbl")
        self.managers_lbl.setMinimumSize(QSize(140, 20))
        self.managers_lbl.setFont(font12)
        self.managers_lbl.setStyleSheet(u"color: #F9E79F")
        self.managers_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_17.addWidget(self.managers_lbl)


        self.gridLayout_12.addLayout(self.verticalLayout_17, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_10)

        self.widget_11 = QWidget(self.header_widget_2)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setMinimumSize(QSize(150, 100))
        self.gridLayout_13 = QGridLayout(self.widget_11)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(5, 20, 5, 20)
        self.cashiers_header_lbl = QLabel(self.widget_11)
        self.cashiers_header_lbl.setObjectName(u"cashiers_header_lbl")
        self.cashiers_header_lbl.setMinimumSize(QSize(140, 20))
        self.cashiers_header_lbl.setFont(font10)
        self.cashiers_header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_18.addWidget(self.cashiers_header_lbl)

        self.cashiers_lbl = QLabel(self.widget_11)
        self.cashiers_lbl.setObjectName(u"cashiers_lbl")
        self.cashiers_lbl.setMinimumSize(QSize(140, 20))
        self.cashiers_lbl.setFont(font12)
        self.cashiers_lbl.setStyleSheet(u"color: #F9E79F")
        self.cashiers_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_18.addWidget(self.cashiers_lbl)


        self.gridLayout_13.addLayout(self.verticalLayout_18, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_11)


        self.verticalLayout.addWidget(self.header_widget_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_user_btn = QPushButton(self.users_page)
        self.add_user_btn.setObjectName(u"add_user_btn")
        self.add_user_btn.setMinimumSize(QSize(120, 44))
        self.add_user_btn.setFont(font2)

        self.horizontalLayout_2.addWidget(self.add_user_btn)

        self.update_user_btn = QPushButton(self.users_page)
        self.update_user_btn.setObjectName(u"update_user_btn")
        self.update_user_btn.setMinimumSize(QSize(120, 44))

        self.horizontalLayout_2.addWidget(self.update_user_btn)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(668, 18, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.delete_user_btn = QPushButton(self.users_page)
        self.delete_user_btn.setObjectName(u"delete_user_btn")
        self.delete_user_btn.setMinimumSize(QSize(120, 44))
        self.delete_user_btn.setFont(font2)

        self.horizontalLayout_3.addWidget(self.delete_user_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.user_table = QTableWidget(self.users_page)
        if (self.user_table.columnCount() < 4):
            self.user_table.setColumnCount(4)
        __qtablewidgetitem49 = QTableWidgetItem()
        __qtablewidgetitem49.setFont(font2);
        __qtablewidgetitem49.setBackground(QColor(255, 255, 255));
        self.user_table.setHorizontalHeaderItem(0, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        __qtablewidgetitem50.setFont(font2);
        self.user_table.setHorizontalHeaderItem(1, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        __qtablewidgetitem51.setFont(font2);
        self.user_table.setHorizontalHeaderItem(2, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        __qtablewidgetitem52.setFont(font2);
        self.user_table.setHorizontalHeaderItem(3, __qtablewidgetitem52)
        self.user_table.setObjectName(u"user_table")
        self.user_table.setMinimumSize(QSize(990, 490))
        self.user_table.setFont(font15)
        self.user_table.horizontalHeader().setMinimumSectionSize(100)
        self.user_table.verticalHeader().setMinimumSectionSize(30)

        self.verticalLayout.addWidget(self.user_table)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.username_search_lineEdit = QLineEdit(self.users_page)
        self.username_search_lineEdit.setObjectName(u"username_search_lineEdit")
        self.username_search_lineEdit.setMinimumSize(QSize(310, 40))
        self.username_search_lineEdit.setFont(font1)

        self.horizontalLayout_5.addWidget(self.username_search_lineEdit)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.clear_user_tb_btn = QPushButton(self.users_page)
        self.clear_user_tb_btn.setObjectName(u"clear_user_tb_btn")
        self.clear_user_tb_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_4.addWidget(self.clear_user_tb_btn)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.gridLayout_15.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.users_page)

        self.verticalLayout_7.addWidget(self.stackedWidget)


        self.gridLayout.addLayout(self.verticalLayout_7, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.pages_widget, 0, 1, 1, 1)

        self.sidebar = QWidget(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.sidebar)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.logo = QLabel(self.sidebar)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(80, 90))
        self.logo.setMaximumSize(QSize(80, 65))
        font18 = QFont()
        font18.setFamilies([u"Segoe UI Black"])
        font18.setPointSize(20)
        font18.setBold(True)
        self.logo.setFont(font18)
        self.logo.setStyleSheet(u"")
        self.logo.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.logo)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkout_btn = QPushButton(self.sidebar)
        self.checkout_btn.setObjectName(u"checkout_btn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkout_btn.sizePolicy().hasHeightForWidth())
        self.checkout_btn.setSizePolicy(sizePolicy2)
        self.checkout_btn.setMinimumSize(QSize(0, 0))
        font19 = QFont()
        font19.setFamilies([u"Segoe UI"])
        font19.setPointSize(13)
        font19.setWeight(QFont.DemiBold)
        self.checkout_btn.setFont(font19)
        self.checkout_btn.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u":/icons/checkout_gold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon6.addFile(u":/icons/checkout_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.checkout_btn.setIcon(icon6)
        self.checkout_btn.setIconSize(QSize(33, 33))
        self.checkout_btn.setCheckable(True)
        self.checkout_btn.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.checkout_btn)

        self.inventory_btn = QPushButton(self.sidebar)
        self.inventory_btn.setObjectName(u"inventory_btn")
        self.inventory_btn.setFont(font19)
        self.inventory_btn.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u":/icons/data_gold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon7.addFile(u":/icons/data_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.inventory_btn.setIcon(icon7)
        self.inventory_btn.setIconSize(QSize(33, 33))
        self.inventory_btn.setCheckable(True)
        self.inventory_btn.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.inventory_btn)

        self.reports_btn = QPushButton(self.sidebar)
        self.reports_btn.setObjectName(u"reports_btn")
        self.reports_btn.setFont(font19)
        self.reports_btn.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/chart_gold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon8.addFile(u":/icons/chart_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.reports_btn.setIcon(icon8)
        self.reports_btn.setIconSize(QSize(33, 33))
        self.reports_btn.setCheckable(True)
        self.reports_btn.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.reports_btn)

        self.users_btn = QPushButton(self.sidebar)
        self.users_btn.setObjectName(u"users_btn")
        self.users_btn.setFont(font19)
        self.users_btn.setStyleSheet(u"")
        icon9 = QIcon()
        icon9.addFile(u":/icons/users_gold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon9.addFile(u":/icons/users_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.users_btn.setIcon(icon9)
        self.users_btn.setIconSize(QSize(33, 33))
        self.users_btn.setCheckable(True)
        self.users_btn.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.users_btn)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 373, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.exit_btn = QPushButton(self.sidebar)
        self.exit_btn.setObjectName(u"exit_btn")
        self.exit_btn.setFont(font19)
        icon10 = QIcon()
        icon10.addFile(u":/icons/exit_gold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon10.addFile(u":/icons/exit_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.exit_btn.setIcon(icon10)
        self.exit_btn.setIconSize(QSize(33, 33))

        self.verticalLayout_5.addWidget(self.exit_btn)


        self.gridLayout_2.addWidget(self.sidebar, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)
        self.reports_tab.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Supermarket Manager", None))
        self.menu_btn.setText("")
        self.account_btn.setText("")
        self.barcode_lineEdit.setInputMask("")
        self.barcode_lineEdit.setText("")
        self.barcode_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Scan or enter barcode...", None))
        self.checkout_add_item.setText(QCoreApplication.translate("MainWindow", u"[F1] Add Item", None))
        self.cancel_sale_btn.setText(QCoreApplication.translate("MainWindow", u"[ESC] Cancel Sale", None))
        ___qtablewidgetitem = self.checkout_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Barcode", None));
        ___qtablewidgetitem1 = self.checkout_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Item Name", None));
        ___qtablewidgetitem2 = self.checkout_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Quantity", None));
        ___qtablewidgetitem3 = self.checkout_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Unit Price", None));
        ___qtablewidgetitem4 = self.checkout_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Discount", None));
        ___qtablewidgetitem5 = self.checkout_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Net Price", None));
        ___qtablewidgetitem6 = self.checkout_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Line Total", None));
#if QT_CONFIG(tooltip)
        self.increase_item_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Click to increase quantity of selected item. You can also press the + key on your keyboard.", None))
#endif // QT_CONFIG(tooltip)
        self.increase_item_btn.setText("")
#if QT_CONFIG(tooltip)
        self.decrease_item_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Click to decrease quantity of selected item. You can also press the - key on your keyboard.", None))
#endif // QT_CONFIG(tooltip)
        self.decrease_item_btn.setText("")
        self.set_quantity_btn.setText(QCoreApplication.translate("MainWindow", u"Set Quantity", None))
        self.apply_discount_btn.setText(QCoreApplication.translate("MainWindow", u"Discount Item", None))
        self.add_free_unit_btn.setText(QCoreApplication.translate("MainWindow", u"Add Free Unit", None))
#if QT_CONFIG(tooltip)
        self.remove_item_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Click to delete the selected item. You can also press the Del key on your keyboard.", None))
#endif // QT_CONFIG(tooltip)
        self.remove_item_btn.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Total:", None))
        self.total_lbl.setText(QCoreApplication.translate("MainWindow", u"$0", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cash Received:", None))
        self.cash_received_lineEdit.setInputMask("")
        self.cash_received_lineEdit.setText("")
        self.cash_received_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Amount...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Change Due:", None))
        self.change_due_lbl.setText(QCoreApplication.translate("MainWindow", u"$0", None))
        self.cash_btn.setText(QCoreApplication.translate("MainWindow", u"[F2] Cash", None))
        self.card_btn.setText(QCoreApplication.translate("MainWindow", u"[F3] Card", None))
        self.checkout_btn_2.setText(QCoreApplication.translate("MainWindow", u"Checkout", None))
        self.current_stock_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Total Items:", None))
        self.total_items_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.reorder_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Low Stock:", None))
        self.low_stock_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.out_of_stock_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Out of Stock:", None))
        self.out_of_stock_lb.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.expired_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Expired:", None))
        self.expired_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.stock_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Stock Value:", None))
        self.stock_value_lbl.setText(QCoreApplication.translate("MainWindow", u"$0", None))
        self.stock_cost_header_lbl_3.setText(QCoreApplication.translate("MainWindow", u"Stock Cost:", None))
        self.stock_cost_lbl.setText(QCoreApplication.translate("MainWindow", u"$0", None))
        self.add_item_btn.setText(QCoreApplication.translate("MainWindow", u"Add Item", None))
        self.update_item_btn.setText(QCoreApplication.translate("MainWindow", u"Update Item", None))
        self.discount_item_btn.setText(QCoreApplication.translate("MainWindow", u"Discount Item", None))
        self.delete_item_btn.setText(QCoreApplication.translate("MainWindow", u"Remove Item", None))
        ___qtablewidgetitem7 = self.inventory_table.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Category", None));
        ___qtablewidgetitem8 = self.inventory_table.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Item Name", None));
        ___qtablewidgetitem9 = self.inventory_table.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"SKU", None));
        ___qtablewidgetitem10 = self.inventory_table.horizontalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Barcode", None));
        ___qtablewidgetitem11 = self.inventory_table.horizontalHeaderItem(4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Batch Number", None));
        ___qtablewidgetitem12 = self.inventory_table.horizontalHeaderItem(5)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Quantity", None));
        ___qtablewidgetitem13 = self.inventory_table.horizontalHeaderItem(6)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Minimum Stock", None));
        ___qtablewidgetitem14 = self.inventory_table.horizontalHeaderItem(7)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Cost per Unit", None));
        ___qtablewidgetitem15 = self.inventory_table.horizontalHeaderItem(8)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Price per Unit", None));
        ___qtablewidgetitem16 = self.inventory_table.horizontalHeaderItem(9)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Discount", None));
        ___qtablewidgetitem17 = self.inventory_table.horizontalHeaderItem(10)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Net Price", None));
        ___qtablewidgetitem18 = self.inventory_table.horizontalHeaderItem(11)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Received Date", None));
        ___qtablewidgetitem19 = self.inventory_table.horizontalHeaderItem(12)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Expiry Date", None));
        ___qtablewidgetitem20 = self.inventory_table.horizontalHeaderItem(13)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        self.item_search_lineEdit.setInputMask("")
        self.item_search_lineEdit.setText("")
        self.item_search_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter an Item Name, SKU, Barcode, or Batch Number to Search...", None))
        self.clear_inventory_tb_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.low_stock_btn.setText(QCoreApplication.translate("MainWindow", u"Low Stock", None))
        self.out_of_stock_btn.setText(QCoreApplication.translate("MainWindow", u"Out of Stock", None))
        self.expired_btn.setText(QCoreApplication.translate("MainWindow", u"Expired", None))
        self.from_lbl.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.from_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy", None))
        self.to_lbl.setText(QCoreApplication.translate("MainWindow", u"To:", None))
        self.to_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"dd/MM/yyyy", None))
        self.sales_history_reset_btn.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        ___qtablewidgetitem21 = self.sales_history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Processed By", None));
        ___qtablewidgetitem22 = self.sales_history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"SKU", None));
        ___qtablewidgetitem23 = self.sales_history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Barcode", None));
        ___qtablewidgetitem24 = self.sales_history_table.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Order ID", None));
        ___qtablewidgetitem25 = self.sales_history_table.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Item Name", None));
        ___qtablewidgetitem26 = self.sales_history_table.horizontalHeaderItem(5)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Quantity", None));
        ___qtablewidgetitem27 = self.sales_history_table.horizontalHeaderItem(6)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"Unit Price", None));
        ___qtablewidgetitem28 = self.sales_history_table.horizontalHeaderItem(7)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"Discount", None));
        ___qtablewidgetitem29 = self.sales_history_table.horizontalHeaderItem(8)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"Net Price", None));
        ___qtablewidgetitem30 = self.sales_history_table.horizontalHeaderItem(9)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"Line Total", None));
        ___qtablewidgetitem31 = self.sales_history_table.horizontalHeaderItem(10)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"Sale Date", None));
        self.sales_search_lineEdit.setInputMask("")
        self.sales_search_lineEdit.setText("")
        self.sales_search_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter an Item Name, Username, SKU, Barcode, or Order ID to Search...", None))
        self.clear_sales_tbl.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.reports_tab.setTabText(self.reports_tab.indexOf(self.sales_history_tab), QCoreApplication.translate("MainWindow", u"Sales History", None))
        self.view_summary_lbl.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.filter_summary_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"All Time", None))
        self.filter_summary_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Daily", None))
        self.filter_summary_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Weekly", None))
        self.filter_summary_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Monthly", None))
        self.filter_summary_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Yearly", None))

        ___qtablewidgetitem32 = self.sales_summary_table.horizontalHeaderItem(0)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"Date", None));
        ___qtablewidgetitem33 = self.sales_summary_table.horizontalHeaderItem(1)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"Total Orders", None));
        ___qtablewidgetitem34 = self.sales_summary_table.horizontalHeaderItem(2)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"Total Quantity", None));
        ___qtablewidgetitem35 = self.sales_summary_table.horizontalHeaderItem(3)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"Gross Sales", None));
        ___qtablewidgetitem36 = self.sales_summary_table.horizontalHeaderItem(4)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"Discounts", None));
        ___qtablewidgetitem37 = self.sales_summary_table.horizontalHeaderItem(5)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"Net Sales", None));
        ___qtablewidgetitem38 = self.sales_summary_table.horizontalHeaderItem(6)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"Average Order Value", None));
        self.reports_tab.setTabText(self.reports_tab.indexOf(self.sales_summary_tab), QCoreApplication.translate("MainWindow", u"Sales Summary", None))
        ___qtablewidgetitem39 = self.top_products_table.horizontalHeaderItem(0)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"Item Name", None));
        ___qtablewidgetitem40 = self.top_products_table.horizontalHeaderItem(1)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"SKU", None));
        ___qtablewidgetitem41 = self.top_products_table.horizontalHeaderItem(2)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"Barcode", None));
        ___qtablewidgetitem42 = self.top_products_table.horizontalHeaderItem(3)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"Quantity Sold", None));
        ___qtablewidgetitem43 = self.top_products_table.horizontalHeaderItem(4)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"Total Revenue", None));
        self.view_prodcuts_lbl.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.filter_products_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"All Time", None))
        self.filter_products_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Daily", None))
        self.filter_products_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Weekly", None))
        self.filter_products_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Monthly", None))
        self.filter_products_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Yearly", None))

        self.reports_tab.setTabText(self.reports_tab.indexOf(self.top_products_tab), QCoreApplication.translate("MainWindow", u"Top Products", None))
        ___qtablewidgetitem44 = self.top_employees_table.horizontalHeaderItem(0)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"Username", None));
        ___qtablewidgetitem45 = self.top_employees_table.horizontalHeaderItem(1)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"Role", None));
        ___qtablewidgetitem46 = self.top_employees_table.horizontalHeaderItem(2)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"Transactions", None));
        ___qtablewidgetitem47 = self.top_employees_table.horizontalHeaderItem(3)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"Items Sold", None));
        ___qtablewidgetitem48 = self.top_employees_table.horizontalHeaderItem(4)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"Total Revenue", None));
        self.view_employees_lbl.setText(QCoreApplication.translate("MainWindow", u"View:", None))
        self.filter_employees_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"All Time", None))
        self.filter_employees_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Daily", None))
        self.filter_employees_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Weekly", None))
        self.filter_employees_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Monthly", None))
        self.filter_employees_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Yearly", None))

        self.reports_tab.setTabText(self.reports_tab.indexOf(self.top_employees_tab), QCoreApplication.translate("MainWindow", u"Top Employees", None))
        self.total_users_header_lbl.setText(QCoreApplication.translate("MainWindow", u"Total Users:", None))
        self.total_users_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.admins_header_lbl.setText(QCoreApplication.translate("MainWindow", u"Admins:", None))
        self.admins_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.managers_header_lbl.setText(QCoreApplication.translate("MainWindow", u"Managers:", None))
        self.managers_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.cashiers_header_lbl.setText(QCoreApplication.translate("MainWindow", u"Cashiers:", None))
        self.cashiers_lbl.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.add_user_btn.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.update_user_btn.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.delete_user_btn.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        ___qtablewidgetitem49 = self.user_table.horizontalHeaderItem(0)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"Username", None));
        ___qtablewidgetitem50 = self.user_table.horizontalHeaderItem(1)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"Password", None));
        ___qtablewidgetitem51 = self.user_table.horizontalHeaderItem(2)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"Role", None));
        ___qtablewidgetitem52 = self.user_table.horizontalHeaderItem(3)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"Created at", None));
        self.username_search_lineEdit.setInputMask("")
        self.username_search_lineEdit.setText("")
        self.username_search_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a Username to Search...", None))
        self.clear_user_tb_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.logo.setText(QCoreApplication.translate("MainWindow", u"S.M.", None))
        self.checkout_btn.setText("")
        self.inventory_btn.setText("")
        self.reports_btn.setText("")
        self.users_btn.setText("")
        self.exit_btn.setText("")
    # retranslateUi

