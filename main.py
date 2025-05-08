import sys
sys.path.append("build")

import radar_modules
dir(radar_modules)

rar = radar_modules.MR76()

print(rar.skip_cycle)