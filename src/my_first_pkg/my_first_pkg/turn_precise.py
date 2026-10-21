import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def normalize(angle):
    """把角度差限制在 -pi ~ pi，避免 3.14 跳到 -3.14 時算錯"""
    return math.atan2(math.sin(angle), math.cos(angle))


class TurnPrecise(Node):
    def __init__(self):
        super().__init__('turn_precise')

        # 旋鈕：宣告並讀取
        self.declare_parameter('speed', 1.0)
        self.declare_parameter('laps', 1)
        self.speed = self.get_parameter('speed').value
        self.target = self.get_parameter('laps').value * 2 * math.pi

        # 狀態：里程表
        self.last_theta = None
        self.turned = 0.0

        # 最後才建立發布、訂閱、計時器
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(0.05, self.control_loop)

    def pose_callback(self, msg):
        if self.last_theta is not None:
            self.turned += normalize(msg.theta - self.last_theta)
        self.last_theta = msg.theta

    def control_loop(self):
        if self.last_theta is None:
            return

        msg = Twist()
        if self.turned < self.target:
            msg.angular.z = self.speed
            self.get_logger().info(
                f'已轉 {math.degrees(self.turned):.1f} 度',
                throttle_duration_sec=1.0)
        else:
            self.get_logger().info(
                f'完成，共轉了 {math.degrees(self.turned):.1f} 度')
            self.timer.cancel()

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = TurnPrecise()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
