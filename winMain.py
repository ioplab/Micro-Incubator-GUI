"""
Micro Incubator GUI
A Software for observe bio sample living cycle.

Feature
-------
Provide Arduino control Panel
Allow control uEye camera interface
Allow control APT motorized scanning stage interface

See https://github.com/jacky10001/Micro-Incubator-GUI
Copyright (c), 2021, IOPLAB. All rights reserved.
"""

import sys

##### 取得時間戳
import time
from datetime import datetime

##### 保存資料用
from contextlib import redirect_stdout

##### Arduino 相關 (UART)
import serial

##### UI 相關
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui.Ui_winMain import Ui_MainWindow

##### CCD APT 相關
from winCam import CamWindow
from winApt import AptWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):    
    def __init__(self, parent=None):
        """
        初始化類別實例
         - 配置UI
         - 設定共用屬性
         - 初始化Serial傳輸功能
         - 連通UI上的按鈕功能
         - 呼叫CCD實例(uEye)
         - 呼叫APT實例(Stage)
         - 宣告計時器，用於讀取Sensor數值
        """

        ##### 繼承QtWidgets.QMainWindow及MainWindow類別實例的所有屬性及方法
        super(MainWindow, self).__init__(parent)

        ##### 配置UI
        self.setupUi(self)
        self.move(30, 30)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ##### 設定共用屬性
        self._timestamp = ""
        self._skip_first = True
        self._log_status = False
        
        ##### 初始化Serial傳輸功能，尋找可用裝置
        self.__setupSerial()

        ##### 連通UI上的按鈕功能
        self.btnConnect.clicked.connect(self.__connect)
        self.btnDisconnect.clicked.connect(self.__disconnect)
        self.btnStart.clicked.connect(self.__start)
        self.btnStop.clicked.connect(self.__stop)
        self.btn_temp.clicked.connect(self.temp_val)
        self.btn_air.clicked.connect(self.air_val)

        ##### 呼叫CCD實例(uEye)
        self.cam = CamWindow()
        self.btnCam.clicked.connect(self.__open_cam)

        ##### 呼叫APT實例(Stage)
        self.apt = AptWindow()
        self.btnApt.clicked.connect(self.__open_apt)

        ##### 宣告計時器，用於讀取Sensor數值
        self.timer = QtCore.QTimer()
        self.timer.stop()             # 初始化階段，暫停計時器功能
        self.timer.setInterval(1000)  # 間隔時間(單位:ms)
        self.timer.timeout.connect(self.read)

    def read(self):
        """ 讀取Sensor數值(使用計時器來讀取) """
        data = self.arduino.readline()  # 讀取Arduino的回傳值
        data = data.decode("utf-8")     # 對接收到的封包進行utf-8解碼
        data = data.replace("\r", "").replace("\n", "")  # 去掉無用字元
        data = data.split(",")          # 分離溫度、氣體資料

        ##### 比對資料完整性、並略過第一筆資料(通常第一筆資料有誤)
        if len(data) == 2 and not self._skip_first:
            ##### 比對資料是否為數值，否則不進行動作
            if data[0].replace(".", "").isdigit() and data[1].replace(".", "").isdigit():
                if self._log_status:  # 自動紀錄屬性為True，才會進行紀錄
                    with open("log-%s.csv"%self._timestamp, 'a') as f:
                        with redirect_stdout(f):
                            print("%s,%s"%(data[0],data[1]))
                # 即時更新UI上的數值
                self.lbl_temp.setText(data[0])
                self.lbl_air.setText(data[1])
        ##### 用於略過第一筆資料，以確保不會接收到異常封包
        if self._skip_first:
            self._skip_first = False
        
        ##### 清除Arduino暫存
        self.arduino.flushInput()

    def temp_val(self):
        """ 設定溫度門檻 """
        val = "t%4.2f"%self.dsb_temp.value()  # 取得UI上的數值
        self.arduino.write(val.encode("utf-8"))  # 傳輸數值至Arduino

    def air_val(self):
        """ 設定氣體門檻 """
        val = "a%4.2f"%self.dsb_air.value()  # 取得UI上的數值
        self.arduino.write(val.encode("utf-8"))  # 傳輸數值至Arduino

    def __open_cam(self):
        """ 開啟CCD UI """
        self.cam.show()

    def __open_apt(self):
        """ 開啟APT UI (同時連通CCD功能，用於掃描擷取影像) """
        self.apt.show()
        self.apt.connectCamView(self.cam)

    def __start(self):
        """ 開始自動記錄數值 """
        now = datetime.now()  # 取得時間戳
        self._timestamp = now.strftime("%Y%m%d-%H%M%S") 
        self._log_status = True  # 開啟自動記錄屬性

    def __stop(self):
        """ 停止記錄數值 """
        self._log_status = False  # 關閉自動記錄屬性

    def __connect(self):
        """ 連接Arduino功能 """
        port = self.cbComList.currentText()
        baud = self.cbBaudList.currentText()
        print("Connect to", port, " Baud Rate:",baud)
        self.arduino = serial.Serial(port, int(baud), timeout=2)
        time.sleep(0.01)
        self.timer.start()

    def __disconnect(self):
        """ 斷開Arduino功能 """
        self.arduino.close()
        self.timer.stop()
        self._skip_first = True
        self._log_status = False
        print("Disconnect arduino.")

    def __setupSerial(self):
        """ 初始化UART裝置 """
        ##### 設定可用的UART裝置
        ports = ["COM%d"%(i+1) for i in range(256)]
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.cbComList.addItem(port)
            except (OSError, serial.SerialException):
                pass
        ##### 設定包率
        for baud in ["9600","19200","38400","57600","74880","115200"]:
            self.cbBaudList.addItem(baud)
    
    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()


if __name__=='__main__':
    ##### 用於開啟UI的程式
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())