import sys
import usbcan
from ctypes import *
import threading
import radar_modules

sys.path.append("build")

dir(radar_modules)

rar = radar_modules.MR76()


lib = cdll.LoadLibrary("./libusbcan.so")

USBCAN_I = c_uint32(3)   # USBCAN-I/I+ 3
USBCAN_II = c_uint32(4)  # USBCAN-II/II+ 4
MAX_CHANNELS = 2         # 通道最大数量
g_thd_run = 1            # 线程运行标志


threads = []
# 波特率这里的十六进制数字，可以由“zcanpro 波特率计算器”计算得出
gBaud = 0x1c00          # 波特率 0x1400-1M(75%), 0x1c00-500k(87.5%), 0x1c01-250k(87.5%), 0x1c03-125k(87.5%)
DevType = USBCAN_II     # 设备类型号
DevIdx = 0              # 设备索引号

# 打开设备
ret = lib.VCI_OpenDevice(DevType, DevIdx, 0)   # 设备类型，设备索引，保留参数
if ret == 0:
    print("Open device fail")
    exit(0)
else:
    print("Opendevice success")


# # 获取设备信息
# info = GetDeviceInf(USBCAN_II, 0)
# print("Devcie Infomation:\n%s" % (info))

# 初始化，启动通道
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
    threads.append(thread) # 独立接收线程
    thread.start()

# 测试发送
send_len = 10  # 发送帧数量
msgs = (usbcan.ZCAN_CAN_OBJ * send_len)()
for i in range(send_len):
    msgs[i].ID = 0x100
    msgs[i].SendType = 0    # 发送方式 0-正常, 1-单次, 2-自发自收
    msgs[i].RemoteFlag = 0  # 0-数据帧 1-远程帧
    msgs[i].ExternFlag = 0  # 0-标准帧 1-扩展帧
    msgs[i].DataLen = 8     # 数据长度 1~8
    for j in range(msgs[i].DataLen):
        msgs[i].Data[j] = j
send_ret = lib.VCI_Transmit(DevType, 0, 0, byref(msgs), send_len)

if send_len == send_ret:
    print("Transmit success, sendcount is: %d " % send_ret)
else:
    print("Transmit fail, sendcounet is: %d " % send_ret)

# 阻塞等待
input()
g_thd_run = 0

# 等待所有线程完成
for thread in threads:
    thread.join()

# 复位通道
for i in range(usbcan.MAX_CHANNELS):
    ret = lib.VCI_ResetCAN(DevType, DevIdx, i)
    if ret == 0:
        print("ResetCAN(%d) fail" % i)
    else:
        print("ResetCAN(%d) success" % i)

# 关闭设备
ret = lib.VCI_CloseDevice(DevType, DevIdx)
if ret == 0:
    print("Closedevice fail")
else:
    print("Closedevice success")
del lib