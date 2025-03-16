# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\LoginAndRegister.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1230, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_Login = QtWidgets.QWidget(self.centralwidget)
        self.widget_Login.setGeometry(QtCore.QRect(80, 40, 971, 601))
        self.widget_Login.setStyleSheet("background-image: url(:/image/images/main_background.jpg);\n"
"background-color: rgb(255, 255, 255);")
        self.widget_Login.setObjectName("widget_Login")
        self.widget_UserLog = QtWidgets.QWidget(self.widget_Login)
        self.widget_UserLog.setGeometry(QtCore.QRect(550, 170, 381, 271))
        self.widget_UserLog.setStyleSheet("background-color: rgb(85, 255, 255, 200);\n"
"background: transparent;\n"
"border: 1px solid #00ffff; \n"
"padding: 10px;")
        self.widget_UserLog.setObjectName("widget_UserLog")
        self.lineEdit_Psd = QtWidgets.QLineEdit(self.widget_UserLog)
        self.lineEdit_Psd.setGeometry(QtCore.QRect(60, 120, 261, 44))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Psd.sizePolicy().hasHeightForWidth())
        self.lineEdit_Psd.setSizePolicy(sizePolicy)
        self.lineEdit_Psd.setStyleSheet("background-color: rgb(255, 255, 255, 70);\n"
"color: rgb(255, 255, 255);\n"
"border: 1px solid #00ffff; \n"
"padding: 10px;\n"
"")
        self.lineEdit_Psd.setClearButtonEnabled(True)
        self.lineEdit_Psd.setObjectName("lineEdit_Psd")
        self.lineEdit_ID = QtWidgets.QLineEdit(self.widget_UserLog)
        self.lineEdit_ID.setGeometry(QtCore.QRect(61, 65, 261, 44))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ID.sizePolicy().hasHeightForWidth())
        self.lineEdit_ID.setSizePolicy(sizePolicy)
        self.lineEdit_ID.setStyleSheet("background-color: rgb(255, 255, 255, 70);\n"
"color: rgb(255, 255, 255);\n"
"border: 1px solid #00ffff; \n"
"padding: 10px;\n"
"\n"
"\n"
"")
        self.lineEdit_ID.setInputMask("")
        self.lineEdit_ID.setClearButtonEnabled(True)
        self.lineEdit_ID.setObjectName("lineEdit_ID")
        self.label_ = QtWidgets.QLabel(self.widget_UserLog)
        self.label_.setGeometry(QtCore.QRect(120, 10, 151, 41))
        self.label_.setStyleSheet("font: 12pt \"宋体\";\n"
"color: rgb(85, 255, 255);\n"
"border: 0px;\n"
"padding: 10px;")
        self.label_.setObjectName("label_")
        self.pushButton_Register = QtWidgets.QPushButton(self.widget_UserLog)
        self.pushButton_Register.setGeometry(QtCore.QRect(210, 190, 131, 51))
        self.pushButton_Register.setStyleSheet("background-color: rgb(85, 255, 255, 200);\n"
"border-radius: 6px;\n"
"border-style: solid;\n"
"border-image: linear-gradient(to bottom, #FF0000, #00FF00) 1 1;\n"
"font: 12pt \"新宋体\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.pushButton_Register.setObjectName("pushButton_Register")
        self.pushButton_Login = QtWidgets.QPushButton(self.widget_UserLog)
        self.pushButton_Login.setGeometry(QtCore.QRect(20, 190, 121, 51))
        self.pushButton_Login.setStyleSheet("background-color: rgb(85, 255, 255, 200);\n"
"border-radius: 6px;\n"
"border-style: solid;\n"
"border-image: linear-gradient(to bottom, #FF0000, #00FF00) 1 1;\n"
"font: 12pt \"新宋体\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.pushButton_Login.setObjectName("pushButton_Login")
        self.label_Name = QtWidgets.QLabel(self.widget_Login)
        self.label_Name.setGeometry(QtCore.QRect(550, 100, 371, 51))
        self.label_Name.setStyleSheet("font: 20pt \"宋体\";\n"
"background-color: rgb(255, 255, 255, 0);\n"
"color: rgb(0, 255, 255);\n"
"background: transparent")
        self.label_Name.setObjectName("label_Name")
        self.pushButton_mininum = QtWidgets.QPushButton(self.widget_Login)
        self.pushButton_mininum.setGeometry(QtCore.QRect(839, 7, 51, 28))
        self.pushButton_mininum.setStyleSheet("font: 20pt \"Agency FB\";\n"
"background-color: rgb(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"background: transparent")
        self.pushButton_mininum.setObjectName("pushButton_mininum")
        self.pushButton_maximum = QtWidgets.QPushButton(self.widget_Login)
        self.pushButton_maximum.setGeometry(QtCore.QRect(880, 10, 56, 29))
        self.pushButton_maximum.setStyleSheet("font: 75 15pt \"Agency FB\";\n"
"background-color: rgb(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"background: transparent")
        self.pushButton_maximum.setObjectName("pushButton_maximum")
        self.pushButton_close = QtWidgets.QPushButton(self.widget_Login)
        self.pushButton_close.setGeometry(QtCore.QRect(924, 0, 51, 38))
        self.pushButton_close.setStyleSheet("background-color: rgb(255, 255, 255, 0);\n"
"font: 75 20pt \"Agency FB\";\n"
"color: rgb(255, 255, 255);\n"
"background: transparent")
        self.pushButton_close.setObjectName("pushButton_close")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1230, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_Psd.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.lineEdit_ID.setPlaceholderText(_translate("MainWindow", "请输入登录账号"))
        self.lineEdit_Psd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_.setText(_translate("MainWindow", "用户登录"))
        self.pushButton_Register.setText(_translate("MainWindow", "注册"))
        self.pushButton_Login.setText(_translate("MainWindow", "登录"))
        self.label_Name.setText(_translate("MainWindow", "入侵检测与响应系统登录"))
        self.pushButton_mininum.setText(_translate("MainWindow", "—"))
        self.pushButton_maximum.setText(_translate("MainWindow", "❐"))
        self.pushButton_close.setText(_translate("MainWindow", "x"))

import image

