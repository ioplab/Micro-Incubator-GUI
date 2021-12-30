# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\YJ\JerryYea\Ui\winMain.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        MainWindow.setMinimumSize(QtCore.QSize(400, 500))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.model = QtWidgets.QWidget(MainWindow)
        self.model.setObjectName("model")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.model)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.view = QtWidgets.QVBoxLayout()
        self.view.setObjectName("view")
        self.top = QtWidgets.QVBoxLayout()
        self.top.setContentsMargins(-1, 0, -1, -1)
        self.top.setObjectName("top")
        self.lbl_5 = QtWidgets.QLabel(self.model)
        self.lbl_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lbl_5.setObjectName("lbl_5")
        self.top.addWidget(self.lbl_5)
        self.line_4 = QtWidgets.QFrame(self.model)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.top.addWidget(self.line_4)
        self.topView = QtWidgets.QHBoxLayout()
        self.topView.setObjectName("topView")
        self.cbComList = QtWidgets.QComboBox(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbComList.sizePolicy().hasHeightForWidth())
        self.cbComList.setSizePolicy(sizePolicy)
        self.cbComList.setObjectName("cbComList")
        self.topView.addWidget(self.cbComList)
        self.cbBaudList = QtWidgets.QComboBox(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbBaudList.sizePolicy().hasHeightForWidth())
        self.cbBaudList.setSizePolicy(sizePolicy)
        self.cbBaudList.setObjectName("cbBaudList")
        self.topView.addWidget(self.cbBaudList)
        self.btnConnect = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnConnect.sizePolicy().hasHeightForWidth())
        self.btnConnect.setSizePolicy(sizePolicy)
        self.btnConnect.setObjectName("btnConnect")
        self.topView.addWidget(self.btnConnect)
        self.btnDisconnect = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDisconnect.sizePolicy().hasHeightForWidth())
        self.btnDisconnect.setSizePolicy(sizePolicy)
        self.btnDisconnect.setObjectName("btnDisconnect")
        self.topView.addWidget(self.btnDisconnect)
        self.top.addLayout(self.topView)
        self.view.addLayout(self.top)
        self.line_8 = QtWidgets.QFrame(self.model)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.view.addWidget(self.line_8)
        self.label_3 = QtWidgets.QLabel(self.model)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.view.addWidget(self.label_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_6 = QtWidgets.QLabel(self.model)
        self.lbl_6.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lbl_6.setObjectName("lbl_6")
        self.verticalLayout.addWidget(self.lbl_6)
        self.line_2 = QtWidgets.QFrame(self.model)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.mid = QtWidgets.QGridLayout()
        self.mid.setObjectName("mid")
        self.lbl_4 = QtWidgets.QLabel(self.model)
        self.lbl_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_4.setObjectName("lbl_4")
        self.mid.addWidget(self.lbl_4, 1, 2, 1, 1)
        self.lbl_1 = QtWidgets.QLabel(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_1.sizePolicy().hasHeightForWidth())
        self.lbl_1.setSizePolicy(sizePolicy)
        self.lbl_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_1.setObjectName("lbl_1")
        self.mid.addWidget(self.lbl_1, 2, 0, 1, 1)
        self.lbl_temp = QtWidgets.QLabel(self.model)
        self.lbl_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_temp.setObjectName("lbl_temp")
        self.mid.addWidget(self.lbl_temp, 2, 1, 1, 1)
        self.lbl_air = QtWidgets.QLabel(self.model)
        self.lbl_air.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_air.setObjectName("lbl_air")
        self.mid.addWidget(self.lbl_air, 3, 1, 1, 1)
        self.dsb_temp = QtWidgets.QDoubleSpinBox(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsb_temp.sizePolicy().hasHeightForWidth())
        self.dsb_temp.setSizePolicy(sizePolicy)
        self.dsb_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_temp.setObjectName("dsb_temp")
        self.mid.addWidget(self.dsb_temp, 2, 2, 1, 1)
        self.lbl_3 = QtWidgets.QLabel(self.model)
        self.lbl_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_3.setObjectName("lbl_3")
        self.mid.addWidget(self.lbl_3, 1, 1, 1, 1)
        self.dsb_air = QtWidgets.QDoubleSpinBox(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsb_air.sizePolicy().hasHeightForWidth())
        self.dsb_air.setSizePolicy(sizePolicy)
        self.dsb_air.setAlignment(QtCore.Qt.AlignCenter)
        self.dsb_air.setMaximum(100000.0)
        self.dsb_air.setObjectName("dsb_air")
        self.mid.addWidget(self.dsb_air, 3, 2, 1, 1)
        self.lbl_2 = QtWidgets.QLabel(self.model)
        self.lbl_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_2.setObjectName("lbl_2")
        self.mid.addWidget(self.lbl_2, 3, 0, 1, 1)
        self.btn_temp = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_temp.sizePolicy().hasHeightForWidth())
        self.btn_temp.setSizePolicy(sizePolicy)
        self.btn_temp.setObjectName("btn_temp")
        self.mid.addWidget(self.btn_temp, 2, 3, 1, 1)
        self.btn_air = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_air.sizePolicy().hasHeightForWidth())
        self.btn_air.setSizePolicy(sizePolicy)
        self.btn_air.setObjectName("btn_air")
        self.mid.addWidget(self.btn_air, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.mid)
        self.line_7 = QtWidgets.QFrame(self.model)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout.addWidget(self.line_7)
        self.view.addLayout(self.verticalLayout)
        self.label_2 = QtWidgets.QLabel(self.model)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.view.addWidget(self.label_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_7 = QtWidgets.QLabel(self.model)
        self.lbl_7.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lbl_7.setObjectName("lbl_7")
        self.verticalLayout_2.addWidget(self.lbl_7)
        self.line = QtWidgets.QFrame(self.model)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.bot_1 = QtWidgets.QHBoxLayout()
        self.bot_1.setObjectName("bot_1")
        self.btnStop = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy)
        self.btnStop.setObjectName("btnStop")
        self.bot_1.addWidget(self.btnStop)
        self.btnStart = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy)
        self.btnStart.setObjectName("btnStart")
        self.bot_1.addWidget(self.btnStart)
        self.verticalLayout_2.addLayout(self.bot_1)
        self.line_6 = QtWidgets.QFrame(self.model)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_2.addWidget(self.line_6)
        self.label = QtWidgets.QLabel(self.model)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lbl_8 = QtWidgets.QLabel(self.model)
        self.lbl_8.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lbl_8.setObjectName("lbl_8")
        self.verticalLayout_2.addWidget(self.lbl_8)
        self.line_3 = QtWidgets.QFrame(self.model)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.bot_2 = QtWidgets.QHBoxLayout()
        self.bot_2.setObjectName("bot_2")
        self.btnApt = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnApt.sizePolicy().hasHeightForWidth())
        self.btnApt.setSizePolicy(sizePolicy)
        self.btnApt.setObjectName("btnApt")
        self.bot_2.addWidget(self.btnApt)
        self.btnCam = QtWidgets.QPushButton(self.model)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCam.sizePolicy().hasHeightForWidth())
        self.btnCam.setSizePolicy(sizePolicy)
        self.btnCam.setObjectName("btnCam")
        self.bot_2.addWidget(self.btnCam)
        self.verticalLayout_2.addLayout(self.bot_2)
        self.line_5 = QtWidgets.QFrame(self.model)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_2.addWidget(self.line_5)
        self.view.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.view)
        MainWindow.setCentralWidget(self.model)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "incubator"))
        self.lbl_5.setText(_translate("MainWindow", "Arduino Control Panel"))
        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.btnDisconnect.setText(_translate("MainWindow", "Close"))
        self.lbl_6.setText(_translate("MainWindow", "Sensor Setup"))
        self.lbl_4.setText(_translate("MainWindow", "Threshold"))
        self.lbl_1.setText(_translate("MainWindow", "Temp:"))
        self.lbl_temp.setText(_translate("MainWindow", "XXXX"))
        self.lbl_air.setText(_translate("MainWindow", "XXXX"))
        self.lbl_3.setText(_translate("MainWindow", "Current Value"))
        self.lbl_2.setText(_translate("MainWindow", "CO2:"))
        self.btn_temp.setText(_translate("MainWindow", "Set"))
        self.btn_air.setText(_translate("MainWindow", "Set"))
        self.lbl_7.setText(_translate("MainWindow", "Sensor Log"))
        self.btnStop.setText(_translate("MainWindow", "Stop Log"))
        self.btnStart.setText(_translate("MainWindow", "Start Log"))
        self.lbl_8.setText(_translate("MainWindow", "Integrated Function"))
        self.btnApt.setText(_translate("MainWindow", "APT"))
        self.btnCam.setText(_translate("MainWindow", "Camera"))
