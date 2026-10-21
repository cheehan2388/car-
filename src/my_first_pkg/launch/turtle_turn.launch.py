from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),
        Node(
            package='my_first_pkg',
            executable='turn_precise',
            parameters=[{'laps': 2, 'speed': 1.5}],
            output='screen',
        ),
    ])
