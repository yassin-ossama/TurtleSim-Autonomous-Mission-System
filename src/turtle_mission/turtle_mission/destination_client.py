#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_interfaces.srv import SetDestination
from my_interfaces.action import NavigateTo

class DestinationClient (Node): 
    def __init__(self):
        super().__init__("destination_client") 

        self.client= self.create_client(SetDestination,"validate_destination")

        self.action_client = ActionClient(
            self, 
            NavigateTo, 
            "navigate_to"
        )

        while not self.client.wait_for_service(timeout_sec=0.5):
            self.get_logger().info("Waiting for Validation server")

        x = float(input("Enter destination x: "))
        y = float(input("Enter destination y: "))
        self.send_destination(x, y)

    def send_destination(self,x,y):
        request = SetDestination.Request()
        request.x = x
        request.y = y

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self,future)

        if future.result() is not None:
            response = future.result()

            if response.valid:
                print('ACCEPTED:', response.message)
                self.send_goal(x, y)
            else:
                print('REJECTED:', response.message)
        else:
            print('Service call failed.')

    def send_goal(self,x,y):
        while not self.action_client.wait_for_server(timeout_sec=0.5):
            self.get_logger().info("Waiting for Navigation server")

        goal = NavigateTo.Goal()
        goal.x = x
        goal.y = y

        print("Sending navigation goal...")

        future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if goal_handle is None or not goal_handle.accepted:
            print("Navigation goal rejected.")
            return

        print("Navigation goal accepted.")

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        if result_future.result() is None:
            print("Failed to receive navigation result.")
            return
        
        result = result_future.result().result

        if result.success:
            print("SUCCESS:", result.message)

            choice = input(
                "Return to home position (5.5, 5.5)? (y/n): "
            ).strip().lower()

            if choice == "y":
                self.send_destination(5.5, 5.5)

            elif choice == "n":
                print("Goal ended.")

            else:
                print("Invalid choice. Goal ended.")

        else:
            print("FAILED:", result.message)
        


    
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        print(
            f"Distance remaining: "
            f"{feedback.distance_remaining:.2f}"
        )


def main (args=None):
    rclpy.init(args=args)
    node= DestinationClient()  
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()