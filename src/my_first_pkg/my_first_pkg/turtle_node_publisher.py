import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.count = 0

    def tick(self):
        msg = String()
        msg.data = f'hello {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(msg.data)
        self.count += 1


def main():
    rclpy.init()
    node = MyPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
