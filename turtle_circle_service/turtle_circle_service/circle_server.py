import rclpy                                      # ROS client library for Python
from rclpy.node import Node                       # Base Node class
from geometry_msgs.msg import Twist               # Message to control turtle motion
from turtle_interfaces.srv import DrawCircle      # Custom service definition
import math, time                                 # Math and time functions

# Define a class that inherits from Node
class CircleServer(Node):
    def __init__(self):
        super().__init__('circle_server')  # Initialize the node with a name

        # Create a service named 'draw_circle' using the DrawCircle interface
        self.srv = self.create_service(DrawCircle, 'draw_circle', self.draw_callback)

        # Create a publisher to publish velocity commands to the turtle
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.get_logger().info('Circle Service Server Ready')  # Log server readiness

    # Callback that runs when the service is called
    def draw_callback(self, request, response):
        radius = request.radius     # Extract requested radius
        repeat = request.repeat     # Extract requested repeat count

        if radius <= 0 or repeat <= 0:
            self.get_logger().warn('Invalid input values!')
            response.success = False
            return response

        vel = Twist()  # Create Twist message for velocity
        vel.linear.x = 1.0  # Set linear velocity
        vel.angular.z = vel.linear.x / radius  # Calculate angular velocity to draw a circle
        time_per_circle = (2 * math.pi * radius) / vel.linear.x  # Time for one full circle

        for i in range(repeat):
            self.get_logger().info(f'Drawing circle {i+1}')
            start_time = time.time()
            while time.time() - start_time < time_per_circle:
                self.publisher.publish(vel)
                time.sleep(0.05)  # Small delay to control publish rate

        self.publisher.publish(Twist())  # Stop the turtle after drawing
        response.success = True          # Mark success
        return response

def main():
    rclpy.init()
    node = CircleServer()
    rclpy.spin(node)  # Keep the node alive
    rclpy.shutdown()