import sys
from ctypes import *
sys.path.append('build')

import radar_modules


dir(radar_modules)

radar = radar_modules.MR76()


radar.parse_data(1,8, 20,20,20,20,20,20,20,20)
print(radar.distance_long)