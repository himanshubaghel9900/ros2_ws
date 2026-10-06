from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    robot_description = ParameterValue(
        Command([
            'xacro ',
            '/home/himanshu/ros2_ws/src/ugv_description/urdf/ugv.urdf.xacro'
        ]),
        value_type=str
    )

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='ugv_description',
            executable='ugv_simulator',
            name='ugv_simulator'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2'
        ),
    ])
