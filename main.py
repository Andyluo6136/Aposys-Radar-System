import sys
import usbcan
sys.path.append("build")

import radar_modules
dir(radar_modules)

rar = radar_modules.MR76()


print(rar.object1[0].id)
