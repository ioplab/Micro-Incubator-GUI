import cv2
import os
import sys
import time
from configparser import ConfigParser

from Ui.Ui_winApt import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets

from PyAPT.PyAPT import APTMotor

global CCD_IMAGE


def print_info(func):
    def wrapper(*args, **kargs):
        cfg = func(*args, **kargs)
        for k, v in cfg.items():
            print('{:16s} {}'.format( k,str(v) ) )
        return cfg
    return wrapper


@print_info
def load_cfg(cfg_file):
    def null_proc(text):
        if text in ['None','Null','none','null']:
            return 'None'
        else: return text
        
    config = {}
    f = ConfigParser()
    f.read(cfg_file, encoding="utf-8")
    sections = f.sections()
    print(sections)
    
    for section in sections:
        config[section] = {}
        options = f.options(section)
        for op in options:
            config[section][op] = null_proc(f.get(section, op))
    
    return config


class MyStage(QtCore.QThread):
    set_update_pos = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None, verbose=None):
        super().__init__(parent)
        self._Motor_x = APTMotor(verbose=verbose)
        self._Motor_y = APTMotor(verbose=verbose)
        self.serial_x = 0
        self.serial_y = 0
        self.mode = ''
        self.rel_distance = 0
        self.abs_distance_x = 55
        self.abs_distance_y = 37
        self.step_x = 0
        self.step_y = 0
        self.stride_x = 0
        self.stride_y = 0
        self.config = None
        self.auto_close = False

    def run(self):
        if self.mode == 'home':
            self._Motor_x.go_home()
            self._Motor_y.go_home()
            # Update text to show position
            self.set_update_pos.emit(self._Motor_x.getPos(), self._Motor_y.getPos())
        elif self.mode == 'rel_x':
            self._Motor_x.mRel(self.rel_distance)
            # Update text to show position
            self.set_update_pos.emit(self._Motor_x.getPos(), self._Motor_y.getPos())
        elif self.mode == 'rel_y':
            self._Motor_y.mRel(self.rel_distance)
            # Update text to show position
            self.set_update_pos.emit(self._Motor_x.getPos(), self._Motor_y.getPos())
        elif self.mode == 'abs':
            self._Motor_x.mAbs(self.abs_distance_x)
            self._Motor_y.mAbs(self.abs_distance_y)
        elif self.mode == 'auto':
            global CCD_IMAGE
            self.auto_close = False
            auto = self.config["auto"]
            print(self.config.keys())
            nb_pt = len(self.config.keys())-1
            freq = int(auto["freq"]) * nb_pt
            stay = int(auto["stay"])
            print("total:", freq, "nb_pt", nb_pt, "stay", stay)
            for i in range(freq):
                self.abs_distance_x = int(self.config["position_%d"%(i%nb_pt)]["x"])
                self.abs_distance_y = int(self.config["position_%d"%(i%nb_pt)]["y"])
                print("freq:", i, "x:", self.abs_distance_x, "y", self.abs_distance_y)
                self._Motor_x.mAbs(self.abs_distance_x)
                self._Motor_y.mAbs(self.abs_distance_y)
                self.set_update_pos.emit(self._Motor_x.getPos(), self._Motor_y.getPos())
                time.sleep(stay)
                savepath = self.config["position_%d"%(i%nb_pt)]["path"]
                os.makedirs(savepath, exist_ok=True)
                cv2.imwrite(os.path.join(savepath, "%06d.bmp"%i), CCD_IMAGE)
                if self.auto_close:
                    break
            print("Finished!!!!!!!!!!!!!!")

        self.mode = ''

    def connect_apt(self):
        self._Motor_x.setSerialNumber(self.serial_x)
        self._Motor_x.initializeHardwareDevice()
        self._Motor_y.setSerialNumber(self.serial_y)
        self._Motor_y.initializeHardwareDevice()

    def go_home(self):
        self._Motor_x.go_home()
        self._Motor_y.go_home()

    def move_rel_x(self, rel_distance):
        self._Motor_x.mRel(rel_distance)

    def move_rel_y(self, rel_distance):
        self._Motor_y.mRel(rel_distance)

    def move_abs_x(self, abs_distance):
        self._Motor_x.mAbs(abs_distance)

    def move_abs_y(self, abs_distance):
        self._Motor_y.mAbs(abs_distance)

    def get_pos_x(self):
        return self._Motor_x.getPos()

    def get_pos_y(self):
        return self._Motor_y.getPos()

    def get_vel_x(self):
        return self._Motor_x.getVelocityParameters()

    def get_vel_y(self):
        return self._Motor_y.getVelocityParameters()

    def get_info_x(self):
        return self._Motor_x.getStageAxisInformation()

    def get_info_y(self):
        return self._Motor_y.getStageAxisInformation()

    def set_vel_x(self, vel_x):
        self._Motor_x.setVel(vel_x)

    def set_vel_y(self, vel_y):
        self._Motor_y.setVel(vel_y)


class AptWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(AptWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.config = None
        self.camView = None

        # APT panel init UI
        self.stage = MyStage()
        self.stage.set_update_pos.connect(self.update_pos)
        self.btn_connect.setCheckable(True)
        self.btn_connect.clicked[bool].connect(self.connect_apt)
        self.btn_go_pos.clicked.connect(self.mot_abs)
        self.btn_go_vel.clicked.connect(self.set_vel_x_y)
        self.btn_home.clicked.connect(self.home)
        self.btn_up.clicked.connect(lambda: self.mot_rel_y(float(self.txt_stride_y.text())))
        self.btn_down.clicked.connect(lambda: self.mot_rel_y(-float(self.txt_stride_y.text())))
        self.btn_left.clicked.connect(lambda: self.mot_rel_x(-float(self.txt_stride_x.text())))
        self.btn_right.clicked.connect(lambda: self.mot_rel_x(float(self.txt_stride_x.text())))
        self.btn_openAutoFile.clicked.connect(self.getAutoFile)
        self.btn_AutoStart.clicked.connect(self.onAutoStart)
        self.btn_AutoClose.clicked.connect(self.onAutoClose)
        
    def _enable_func(self, enable):
        self.txt_serial_x.setEnabled(not enable)
        self.txt_serial_y.setEnabled(not enable)
        self.txt_pos_x.setEnabled(enable)
        self.txt_pos_y.setEnabled(enable)
        self.txt_vel_x.setEnabled(enable)
        self.txt_vel_y.setEnabled(enable)
        self.txt_stride_x.setEnabled(enable)
        self.txt_stride_y.setEnabled(enable)
        self.btn_home.setEnabled(enable)
        self.btn_up.setEnabled(enable)
        self.btn_down.setEnabled(enable)
        self.btn_right.setEnabled(enable)
        self.btn_left.setEnabled(enable)
        self.btn_go_pos.setEnabled(enable)
        self.btn_go_vel.setEnabled(enable)
        self.btn_openAutoFile.setEnabled(enable)
        self.btn_AutoStart.setEnabled(enable)
        self.btn_AutoClose.setEnabled(enable)
    
    def closeEvent(self, event):
        self.connectSignal(False)
        self.close()
    
    def connectCamView(self, camView):
        self.camView = camView
        if not self.camView.Camera:
            print("No camera.............")
            return
        print("Get camera!!")
        if self.camView.Camera.get_status():
            self.connectSignal(True)
            print("Get signal!!")
        else:
            print("Camera not connect...........")
            self.camView = None  # not connect, will remove
    
    def connectSignal(self, status):
        if not self.camView.Camera:
            print("No Signal.............")
            return
        if self.camView.Camera.get_status():
            if status:
                print("Connect \"self.apt.getImg\" to signal!!")
                self.camView.update_signal.connect(self.getImg)
            else:
                self.camView.update_signal.disconnect(self.getImg)
                print("Disconnect \"self.apt.getImg\" to signal..........")

    def getImg(self, image_data):
        global CCD_IMAGE
        CCD_IMAGE = image_data
        # print(image_data.shape)

    def connect_apt(self, pressed):
        if pressed:
            # APT Motor connect
            self.stage.serial_x = int(self.txt_serial_x.text())
            self.stage.serial_y = int(self.txt_serial_y.text())
            self.stage.connect_apt()
            self.btn_connect.setStyleSheet("background-color: green")
            self._enable_func(enable=True)

            # Update text to show position
            pos_x = self.stage.get_pos_x()
            pos_y = self.stage.get_pos_y()
            self.txt_pos_x.setValue(pos_x)
            self.txt_pos_y.setValue(pos_y)
            _, _, max_vel_x = self.stage.get_vel_x()
            _, _, max_vel_y = self.stage.get_vel_y()
            self.txt_vel_x.setValue(max_vel_x)
            self.txt_vel_y.setValue(max_vel_y)
            print('X position %f, Y position %f' % (pos_x, pos_y))
            print('X velocity %f, Y velocity %f' % (max_vel_x, max_vel_y))

            self.txt_stride_x.setValue(2.00)
            self.txt_stride_y.setValue(2.00)

            self.x_info = self.stage.get_info_x()
            self.y_info = self.stage.get_info_y()
            # print( self.x_info[ 1 ] , self.x_info[ 2 ] )
            # 110.0 1
            # print( self.y_info[ 1 ] , self.y_info[ 2 ] )
            # 75.0 1
            self.y_max = max(self.y_info[1], self.y_info[2])
            self.y_min = min(self.y_info[1], self.y_info[2])
            self.x_max = max(self.x_info[1], self.x_info[2])
            self.x_min = min(self.x_info[1], self.x_info[2])
            return True
        else:
            # APT Motor disconnect
            # Success
            self.btn_connect.setStyleSheet("background-color: gray")
            self._enable_func(enable=False)

            self.txt_pos_x.setValue(0.0000)
            self.txt_pos_y.setValue(0.0000)
            self.txt_vel_x.setValue(0.000)
            self.txt_vel_y.setValue(0.000)
            return True

    def update_pos(self, pos_x, pos_y):
        # Update text to show position
        self.txt_pos_x.setValue(pos_x)
        self.txt_pos_y.setValue(pos_y)

    def mot_rel_x(self, rel_distance):
        if self.x_min <= float(self.txt_pos_x.text()) + rel_distance <= self.x_max:
            # self.stage.move_rel_x(rel_distance)
            self.stage.rel_distance = rel_distance
            self.stage.mode = 'rel_x'
            self.stage.start()

    def mot_rel_y(self, rel_distance):
        if self.y_min <= float(self.txt_pos_y.text()) + rel_distance <= self.y_max:
            # self.stage.move_rel_y(rel_distance)
            self.stage.rel_distance = rel_distance
            self.stage.mode = 'rel_y'
            self.stage.start()

    def mot_abs(self):
        absDistance_x = float(self.txt_pos_x.text())
        absDistance_y = float(self.txt_pos_y.text())
        if self.x_min <= absDistance_x <= self.x_max and self.y_min <= absDistance_y <= self.y_max:
            # self.stage.move_abs_x(absDistance_x)
            # self.stage.move_abs_y(absDistance_y)
            self.stage.abs_distance_x = absDistance_x
            self.stage.abs_distance_y = absDistance_y
            self.stage.mode = 'abs'
            self.stage.start()

    def set_vel_x_y(self):
        self.stage.set_vel_x(float(self.txt_vel_x.text()))
        self.stage.set_vel_y(float(self.txt_vel_y.text()))

    def home(self):
        # self.stage.go_home()
        self.stage.mode = 'home'
        self.stage.start()

    def getAutoFile(self):
        cfgpath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "", os.getcwd(), "ini Files (*.ini)")
        if cfgpath == "":
            self.stage.config = None
            return
        print(cfgpath)
        self.stage.config = load_cfg(cfgpath)

    def onAutoStart(self):
        if not self.stage.config:
            return
        print("Start auto mode")
        self.stage.mode = 'auto'
        self.stage.start()

    def onAutoClose(self):
        if not self.stage.config:
            return
        print("Close auto mode")
        self.stage.auto_close = True



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = AptWindow()
    win.show()
    sys.exit(app.exec_())
