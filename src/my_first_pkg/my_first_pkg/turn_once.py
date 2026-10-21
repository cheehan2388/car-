import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurnOnce(Node):
    def __init__(self):
        super().__init__('turn_once')                      # node 的名字
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.speed = 1.0                                   # 角速度 rad/s
        self.duration = 2 * math.pi / self.speed           # 轉一圈要幾秒
        self.start = self.get_clock().now()                # 記下開始時間

        self.timer = self.create_timer(0.1, self.tick)     # 每 0.1 秒呼叫 tick

    def tick(self):
        elapsed = (self.get_clock().now() - self.start).nanoseconds / 1e9
        msg = Twist()

        if elapsed < self.duration:
            msg.angular.z = self.speed                     # 還沒轉完：繼續轉
            self.pub.publish(msg)
        else:
            self.pub.publish(msg)                          # msg 全是 0 = 停止
            self.get_logger().info('轉完一圈了，按 Ctrl+C 結束')
            self.timer.cancel()                            # 不再呼叫 tick


def main():
    rclpy.init()
    node = TurnOnce()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()