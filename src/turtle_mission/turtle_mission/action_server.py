#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import time
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.action import ActionServer , CancelResponse
from rclpy.action.server import ServerGoalHandle
from my_interfaces.action import NavigateTo



class NavigatServer (Node): 
    def __init__(self):
        super().__init__("navigate_server") 

        self.pose = None
        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10) 

        self.action_server = ActionServer(
            self,
            NavigateTo,
            "navigate_to",
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback
            )

        self.get_logger().info("NavigateTo action server is ready")

    def pose_callback(self, msg):
        self.pose = msg

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Cancellation requested")
        return CancelResponse.ACCEPT

    def execute_callback (self , goal_handle: ServerGoalHandle ):
        x = goal_handle.request.x
        y = goal_handle.request.y

        result = NavigateTo.Result()
        feedback = NavigateTo.Feedback()

        self.get_logger().info(f"Navigating to x={x}, y={y}")

        while rclpy.ok():

            if goal_handle.is_cancel_requested:
                self.stop_turtle()
                goal_handle.canceled()
                result.success = False
                result.message = "Navigation cancelled"
                return result

            if self.pose is None:
                time.sleep(0.1)
                continue

            dx = x - self.pose.x
            dy = y - self.pose.y

            distance = math.sqrt(dx**2 + dy**2)

            feedback.distance_remaining = distance
            goal_handle.publish_feedback(feedback)

            if distance < 0.1:
                self.stop_turtle()
                goal_handle.succeed()

                result.success = True
                result.message = "Destination reached"
                return result

            angle_to_goal = math.atan2(dy, dx)

            angle_error = math.atan2(
                math.sin(angle_to_goal - self.pose.theta),
                math.cos(angle_to_goal - self.pose.theta)
            )   

            cmd = Twist()

            cmd.angular.z = 2.0 * angle_error
    
            speed_factor = max(0.0, math.cos(angle_error))
            cmd.linear.x = min(1.5, 1.5 * distance * speed_factor)

            self.publisher.publish(cmd)

            time.sleep(0.1)

    def stop_turtle(self):
        self.publisher.publish(Twist())

    def destroy_node(self):
        self.stop_turtle()
        super().destroy_node()

def main (args=None):
    rclpy.init(args=args)
    node = NavigatServer()

    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()