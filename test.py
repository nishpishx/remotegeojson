#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus
import math
import time

class FakeGPSPublisher(Node):
    def __init__(self):
        super().__init__('fake_gps_publisher')
        self.publisher_ = self.create_publisher(NavSatFix, '/gps/fix', 10)
        timer_period = 1.0 / 0.5  # 20 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.start_time = time.time()
        self.get_logger().info('Publishing fake NavSatFix at 20 Hz')

    def timer_callback(self):
        msg = NavSatFix()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'gps_link'

        # Fake position (simulate slow circular motion)
        t = time.time() - self.start_time
        msg.latitude  = 37.4219999 + 0.0001 * math.sin(t / 10.0)
        msg.longitude = -122.0840575 + 0.0001 * math.cos(t / 10.0)
        msg.altitude = 5.0 + 0.1 * math.sin(t / 5.0)

        msg.status.status = NavSatStatus.STATUS_FIX
        msg.status.service = NavSatStatus.SERVICE_GPS
        msg.position_covariance = [0.0] * 9
        msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FakeGPSPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
