import cv2
import os
import sys
import time
import numpy as np
from configparser import ConfigParser

from Ui.Ui_winCam import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets

from pyueye import ueye
from api_ueye import Camera
from api_ueye import FrameThread


def print_info(func):
    def wrapper(*args, **kargs):
        cfg = func(*args, **kargs)
        for k, v in cfg["Image size"].items():
            print('{:16s} {}'.format( k,str(v) ) )
        for k, v in cfg["Timing"].items():
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
    f.read(cfg_file, encoding="utf-8-sig")
    sections = f.sections()
    
    for section in sections:
        config[section] = {}
        options = f.options(section)
        for op in options:
            config[section][op] = null_proc(f.get(section, op))
    
    return config



class CamWindow(QtWidgets.QWidget, Ui_Form):

    update_signal = QtCore.pyqtSignal(np.ndarray, name="update_signal")

    def __init__(self, parent=None):
        super(CamWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.viewData.setScaledContents(True)
        
        self.view_x = self.view.horizontalScrollBar()
        self.view_y = self.view.verticalScrollBar()
        self.view.installEventFilter(self)
        self.last_move_x = 0
        self.last_move_y = 0
        self.frame_rate = 0
        self.exposure_val = 0
        self.config = None

        self.Camera = None
        self._switch_btn('stop')
        
        self.camBtn_open.clicked.connect(self.openCam)
        self.camBtn_stop.clicked.connect(self.stopCam)
        self.camBtn_save.clicked.connect(self.saveCam)
        self.camBtn_cfg.clicked.connect(self.loadCfg)
        
    def saveCam(self, image_data):
        if not self.Camera:
            print("No camera can close")
            return
        image = self.image
        savepath, _ = QtWidgets.QFileDialog.getSaveFileName(None, "", os.getcwd(), "bmp (*.bmp)")
        if savepath == "":
            return
        cv2.imwrite(savepath, image)

    def handle(self, image_data):
        self.frame_rate = self.Camera.get_FrameRate()
        self.exposure_val = self.Camera.get_Exposure()
        self.lbl_showInfo.setText("Frame Rate: %0.3f fps - Exposure Time:  %0.3f ms" % (self.frame_rate, self.exposure_val))
        self.image = image_data.as_1d_image()
        self.update_signal.emit(self.image)
        image_data.unlock()
    
    def loadCfg(self):
        cfgpath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "", os.getcwd(), "ini Files (*.ini)")
        if cfgpath == "":
            self.config = None
            return
        print(cfgpath)
        self.config = load_cfg(cfgpath)
        
    def openCam(self):
        self.Camera = Camera()
        self.Thread = FrameThread(self.Camera, self)
        ret = self.Camera.init()
        
        if ret != 3:
            self.Camera.set_colormode(ueye.IS_CM_SENSOR_RAW8)
            # self.Camera.set_colormode(ueye.IS_CM_BGR8_PACKED)
            if not self.config:
                self.Nx = 1280
                self.Ny = 1024
                self.Camera.set_aoi(0, 0, self.Nx, self.Ny)
                self.Camera.alloc()
            else:
                self.Nx = int(self.config["Image size"]["width"])
                self.Ny = int(self.config["Image size"]["height"])
                self.Camera.set_aoi(0, 0, self.Nx, self.Ny)
                self.Camera.alloc()
                self.Camera.set_PixelClock(int(self.config["Timing"]["pixelclock"]))
                self.frame_rate = self.Camera.set_FrameRate(float(self.config["Timing"]["framerate"]))
                self.exposure_val = self.Camera.set_Exposure(float(self.config["Timing"]["exposure"]))
                print("Frame Rate: %0.3f fps - Exposure Time:  %0.3f ms" % (self.frame_rate, self.exposure_val))
        
            self.Camera.capture_video()
            #---------#
            self.Thread.start()
            self.update_signal.connect(self.showData)
            self._switch_btn('open')
            print("connect to uEye......")
        else:
            self.Camera.exit()
            self.Thread.stop()
            self.Camera = None
            self._switch_btn('stop')
            print("Not wire to uEye......")

    def stopCam(self):
        if self.Camera.get_status():
            self.Thread.stop()
            self.Thread.join()
            self.Camera.stop_video()
            self.Camera.exit()
            self.Camera = None
            self._switch_btn('stop')
    
    def closeEvent(self, event):
        if not self.Camera:
            print("No camera can close")
        else:
            if self.Camera.get_status():
                self.Thread.stop()
                self.Thread.join()
                self.Camera.stop_video()
                self.Camera.exit()
            self.Camera = None
            print("Close camera")
        self.close()

    def showData(self, image):    
        qimg = QtGui.QImage(image.data,
                            image.shape[1],
                            image.shape[0],
                            QtGui.QImage.Format_Indexed8)    
        self.viewData.setScaledContents(True)
        self.viewData.setPixmap(QtGui.QPixmap.fromImage(qimg))
        if self.viewCbo_roi.currentIndex() == 0: roi_rate = 0.5
        elif self.viewCbo_roi.currentIndex() == 1: roi_rate = 0.75
        elif self.viewCbo_roi.currentIndex() == 2: roi_rate = 1
        elif self.viewCbo_roi.currentIndex() == 3: roi_rate = 1.25
        elif self.viewCbo_roi.currentIndex() == 4: roi_rate = 1.5
        else: pass
        self.viewForm.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewForm.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)

    def eventFilter(self, source, event):
        if source == self.view:
            if event.type() == QtCore.QEvent.MouseMove:
                if self.last_move_x == 0 or self.last_move_y == 0:
                    self.last_move_x = event.pos().x()
                    self.last_move_y = event.pos().y()
                distance_x = self.last_move_x - event.pos().x()
                distance_y = self.last_move_y - event.pos().y()
                self.view_x.setValue(self.view_x.value() + distance_x)
                self.view_y.setValue(self.view_y.value() + distance_y)
                self.last_move_x = event.pos().x()
                self.last_move_y = event.pos().y()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.last_move_x = 0
                self.last_move_y = 0
            return QtWidgets.QWidget.eventFilter(self, source, event)
    
    def _switch_btn(self, src):
        if src =='open':
            self.camBtn_open.setEnabled(False)
            self.camBtn_stop.setEnabled(True)
            self.camBtn_save.setEnabled(True)
            self.viewCbo_roi.setEnabled(True)
        elif src =='stop':
            self.camBtn_open.setEnabled(True)
            self.camBtn_stop.setEnabled(False)
            self.camBtn_save.setEnabled(False)
            self.viewCbo_roi.setEnabled(False)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = CamWindow()
    win.show()
    sys.exit(app.exec_())
