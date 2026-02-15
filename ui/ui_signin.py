# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signinzgFaLe.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_LogInWindow(object):
    def setupUi(self, LogInWindow):
        if not LogInWindow.objectName():
            LogInWindow.setObjectName(u"LogInWindow")
        LogInWindow.resize(800, 600)
        LogInWindow.setMinimumSize(QSize(800, 600))
        LogInWindow.setMaximumSize(QSize(800, 600))
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        LogInWindow.setWindowIcon(icon)
        LogInWindow.setStyleSheet(u"QMainWindow {\n"
"background-color: qlineargradient(\n"
"    x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #FFFFFF,\n"
"    stop:1 #E8E8E8\n"
");\n"
"}\n"
"\n"
"#username_label, #password_label{\n"
"	color: #34495e;\n"
"	font-family: \"Segoe UI\";\n"
"	font-weight: medium;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#header_label {\n"
"	color: #34495e;\n"
"}\n"
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
"    padding: 10px 24px;\n"
"	font-weight: medium;\n"
"    font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2c3e50; \n"
"    border-color: #2c3e50;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #22313f; \n"
"    border-color: #22313f;\n"
"}")
        self.centralwidget = QWidget(LogInWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 83, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(185, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 82, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(186, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 34, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(22)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(12)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.header_label = QLabel(self.widget)
        self.header_label.setObjectName(u"header_label")
        self.header_label.setMinimumSize(QSize(0, 100))
        font = QFont()
        font.setFamilies([u"Segoe UI Semibold"])
        font.setPointSize(20)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.header_label)

        self.input_layout = QVBoxLayout()
        self.input_layout.setObjectName(u"input_layout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.username_label = QLabel(self.widget)
        self.username_label.setObjectName(u"username_label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        self.username_label.setFont(font1)

        self.verticalLayout.addWidget(self.username_label)

        self.username_lineEdit = QLineEdit(self.widget)
        self.username_lineEdit.setObjectName(u"username_lineEdit")
        self.username_lineEdit.setMinimumSize(QSize(0, 35))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(14)
        font2.setBold(False)
        self.username_lineEdit.setFont(font2)

        self.verticalLayout.addWidget(self.username_lineEdit)


        self.input_layout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.password_label = QLabel(self.widget)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setFont(font1)

        self.verticalLayout_2.addWidget(self.password_label)

        self.password_lineEdit = QLineEdit(self.widget)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setMinimumSize(QSize(0, 35))
        self.password_lineEdit.setFont(font2)

        self.verticalLayout_2.addWidget(self.password_lineEdit)


        self.input_layout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.input_layout)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.log_in_pushButton = QPushButton(self.widget)
        self.log_in_pushButton.setObjectName(u"log_in_pushButton")
        font3 = QFont()
        font3.setBold(True)
        self.log_in_pushButton.setFont(font3)

        self.verticalLayout_6.addWidget(self.log_in_pushButton)


        self.gridLayout.addLayout(self.verticalLayout_6, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 36, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 1, 1, 1, 1)

        LogInWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LogInWindow)

        QMetaObject.connectSlotsByName(LogInWindow)
    # setupUi

    def retranslateUi(self, LogInWindow):
        LogInWindow.setWindowTitle(QCoreApplication.translate("LogInWindow", u"Supermarket Manager", None))
        self.header_label.setText(QCoreApplication.translate("LogInWindow", u"Supermarket Manager", None))
        self.username_label.setText(QCoreApplication.translate("LogInWindow", u"Username:", None))
        self.password_label.setText(QCoreApplication.translate("LogInWindow", u"Password:", None))
        self.log_in_pushButton.setText(QCoreApplication.translate("LogInWindow", u"Log in", None))
    # retranslateUi

