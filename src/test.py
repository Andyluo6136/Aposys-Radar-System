# # import sys
# # from ctypes import *
# # sys.path.append('build')

# # import radar_modules


# # dir(radar_modules)

# # radar = radar_modules.MR76()
# # data = radar_modules.mr76_data()

# # radar.parse_data(1,8, 20,20,20,20,20,20,20,20)
# # print(radar.object1[0].id)





import rclpy
from ros_files.ros_files.rviz_node import rviz_node
import time
rclpy.init()
node = rviz_node()
while True:
    node.publish_marker(0.0,0.0,3)
    print("s")

    rclpy.spin_once(node, timeout_sec=0)
    node.publish_marker(2.0,0.0,1)

    node.delete(1)

    rclpy.spin_once(node, timeout_sec=0)
    time.sleep(0.5)
rclpy.shutdown()


