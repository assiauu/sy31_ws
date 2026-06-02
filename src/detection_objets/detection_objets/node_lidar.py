import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan #le type de message dans /scan il contient intensities ...etc
import numpy as np

class LidarNode(Node):
    def __init__(self):
        super().__init__('lidar_node') #nom nommer lidar_node
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.lidar_callback,
            10
        )

    #def lidar_callback(self, msg):