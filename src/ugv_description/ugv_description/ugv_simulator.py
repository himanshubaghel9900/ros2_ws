import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class UGVSimulator(Node):

    def __init__(self):
        super().__init__('ugv_simulator')

        # UGV dimensions
        self.wheel_radius = 0.18
        self.wheel_separation = 0.92

        # Robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Wheel positions
        self.left_wheel_position = 0.0
        self.right_wheel_position = 0.0

        # Current velocity
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        # ROS interfaces
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.joint_state_pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        # 50 Hz update loop
        self.timer = self.create_timer(
            0.02,
            self.update
        )

        self.last_time = self.get_clock().now()

        self.get_logger().info('UGV simulator started')

    def cmd_vel_callback(self, msg):
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def update(self):

        current_time = self.get_clock().now()

        dt = (
            current_time - self.last_time
        ).nanoseconds / 1e9

        self.last_time = current_time

        # Differential-drive wheel velocities
        left_velocity = (
            self.linear_velocity
            - (self.angular_velocity * self.wheel_separation / 2.0)
        ) / self.wheel_radius

        right_velocity = (
            self.linear_velocity
            + (self.angular_velocity * self.wheel_separation / 2.0)
        ) / self.wheel_radius

        # Wheel positions
        self.left_wheel_position += left_velocity * dt
        self.right_wheel_position += right_velocity * dt

        # Robot pose
        self.x += (
            self.linear_velocity
            * math.cos(self.theta)
            * dt
        )

        self.y += (
            self.linear_velocity
            * math.sin(self.theta)
            * dt
        )

        self.theta += self.angular_velocity * dt

        # Publish wheel joint states
        self.publish_joint_states(
            left_velocity,
            right_velocity,
            current_time
        )

        # Publish odom -> base_link
        self.publish_odom_tf(current_time)

    def publish_joint_states(
        self,
        left_velocity,
        right_velocity,
        current_time
    ):

        msg = JointState()

        msg.header.stamp = current_time.to_msg()

        msg.name = [
            'front_left_wheel_joint',
            'rear_left_wheel_joint',
            'front_right_wheel_joint',
            'rear_right_wheel_joint'
        ]

        msg.position = [
            self.left_wheel_position,
            self.left_wheel_position,
            self.right_wheel_position,
            self.right_wheel_position
        ]

        msg.velocity = [
            left_velocity,
            left_velocity,
            right_velocity,
            right_velocity
        ]

        self.joint_state_pub.publish(msg)

    def publish_odom_tf(self, current_time):

        transform = TransformStamped()

        transform.header.stamp = current_time.to_msg()

        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_link'

        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0

        # Convert yaw to quaternion
        transform.transform.rotation.z = math.sin(
            self.theta / 2.0
        )

        transform.transform.rotation.w = math.cos(
            self.theta / 2.0
        )

        self.tf_broadcaster.sendTransform(transform)


def main(args=None):

    rclpy.init(args=args)

    node = UGVSimulator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
