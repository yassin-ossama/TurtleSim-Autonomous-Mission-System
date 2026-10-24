#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.srv import SetDestination


class DestinationServer (Node): 
    def __init__(self):
        super().__init__("destination_server") 

        self.service=self.create_service(SetDestination,'validate_destination',self.validate_destination)

        self.get_logger().info("Validating date server is ready")

    def validate_destination (self,request,response):
        x=request.x
        y=request.y

        if 0 <= x <= 11 and 0 <= y <= 11 :
            response.valid=True
            response.message = "Destination is valid"
        else:
            response.valid=False
            response.message = "Invalid destination"

        return response


def main (args=None):
    rclpy.init(args=args)
    node= DestinationServer()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()