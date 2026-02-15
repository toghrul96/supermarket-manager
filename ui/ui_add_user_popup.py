# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_user_popupVpQDLQ.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_AddUserPopUp(object):
    def setupUi(self, AddUserPopUp):
        if not AddUserPopUp.objectName():
            AddUserPopUp.setObjectName(u"AddUserPopUp")
        AddUserPopUp.resize(382, 338)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddUserPopUp.sizePolicy().hasHeightForWidth())
        AddUserPopUp.setSizePolicy(sizePolicy)
        AddUserPopUp.setMinimumSize(QSize(382, 338))
        AddUserPopUp.setMaximumSize(QSize(382, 338))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        AddUserPopUp.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AddUserPopUp.setWindowIcon(icon)
        AddUserPopUp.setStyleSheet(u"QMainWindow {\n"
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
"")
        self.gridLayout_2 = QGridLayout(AddUserPopUp)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(3, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.widget = QWidget(AddUserPopUp)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setSpacing(25)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setSpacing(6)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setSpacing(4)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.username_label = QLabel(self.widget)
        self.username_label.setObjectName(u"username_label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.username_label.setFont(font1)

        self.verticalLayout_28.addWidget(self.username_label)

        self.username_lineEdit_1 = QLineEdit(self.widget)
        self.username_lineEdit_1.setObjectName(u"username_lineEdit_1")
        self.username_lineEdit_1.setMinimumSize(QSize(0, 35))
        font2 = QFont()
        font2.setPointSize(14)
        self.username_lineEdit_1.setFont(font2)

        self.verticalLayout_28.addWidget(self.username_lineEdit_1)


        self.verticalLayout_27.addLayout(self.verticalLayout_28)

        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setSpacing(4)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.password_label = QLabel(self.widget)
        self.password_label.setObjectName(u"password_label")

        self.verticalLayout_29.addWidget(self.password_label)

        self.password_lineEdit_1 = QLineEdit(self.widget)
        self.password_lineEdit_1.setObjectName(u"password_lineEdit_1")
        self.password_lineEdit_1.setMinimumSize(QSize(0, 35))
        self.password_lineEdit_1.setFont(font2)

        self.verticalLayout_29.addWidget(self.password_lineEdit_1)


        self.verticalLayout_27.addLayout(self.verticalLayout_29)

        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setSpacing(4)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(-1, 2, -1, -1)
        self.role_label = QLabel(self.widget)
        self.role_label.setObjectName(u"role_label")

        self.verticalLayout_30.addWidget(self.role_label)

        self.role_cb = QComboBox(self.widget)
        self.role_cb.addItem("")
        self.role_cb.addItem("")
        self.role_cb.addItem("")
        self.role_cb.setObjectName(u"role_cb")
        self.role_cb.setMinimumSize(QSize(0, 40))
        font3 = QFont()
        font3.setPointSize(11)
        self.role_cb.setFont(font3)
        self.role_cb.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.role_cb.setIconSize(QSize(16, 16))

        self.verticalLayout_30.addWidget(self.role_cb)


        self.verticalLayout_27.addLayout(self.verticalLayout_30)


        self.verticalLayout_26.addLayout(self.verticalLayout_27)

        self.add_user_btn = QPushButton(self.widget)
        self.add_user_btn.setObjectName(u"add_user_btn")
        self.add_user_btn.setMinimumSize(QSize(320, 45))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.add_user_btn.setFont(font4)

        self.verticalLayout_26.addWidget(self.add_user_btn)


        self.gridLayout.addLayout(self.verticalLayout_26, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(2, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 1, 1, 1)


        self.retranslateUi(AddUserPopUp)

        QMetaObject.connectSlotsByName(AddUserPopUp)
    # setupUi

    def retranslateUi(self, AddUserPopUp):
        AddUserPopUp.setWindowTitle(QCoreApplication.translate("AddUserPopUp", u"Add New User", None))
        self.username_label.setText(QCoreApplication.translate("AddUserPopUp", u"Username:", None))
        self.password_label.setText(QCoreApplication.translate("AddUserPopUp", u"Password:", None))
        self.role_label.setText(QCoreApplication.translate("AddUserPopUp", u"Role:", None))
        self.role_cb.setItemText(0, QCoreApplication.translate("AddUserPopUp", u"Cashier", None))
        self.role_cb.setItemText(1, QCoreApplication.translate("AddUserPopUp", u"Manager", None))
        self.role_cb.setItemText(2, QCoreApplication.translate("AddUserPopUp", u"Admin", None))

        self.add_user_btn.setText(QCoreApplication.translate("AddUserPopUp", u"Add User", None))
    # retranslateUi

