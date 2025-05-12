import sys
import usbcan
from ctypes import *
import threading
sys.path.append('build')

import radar_modules


dir(radar_modules)

rar = radar_modules.MR76()


lib = cdll.LoadLibrary("./libusbcan.so")

USBCAN_I = c_uint32(3)   # USBCAN-I/I+ 3
USBCAN_II = c_uint32(4)  # USBCAN-II/II+ 4
MAX_CHANNELS = 2         # Maximum number of channels
g_thd_run = 1            # Thread running flag


threads = []
# The baud rate is a hexadecimal number that can be calculated using the "zcanpro baud rate calculator"
gBaud = 0x1c00          # Baud rate 0x1400-1M(75%), 0x1c00-500k(87.5%), 0x1c01-250k(87.5%), 0x1c03-125k(87.5%)
DevType = USBCAN_II     # Device type number
DevIdx = 0              # Device index number


# Turn on the device
ret = lib.VCI_OpenDevice(DevType, DevIdx, 0)   # Device type, device index, reserved parameters
if ret == 0:
    print("Open device fail")
    exit(0)
else:
    print("Opendevice success")


# Get device information
# info = GetDeviceInf(USBCAN_II, 0)
# print("Devcie Infomation:\n%s" % (info))

# Initialize and start the channel
print(MAX_CHANNELS)
for i in range(usbcan.MAX_CHANNELS):
    init_config = usbcan.ZCAN_CAN_INIT_CONFIG()
    init_config.AccCode = 0
    init_config.AccMask = 0xFFFFFFFF
    init_config.Reserved = 0
    init_config.Filter = 1
    init_config.Timing0 = 0x1c00 & 0xff
    init_config.Timing1 = 0x1c00 >> 8
    init_config.Mode = 0
    ret = lib.VCI_InitCAN(DevType, 0, i, byref(init_config))
    if ret == 0:
        print("InitCAN(%d) fail" % i)
    else:
        print("InitCAN(%d) success" % i)

    ret = lib.VCI_StartCAN(DevType, 0, i)
    if ret == 0:
        print("StartCAN(%d) fail" % i)
    else:
        print("StartCAN(%d) success" % i)
        
    thread = threading.Thread(target=usbcan.rx_thread, args=(DevType, DevIdx, i,))
    threads.append(thread) # independent receiving thread
    thread.start()

# Test sending
send_len = 10  # Number of frames sent
msgs = (usbcan.ZCAN_CAN_OBJ * send_len)()
for i in range(send_len):
    msgs[i].ID = 0x100
    msgs[i].SendType = 0    # Sending mode 0-Normal, 1-Single, 2-Self-send and self-receive
    msgs[i].RemoteFlag = 0  # 0-Data frame 1-Remote frame
    msgs[i].ExternFlag = 0  # 0-Standard frame 1-Extended frame
    msgs[i].DataLen = 8     # Data length 1~8
    for j in range(msgs[i].DataLen):
        msgs[i].Data[j] = j
send_ret = lib.VCI_Transmit(DevType, 0, 0, byref(msgs), send_len)

if send_len == send_ret:
    print("Transmit success, sendcount is: %d " % send_ret)
else:
    print("Transmit fail, sendcounet is: %d " % send_ret)

# blocking wait
input()
g_thd_run = 0

# Wait for all threads to complete
for thread in threads:
    thread.join()

# reset channel
for i in range(usbcan.MAX_CHANNELS):
    ret = lib.VCI_ResetCAN(DevType, DevIdx, i)
    if ret == 0:
        print("ResetCAN(%d) fail" % i)
    else:
        print("ResetCAN(%d) success" % i)

# Turn off the device
ret = lib.VCI_CloseDevice(DevType, DevIdx)
if ret == 0:
    print("Closedevice fail")
else:
    print("Closedevice success")
del lib