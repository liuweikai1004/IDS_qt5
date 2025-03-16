# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Home.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1642, 846)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(90, 60, 831, 611))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.widget_NameAndLogo = QtWidgets.QWidget(self.widget)
        self.widget_NameAndLogo.setGeometry(QtCore.QRect(0, 0, 181, 71))
        self.widget_NameAndLogo.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.widget_NameAndLogo.setObjectName("widget_NameAndLogo")
        self.label_Name = QtWidgets.QLabel(self.widget_NameAndLogo)
        self.label_Name.setGeometry(QtCore.QRect(39, 30, 141, 20))
        self.label_Name.setObjectName("label_Name")
        self.lineEdit_Logo = QtWidgets.QLineEdit(self.widget_NameAndLogo)
        self.lineEdit_Logo.setGeometry(QtCore.QRect(0, 10, 41, 61))
        self.lineEdit_Logo.setStyleSheet("background-image: url(:/image/images/文心一言AI作图_20250312092512.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"background-size: 50% 50%;\n"
"border: 1px solid #00ffff; \n"
"")
        self.lineEdit_Logo.setObjectName("lineEdit_Logo")
        self.widget_Menu = QtWidgets.QWidget(self.widget)
        self.widget_Menu.setGeometry(QtCore.QRect(0, 70, 181, 531))
        self.widget_Menu.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.widget_Menu.setObjectName("widget_Menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_Menu)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_Home = QtWidgets.QPushButton(self.widget_Menu)
        self.pushButton_Home.setObjectName("pushButton_Home")
        self.verticalLayout.addWidget(self.pushButton_Home)
        self.pushButton_DataCapture = QtWidgets.QPushButton(self.widget_Menu)
        self.pushButton_DataCapture.setObjectName("pushButton_DataCapture")
        self.verticalLayout.addWidget(self.pushButton_DataCapture)
        self.pushButton_DataProAndPre = QtWidgets.QPushButton(self.widget_Menu)
        self.pushButton_DataProAndPre.setObjectName("pushButton_DataProAndPre")
        self.verticalLayout.addWidget(self.pushButton_DataProAndPre)
        self.widget_Home = QtWidgets.QWidget(self.widget)
        self.widget_Home.setGeometry(QtCore.QRect(180, 0, 651, 601))
        self.widget_Home.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #00eaff, stop: 1 #00aaff);")
        self.widget_Home.setObjectName("widget_Home")
        self.pushButton_maximum = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_maximum.setGeometry(QtCore.QRect(556, 10, 56, 29))
        self.pushButton_maximum.setStyleSheet("font: 75 15pt \"Agency FB\";\n"
"background-color: rgb(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_maximum.setObjectName("pushButton_maximum")
        self.pushButton_mininum = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_mininum.setGeometry(QtCore.QRect(515, 7, 51, 28))
        self.pushButton_mininum.setStyleSheet("font: 20pt \"Agency FB\";\n"
"background-color: rgb(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_mininum.setObjectName("pushButton_mininum")
        self.pushButton_close = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_close.setGeometry(QtCore.QRect(600, 0, 51, 38))
        self.pushButton_close.setStyleSheet("background-color: rgb(255, 255, 255, 0);\n"
"font: 75 20pt \"Agency FB\";\n"
"color: rgb(255, 255, 255);\n"
"")
        self.pushButton_close.setObjectName("pushButton_close")
        self.label_Welcome = QtWidgets.QLabel(self.widget_Home)
        self.label_Welcome.setGeometry(QtCore.QRect(0, 60, 521, 121))
        self.label_Welcome.setStyleSheet("font: 28pt \"新宋体\";\n"
"background-color: rgb(255, 255, 255, 0);")
        self.label_Welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Welcome.setObjectName("label_Welcome")
        self.pushButton_Start = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_Start.setGeometry(QtCore.QRect(90, 100, 141, 51))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_End = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_End.setGeometry(QtCore.QRect(370, 100, 161, 51))
        self.pushButton_End.setObjectName("pushButton_End")
        self.pushButton_InputData = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_InputData.setGeometry(QtCore.QRect(40, 60, 151, 51))
        self.pushButton_InputData.setObjectName("pushButton_InputData")
        self.textEdit_Result = QtWidgets.QTextEdit(self.widget_Home)
        self.textEdit_Result.setGeometry(QtCore.QRect(50, 150, 541, 401))
        self.textEdit_Result.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_Result.setObjectName("textEdit_Result")
        self.textEdit_Tips = QtWidgets.QTextEdit(self.widget_Home)
        self.textEdit_Tips.setGeometry(QtCore.QRect(20, 220, 331, 291))
        self.textEdit_Tips.setStyleSheet("background-color: rgb(255, 255, 255, 0);\n"
"border: 0px solid #00ffff; ")
        self.textEdit_Tips.setObjectName("textEdit_Tips")
        self.textEdit_Log = QtWidgets.QTextEdit(self.widget_Home)
        self.textEdit_Log.setGeometry(QtCore.QRect(80, 180, 471, 361))
        self.textEdit_Log.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_Log.setObjectName("textEdit_Log")
        self.pushButton_loadModel = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_loadModel.setGeometry(QtCore.QRect(230, 60, 151, 51))
        self.pushButton_loadModel.setObjectName("pushButton_loadModel")
        self.pushButton_StartPredict = QtWidgets.QPushButton(self.widget_Home)
        self.pushButton_StartPredict.setGeometry(QtCore.QRect(425, 60, 151, 51))
        self.pushButton_StartPredict.setObjectName("pushButton_StartPredict")
        self.textEdit_Result.raise_()
        self.pushButton_close.raise_()
        self.pushButton_maximum.raise_()
        self.pushButton_mininum.raise_()
        self.label_Welcome.raise_()
        self.pushButton_Start.raise_()
        self.pushButton_End.raise_()
        self.pushButton_InputData.raise_()
        self.textEdit_Tips.raise_()
        self.textEdit_Log.raise_()
        self.pushButton_loadModel.raise_()
        self.pushButton_StartPredict.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1642, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_Home.clicked.connect(self.label_Welcome.show)
        self.pushButton_Home.clicked.connect(self.textEdit_Tips.show)
        self.pushButton_Home.clicked.connect(self.pushButton_InputData.hide)
        self.pushButton_Home.clicked.connect(self.textEdit_Result.hide)
        self.pushButton_Home.clicked.connect(self.pushButton_Start.hide)
        self.pushButton_Home.clicked.connect(self.pushButton_End.hide)
        self.pushButton_DataCapture.clicked.connect(self.label_Welcome.hide)
        self.pushButton_DataCapture.clicked.connect(self.textEdit_Tips.hide)
        self.pushButton_DataCapture.clicked.connect(self.pushButton_Start.show)
        self.pushButton_DataCapture.clicked.connect(self.pushButton_End.show)
        self.pushButton_DataCapture.clicked.connect(self.label_Welcome.hide)
        self.pushButton_DataCapture.clicked.connect(self.textEdit_Tips.hide)
        self.pushButton_DataCapture.clicked.connect(self.textEdit_Result.hide)
        self.pushButton_DataCapture.clicked.connect(self.pushButton_InputData.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.textEdit_Tips.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.label_Welcome.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.pushButton_Start.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.pushButton_End.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.pushButton_InputData.show)
        self.pushButton_DataProAndPre.clicked.connect(self.textEdit_Result.show)
        self.pushButton_Home.clicked.connect(self.textEdit_Log.hide)
        self.pushButton_DataCapture.clicked.connect(self.textEdit_Log.show)
        self.pushButton_DataProAndPre.clicked.connect(self.textEdit_Log.hide)
        self.pushButton_Home.clicked.connect(self.pushButton_loadModel.hide)
        self.pushButton_Home.clicked.connect(self.pushButton_StartPredict.hide)
        self.pushButton_DataCapture.clicked.connect(self.pushButton_loadModel.hide)
        self.pushButton_DataCapture.clicked.connect(self.pushButton_StartPredict.hide)
        self.pushButton_DataProAndPre.clicked.connect(self.pushButton_loadModel.show)
        self.pushButton_DataProAndPre.clicked.connect(self.pushButton_StartPredict.show)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Name.setText(_translate("MainWindow", "入侵检测与响应系统"))
        self.pushButton_Home.setText(_translate("MainWindow", "首页"))
        self.pushButton_DataCapture.setText(_translate("MainWindow", "网络流量收集"))
        self.pushButton_DataProAndPre.setText(_translate("MainWindow", "数据处理与检测"))
        self.pushButton_maximum.setText(_translate("MainWindow", "❐"))
        self.pushButton_mininum.setText(_translate("MainWindow", "—"))
        self.pushButton_close.setText(_translate("MainWindow", "x"))
        self.label_Welcome.setText(_translate("MainWindow", "欢迎使用入侵检测系统"))
        self.pushButton_Start.setText(_translate("MainWindow", "开始收集"))
        self.pushButton_End.setText(_translate("MainWindow", "结束收集"))
        self.pushButton_InputData.setText(_translate("MainWindow", "导入数据并处理"))
        self.textEdit_Tips.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">该系统基于CNN-LSTM学习算法构建,用法如下：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(1)网络流量收集</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">可以根据用户需求收集一定数量网络流量数据</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">包，并提取出必要的流量包中的数据存在提供</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">的CSV文件中。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">操作：点击“开始收集”，本系统收集网络中</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">的流量包，点击“结束收集”，系统停止收集</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">网络流量数据包，并保存在提供的文件中。</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">（2）数据处理与预测</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">用户提供需要进行检测的数据文件，首先进行</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">必要的预处理，处理完成后交给已训练好的模</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">型机型检测。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">操作：点击“导入数据”，用户将文件导入，</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">点击“开始检测”，系统利用训练好的模型进</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">行检测并将检测结果展示在结果框内。</p></body></html>"))
        self.pushButton_loadModel.setText(_translate("MainWindow", "加载模型"))
        self.pushButton_StartPredict.setText(_translate("MainWindow", "开始检测"))

import image

