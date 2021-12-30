from pyueye import ueye
from threading import Thread
from ctypes import byref


def get_bits_per_pixel(color_mode):
    """
    returns the number of bits per pixel for the given color mode
    raises exception if color mode is not is not in dict
    """
    
    return {
        ueye.IS_CM_SENSOR_RAW8: 8,
        ueye.IS_CM_SENSOR_RAW10: 16,
        ueye.IS_CM_SENSOR_RAW12: 16,
        ueye.IS_CM_SENSOR_RAW16: 16,
        ueye.IS_CM_MONO8: 8,
        ueye.IS_CM_RGB8_PACKED: 24,
        ueye.IS_CM_BGR8_PACKED: 24,
        ueye.IS_CM_RGBA8_PACKED: 32,
        ueye.IS_CM_BGRA8_PACKED: 32,
        ueye.IS_CM_BGR10_PACKED: 32,
        ueye.IS_CM_RGB10_PACKED: 32,
        ueye.IS_CM_BGRA12_UNPACKED: 64,
        ueye.IS_CM_BGR12_UNPACKED: 48,
        ueye.IS_CM_BGRY8_PACKED: 32,
        ueye.IS_CM_BGR565_PACKED: 16,
        ueye.IS_CM_BGR5_PACKED: 16,
        ueye.IS_CM_UYVY_PACKED: 16,
        ueye.IS_CM_UYVY_MONO_PACKED: 16,
        ueye.IS_CM_UYVY_BAYER_PACKED: 16,
        ueye.IS_CM_CBYCRY_PACKED: 16,        
    } [color_mode]


class uEyeException(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
    def __str__(self):
        return "Err: " + str(self.error_code)


def check(ret):
    if ret != ueye.IS_SUCCESS:
        raise uEyeException(ret)


class ImageBuffer:
    def __init__(self):
        self.mem_ptr = ueye.c_mem_p()
        self.mem_id = ueye.int()


class MemoryInfo:
    def __init__(self, h_cam, img_buff):
        self.x = ueye.int()
        self.y = ueye.int()
        self.bits = ueye.int()
        self.pitch = ueye.int()
        self.img_buff = img_buff

        rect_aoi = ueye.IS_RECT()
        check(ueye.is_AOI(h_cam,
                          ueye.IS_AOI_IMAGE_GET_AOI, rect_aoi, ueye.sizeof(rect_aoi)))
        self.width = rect_aoi.s32Width.value
        self.height = rect_aoi.s32Height.value
        
        check(ueye.is_InquireImageMem(h_cam,
                                      self.img_buff.mem_ptr,
                                      self.img_buff.mem_id, self.x, self.y, self.bits, self.pitch))


class ImageData:
    def __init__(self, h_cam, img_buff):
        self.h_cam = h_cam
        self.img_buff = img_buff
        self.mem_info = MemoryInfo(h_cam, img_buff)
        self.color_mode = ueye.is_SetColorMode(h_cam, ueye.IS_GET_COLOR_MODE)
        self.bits_per_pixel = get_bits_per_pixel(self.color_mode)
        self.array = ueye.get_data(self.img_buff.mem_ptr,
                                   self.mem_info.width,
                                   self.mem_info.height,
                                   self.mem_info.bits,
                                   self.mem_info.pitch,
                                   True)

    def as_1d_image(self):        
        channels = int((7 + self.bits_per_pixel) / 8)
        import numpy
        if channels > 1:
            return numpy.reshape(self.array, (self.mem_info.height, self.mem_info.width, channels))
        else:
            return numpy.reshape(self.array, (self.mem_info.height, self.mem_info.width))


    def unlock(self):
        check(ueye.is_UnlockSeqBuf(self.h_cam, self.img_buff.mem_id, self.img_buff.mem_ptr))

class Rect:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height



#------------------------------------------------------------------------------------#



class FrameThread(Thread):
    def __init__(self, cam, views=None, copy=True):
        super(FrameThread, self).__init__()
        self._running = True
        self.timeout = 1000
        self.cam = cam
        self.views = views
        self.copy = copy

    def run(self):
        self._running = True
        while self._running:
            img_buffer = ImageBuffer()
            ret = ueye.is_WaitForNextImage(self.cam.handle(),
                                           self.timeout,
                                           img_buffer.mem_ptr,
                                           img_buffer.mem_id)
            if ret == ueye.IS_SUCCESS:
                self.notify(ImageData(self.cam.handle(), img_buffer))
            else:
                print("err.................")

        print("stop capture image from ueye")

    def notify(self, image_data):
        if self.views:
            if type(self.views) is not list:
                self.views = [self.views]
            for view in self.views:
                view.handle(image_data)

    def stop(self):
        self._running = False


#------------------------------------------------------------------------------------#


class Camera:
    def __init__(self, device_id=0):
        self.h_cam = ueye.HIDS(device_id)
        self.img_buffers = []
        self._connect = False

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, _type, value, traceback):
        self.exit()

    def get_status(self):
        return self._connect

    def handle(self):
        return self.h_cam

    def alloc(self, buffer_count=3):
        rect = self.get_aoi()
        bpp = get_bits_per_pixel(self.get_colormode())

        for buff in self.img_buffers:
            check(ueye.is_FreeImageMem(self.h_cam, buff.mem_ptr, buff.mem_id))

        for i in range(buffer_count):
            buff = ImageBuffer()
            ueye.is_AllocImageMem(self.h_cam,
                                  rect.width, rect.height, bpp,
                                  buff.mem_ptr, buff.mem_id)
            
            check(ueye.is_AddToSequence(self.h_cam, buff.mem_ptr, buff.mem_id))

            self.img_buffers.append(buff)

        ueye.is_InitImageQueue(self.h_cam, 0)

    def init(self):
        ret = ueye.is_InitCamera(self.h_cam, None)
        if ret != ueye.IS_SUCCESS:
            self.h_cam = None
            self._connect = False
            # raise uEyeException(ret)
        else:
            self._connect = True
        return ret

    def exit(self):
        ret = None
        if self.h_cam is not None:
            ret = ueye.is_ExitCamera(self.h_cam)
        if ret == ueye.IS_SUCCESS:
            self.h_cam = None
        self._connect = False

    def get_aoi(self):
        rect_aoi = ueye.IS_RECT()
        ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_GET_AOI, rect_aoi, ueye.sizeof(rect_aoi))

        return Rect(rect_aoi.s32X.value,
                    rect_aoi.s32Y.value,
                    rect_aoi.s32Width.value,
                    rect_aoi.s32Height.value)

    def set_aoi(self, x, y, width, height):
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(x)
        rect_aoi.s32Y = ueye.int(y)
        rect_aoi.s32Width = ueye.int(width)
        rect_aoi.s32Height = ueye.int(height)

        return ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))

    def capture_video(self, wait=False):
        wait_param = ueye.IS_WAIT if wait else ueye.IS_DONT_WAIT
        return ueye.is_CaptureVideo(self.h_cam, wait_param)

    def stop_video(self):
        return ueye.is_StopLiveVideo(self.h_cam, ueye.IS_FORCE_VIDEO_STOP)
    
    def freeze_video(self, wait=False):
        wait_param = ueye.IS_WAIT if wait else ueye.IS_DONT_WAIT
        return ueye.is_FreezeVideo(self.h_cam, wait_param)

    def set_colormode(self, colormode):
        check(ueye.is_SetColorMode(self.h_cam, colormode))
        
    def get_colormode(self):
        ret = ueye.is_SetColorMode(self.h_cam, ueye.IS_GET_COLOR_MODE)
        return ret

    def get_format_list(self):
        count = ueye.UINT()
        check(ueye.is_ImageFormat(self.h_cam, ueye.IMGFRMT_CMD_GET_NUM_ENTRIES, count, ueye.sizeof(count)))
        format_list = ueye.IMAGE_FORMAT_LIST(ueye.IMAGE_FORMAT_INFO * count.value)
        format_list.nSizeOfListEntry = ueye.sizeof(ueye.IMAGE_FORMAT_INFO)
        format_list.nNumListElements = count.value
        check(ueye.is_ImageFormat(self.h_cam, ueye.IMGFRMT_CMD_GET_LIST,
                                  format_list, ueye.sizeof(format_list)))
        return format_list
    
    #---- add ----#

    def set_PixelClock(self, mhz):
        mhz = ueye.UINT(mhz)
        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_SET, mhz, ueye.sizeof(mhz)))
        
    def get_PixelClock(self):
        mhz = ueye.UINT(0)
        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET, mhz, ueye.sizeof(mhz)))
        return mhz
        
    def get_PixelClockRange(self):
        class IS_STRUCT(ueye._Structure):
            _pack_ = 8
            _fields_ = [("pc%03d"%(i+1), ueye.UINT) for i in range(10)]
        
#        pc_default = ueye.UINT()
#        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET_DEFAULT, pc_default, ueye.sizeof(pc_default)))
        
        pc_num = ueye.UINT()
        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET_NUMBER, pc_num, ueye.sizeof(pc_num)))
        
        pc_list = [] ; cnt_num = 0
        pc_struct = IS_STRUCT()
        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET_LIST, pc_struct, pc_num*ueye.sizeof(ueye.UINT())))
        for field_name, _ in pc_struct._fields_:
            if cnt_num < pc_num:
                pc_list.append(int(getattr(pc_struct, field_name)))
                cnt_num += 1
            else: break
        
#        pc_s32range = ueye.IS_RANGE_S32()
#        check(ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET_RANGE, pc_s32range, ueye.sizeof(pc_s32range)))
        return pc_num, pc_list
        
    def set_FrameRate(self, rate):
        rate = ueye.DOUBLE(rate)
        newrate = ueye.DOUBLE()
        check(ueye.is_SetFrameRate(self.h_cam, rate, newrate))
        return newrate
        
    def set_Exposure(self, ms):
        ms = ueye.DOUBLE(ms)
        check(ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, ms, ueye.sizeof(ms)))
        return  ms
    
    def get_FrameTimeRange(self):
        min = ueye.DOUBLE()
        max = ueye.DOUBLE()
        intervall = ueye.DOUBLE()
        check(ueye.is_GetFrameTimeRange(self.h_cam, min, max, intervall))
        return min, max, intervall
    
    def get_FrameRate(self):
        rate = ueye.DOUBLE()
        check(ueye.is_GetFramesPerSecond(self.h_cam, rate))
        return rate
        
    def get_Exposure(self):
        ms = ueye.DOUBLE()
        check(ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, ms, ueye.sizeof(ms)))
        return ms
        
    def set_full_auto(self):
        enable = ueye.DOUBLE(1)
        zero = ueye.DOUBLE(0)
        ms = ueye.DOUBLE(20)
        rate = ueye.DOUBLE(50)
        newrate = ueye.DOUBLE()

        ret = ueye.is_SetAutoParameter(self.h_cam, ueye.IS_SET_ENABLE_AUTO_GAIN, enable, zero)
        ret = ueye.is_SetAutoParameter(self.h_cam, ueye.IS_SET_ENABLE_AUTO_SHUTTER, enable, zero)
        ret = ueye.is_SetFrameRate(self.h_cam, rate, newrate)
        ret = ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, ms, ueye.sizeof(ms))
        
        print("Auto mode")
        print('A_GAIN:',ret)
        print('A_SHUTTER:',ret)
        print('FR:',ret,newrate)
        print('EXP:',ret,ms)


