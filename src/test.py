import sys
from ctypes import *
sys.path.append('build')

import radar_modules


dir(radar_modules)

radar = radar_modules.MR76()
data = radar_modules.mr76_data()

radar.parse_data(1,8, 20,20,20,20,20,20,20,20)
print(radar.object1[0].distance_long)
