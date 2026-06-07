#!/usr/bin/env python3
 
import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from numpy import linalg
from .utils import make_pointcloud2, declare_param
from sensor_msgs_py.point_cloud2 import read_points_numpy
from geometry_msgs.msg import PointStamped
 
class Clusterer(Node):
    def __init__(self):
        super().__init__("clusterer")
 
        declare_param(self, "k", 5)
        declare_param(self, "D", 0.2)
       
        declare_param(self, "min_cluster_points", 8)
 
        self.pub_centre=self.create_publisher(PointStamped,"objet_centre1",10)
        self.pub = self.create_publisher(PointCloud2, "clusters_all", 10)
        self.sub = self.create_subscription(PointCloud2, "points", self.callback, 10)
 
    def callback(self, msg: PointCloud2):
        points = read_points_numpy(msg, ["x", "y", "intensity", "clusterId"])
 
        if len(points) == 0:
            return;
 
        for i in range(0, len(points)):
            points[i, 3] = 0
           
        for i in range(0, len(points)):
            current_k = min(self.k, i)
            if current_k == 0:
                continue
               
            distance = np.zeros(current_k)
            for j in range(current_k):
                vec = points[i, :2] - points[i - j - 1, :2]
                distance[j] = np.linalg.norm(vec)
               
            if len(distance) > 0:
                dmin = np.min(distance)
                jmin = np.argmin(distance) + 1
                if dmin < self.D:
                    if points[i - jmin, 3] == 0:
                        points[i - jmin, 3] = np.max(points[:, 3]) + 1
                    points[i, 3] = points[i - jmin, 3]
 
        unique_clusters = [cid for cid in np.unique(points[:, 3]) if cid != 0]
 
        best_cluster_id = None
        max_points = 0
 
        for cluster_id in unique_clusters:
            nb_points = np.sum(points[:, 3] == cluster_id)
            if nb_points > max_points:
                max_points = nb_points
                best_cluster_id = cluster_id
 
        if best_cluster_id is not None and max_points >= self.min_cluster_points:
           
            cluster_mask = points[:, 3] == best_cluster_id
            cluster_points = points[cluster_mask]
 
            points[~cluster_mask, 3] = 0
 
            x_coords = cluster_points[:, 0]
            y_coords = cluster_points[:, 1]
 
            x_min, x_max = np.min(x_coords), np.max(x_coords)
            y_min, y_max = np.min(y_coords), np.max(y_coords)
 
            pos_x_centre = (x_min + x_max) / 2.0
            pos_y_centre = (y_min + y_max) / 2.0
            msg_centre1=PointStamped()
            msg_centre1.header=msg.header
            msg_centre1.point.x=float(pos_x_centre)
            msg_centre1.point.y=float(pos_y_centre)
            msg_centre1.point.z=0.0
            self.pub_centre.publish(msg_centre1)
           
           
        else:
            points[:, 3] = 0
            
 
        self.pub.publish(make_pointcloud2(msg.header, *points.T))
 
 
def main(args=None):
    rclpy.init(args=args)
    try:
        rclpy.spin(Clusterer())
    except KeyboardInterrupt:
        pass