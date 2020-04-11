# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignalGenerator.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(886, 600)
        MainWindow.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textBrowser_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textBrowser_2.setAcceptDrops(False)
        self.textBrowser_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout.addWidget(self.textBrowser_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lstConfiguration = QtWidgets.QListWidget(self.groupBox_2)
        self.lstConfiguration.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstConfiguration.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.lstConfiguration.setAlternatingRowColors(True)
        self.lstConfiguration.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lstConfiguration.setObjectName("lstConfiguration")
        self.horizontalLayout_2.addWidget(self.lstConfiguration)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textDescription = QtWidgets.QTextEdit(self.groupBox)
        self.textDescription.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.textDescription.setObjectName("textDescription")
        self.verticalLayout_2.addWidget(self.textDescription)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 12, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.btnStart = QtWidgets.QPushButton(self.groupBox)
        self.btnStart.setObjectName("btnStart")
        self.gridLayout.addWidget(self.btnStart, 0, 4, 1, 1)
        self.btnStop = QtWidgets.QPushButton(self.groupBox)
        self.btnStop.setObjectName("btnStop")
        self.gridLayout.addWidget(self.btnStop, 0, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.btnSearchPS = QtWidgets.QPushButton(self.groupBox)
        self.btnSearchPS.setObjectName("btnSearchPS")
        self.gridLayout.addWidget(self.btnSearchPS, 0, 1, 1, 1)
        self.cbxPSAddress = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbxPSAddress.sizePolicy().hasHeightForWidth())
        self.cbxPSAddress.setSizePolicy(sizePolicy)
        self.cbxPSAddress.setObjectName("cbxPSAddress")
        self.gridLayout.addWidget(self.cbxPSAddress, 0, 0, 1, 1)
        self.btnShowCode = QtWidgets.QPushButton(self.groupBox)
        self.btnShowCode.setObjectName("btnShowCode")
        self.gridLayout.addWidget(self.btnShowCode, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout.addWidget(self.groupBox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.lstConfiguration.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Signal Generator"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This application uses Pulse Streamer to generate various pulse patterns that emulate signals of a typical experimental setup. These signals include laser sync, pixel triggers and photon events. Please select the configuration in the list below and click &quot;Start&quot;.</p></body></html>"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Select configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "Description"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnStop.setText(_translate("MainWindow", "Stop"))
        self.btnSearchPS.setText(_translate("MainWindow", "Refresh"))
        self.btnShowCode.setText(_translate("MainWindow", "Show code"))

