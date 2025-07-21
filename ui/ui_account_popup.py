# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'account_popupDyIzfP.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_AccountInformation(object):
    def setupUi(self, AccountInformation):
        if not AccountInformation.objectName():
            AccountInformation.setObjectName(u"AccountInformation")
        AccountInformation.resize(280, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AccountInformation.sizePolicy().hasHeightForWidth())
        AccountInformation.setSizePolicy(sizePolicy)
        AccountInformation.setMinimumSize(QSize(280, 200))
        AccountInformation.setMaximumSize(QSize(400, 200))
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AccountInformation.setWindowIcon(icon)
        AccountInformation.setStyleSheet(u"QMainWindow {\n"
"background-color: qlineargradient(\n"
"    x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #FFFFFF,\n"
"    stop:1 #E8E8E8\n"
");\n"
"}\n"
"\n"
"#info_widget {\n"
"    background-color: #34495e;\n"
"    border-radius: 5px;\n"
"    border: 2px solid #2c3e50;\n"
"}\n"
"\n"
"QLabel#username_text_lbl,\n"
"QLabel#role_text_lbl {\n"
"    color: #E8E8E8;\n"
"}\n"
"\n"
"QLabel#username_lbl,\n"
"QLabel#role_lbl {\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"#username_widget,\n"
"#role_widget {\n"
"	border: 2px solid #F5F7F9;\n"
"	border-radius: 5px\n"
"}\n"
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
"\n"
"")
        self.gridLayout_4 = QGridLayout(AccountInformation)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.info_widget = QWidget(AccountInformation)
        self.info_widget.setObjectName(u"info_widget")
        self.gridLayout_3 = QGridLayout(self.info_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.username_widget = QWidget(self.info_widget)
        self.username_widget.setObjectName(u"username_widget")
        self.gridLayout = QGridLayout(self.username_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.username_text_lbl = QLabel(self.username_widget)
        self.username_text_lbl.setObjectName(u"username_text_lbl")
        font = QFont()
        font.setPointSize(13)
        font.setWeight(QFont.DemiBold)
        self.username_text_lbl.setFont(font)
        self.username_text_lbl.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.username_text_lbl)

        self.username_lbl = QLabel(self.username_widget)
        self.username_lbl.setObjectName(u"username_lbl")
        self.username_lbl.setFont(font)
        self.username_lbl.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.username_lbl)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.username_widget)

        self.role_widget = QWidget(self.info_widget)
        self.role_widget.setObjectName(u"role_widget")
        self.gridLayout_2 = QGridLayout(self.role_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.role_text_lbl = QLabel(self.role_widget)
        self.role_text_lbl.setObjectName(u"role_text_lbl")
        self.role_text_lbl.setFont(font)
        self.role_text_lbl.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.role_text_lbl)

        self.role_lbl = QLabel(self.role_widget)
        self.role_lbl.setObjectName(u"role_lbl")
        self.role_lbl.setFont(font)
        self.role_lbl.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.role_lbl)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.role_widget)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.info_widget)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.logout_btn = QPushButton(AccountInformation)
        self.logout_btn.setObjectName(u"logout_btn")
        self.logout_btn.setMinimumSize(QSize(200, 45))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.logout_btn.setFont(font1)

        self.verticalLayout_3.addWidget(self.logout_btn)


        self.gridLayout_4.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(AccountInformation)

        QMetaObject.connectSlotsByName(AccountInformation)
    # setupUi

    def retranslateUi(self, AccountInformation):
        AccountInformation.setWindowTitle(QCoreApplication.translate("AccountInformation", u"Account Information", None))
        self.username_text_lbl.setText(QCoreApplication.translate("AccountInformation", u"Username:", None))
        self.username_lbl.setText(QCoreApplication.translate("AccountInformation", u"username", None))
        self.role_text_lbl.setText(QCoreApplication.translate("AccountInformation", u"Role:", None))
        self.role_lbl.setText(QCoreApplication.translate("AccountInformation", u"role", None))
        self.logout_btn.setText(QCoreApplication.translate("AccountInformation", u"Log out", None))
    # retranslateUi

