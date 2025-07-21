# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'discount_item_popuplEdtKa.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_DialogPopUp(object):
    def setupUi(self, DialogPopUp):
        if not DialogPopUp.objectName():
            DialogPopUp.setObjectName(u"DialogPopUp")
        DialogPopUp.resize(200, 114)
        DialogPopUp.setMinimumSize(QSize(200, 114))
        DialogPopUp.setMaximumSize(QSize(200, 114))
        icon = QIcon()
        icon.addFile(u":/icons/cart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DialogPopUp.setWindowIcon(icon)
        DialogPopUp.setStyleSheet(u"QMainWindow {\n"
"background-color: qlineargradient(\n"
"    x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #FFFFFF,\n"
"    stop:1 #E8E8E8\n"
");\n"
"}\n"
"\n"
"\n"
"QLineEdit {\n"
"	border: 1px solid #34495e;\n"
"	background: #F5F7F9;\n"
"	padding: 6px 8px;\n"
"	border-radius: 4px;\n"
"}\n"
"\n"
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
        self.gridLayout = QGridLayout(DialogPopUp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(14)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.discount_lineEdit = QLineEdit(DialogPopUp)
        self.discount_lineEdit.setObjectName(u"discount_lineEdit")
        self.discount_lineEdit.setMinimumSize(QSize(50, 35))
        font = QFont()
        font.setPointSize(14)
        self.discount_lineEdit.setFont(font)
        self.discount_lineEdit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.discount_lineEdit)

        self.percentage_label = QLabel(DialogPopUp)
        self.percentage_label.setObjectName(u"percentage_label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.percentage_label.setFont(font1)

        self.horizontalLayout.addWidget(self.percentage_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.apply_discount_btn = QPushButton(DialogPopUp)
        self.apply_discount_btn.setObjectName(u"apply_discount_btn")
        self.apply_discount_btn.setMinimumSize(QSize(100, 40))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.apply_discount_btn.setFont(font2)
        self.apply_discount_btn.setIconSize(QSize(16, 16))

        self.verticalLayout.addWidget(self.apply_discount_btn)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.retranslateUi(DialogPopUp)

        QMetaObject.connectSlotsByName(DialogPopUp)
    # setupUi

    def retranslateUi(self, DialogPopUp):
        DialogPopUp.setWindowTitle(QCoreApplication.translate("DialogPopUp", u"Discount Item", None))
        self.discount_lineEdit.setText("")
        self.discount_lineEdit.setPlaceholderText("")
        self.percentage_label.setText(QCoreApplication.translate("DialogPopUp", u"%", None))
        self.apply_discount_btn.setText(QCoreApplication.translate("DialogPopUp", u"Apply Discount", None))
    # retranslateUi

