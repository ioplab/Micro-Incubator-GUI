# Micro Incubator GUI by Arduino and Python

Make a Micro Incubator by Arduino. Using Python to create GUI.

---

## Python environment

- Python 3.7.10 (Anaconda3)
- pyueye
- numpy
- opencv-python
- PyQt5
- PyInstaller

---

## Arduino

- K type thermocouple sensor (Max6675)
- CO2 sensor (NDIRZ16)

---

## GUI

- Control Arduino UNO
- Log sensor value
- Open Thorlab motorized stage (APT)
- Open uEye camera

---

## uEye camera

- Can load parameter (by INI-File)
- View in real time
- Save current image
- Open and close camera

---

## APT stage

- Connect stage ([BBD203 - 3-Channel Benchtop 3-Phase Brushless DC Servo Controller](https://www.thorlabs.com/thorproduct.cfm?partnumber=BBD203))
- Set absolate position
- Manual move (relative position)
- Auto tour scanning (combine camera function)

---

## Refer

- [mcleu/PyAPT](https://github.com/mcleu/PyAPT)
- [pyueye](https://pypi.org/project/pyueye/)
- [如何透過 Python 使用 IDS uEye 相機？](https://pixoel.com.tw/techtips_details_22.html)

## SDK

- [APT Version 3.21.5](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=5066)
- [IDS Software Suite 4.94.2 WHQL (64-bit)](https://pixoel.com.tw/download.html)
- [Software | Arduino](https://www.arduino.cc/en/software)
