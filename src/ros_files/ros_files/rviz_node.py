import rclpy
import rclpy.logging
from rclpy.node import Node
from visualization_msgs.msg import Marker
import time

class rviz_node(Node):
    def __init__(self):
        super().__init__("point_publisher")
        self.logger = self.get_logger()
        self.marker_pub = self.create_publisher(Marker, "/visualization_marker", 10)

    def publish_marker(self, distance_long, distance_lat, id):

        # defines the point as part of the marker class
        point = Marker()

        point.header.frame_id = "/map"
        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        point.type = 2

        # need ID to differentiate between different points
        point.id = id

        # Set the scale of the marker
        point.scale.x = 1.0
        point.scale.y = 1.0
        point.scale.z = 0.0

        # Set the color
        point.color.r = 1.0
        point.color.g = 0.0
        point.color.b = 0.0
        point.color.a = 1.0

        # Set the pose of the marker
        point.pose.position.x = distance_long
        point.pose.position.y = distance_lat
        point.pose.position.z = 0.0
        point.pose.orientation.x = 0.0
        point.pose.orientation.y = 0.0
        point.pose.orientation.z = 0.0
        point.pose.orientation.w = 1.0

        # maybe to add text to the markers
        """text = Marker()
        text.header.frame_id = "map"

        text.id = 1
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD
        text.scale.z = 0.6  # Only z is used for text size
        text.color.r = 1.0
        text.color.g = 0.0
        text.color.b = 0.0
        text.color.a = 1.0
        text.pose.position.x = 1.0
        text.pose.position.y = 1.0
        text.pose.position.z = 1.6  # Lift text above cube
        text.pose.orientation.w = 1.0
        text.text = f"hello "


        self.marker_pub.publish(point)
        
        self.logger.info("2nd published")
        self.marker_pub.publish(text)"""

    def delete(self, id):
        marker = Marker()
        marker.id = id
        marker.action = Marker.DELETE
        self.marker_pub.publish(marker)


if __name__ == '__main__':
    rclpy.init(args=None)
    node = rviz_node()
    while True:
        node.publish_marker(0.0, 3.0, 1)
        node.publish_marker(0.0, 0.0, 2)
        
        rclpy.spin_once(node)

        time.sleep(0.5)
    rclpy.shutdown()
        
