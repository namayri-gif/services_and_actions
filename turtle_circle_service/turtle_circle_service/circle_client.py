import rclpy                          # ROS 2 Python client
from rclpy.node import Node           # Node base class
from turtle_interfaces.srv import DrawCircle  # Custom service

# Define a node for the client
class CircleClient(Node):
    def __init__(self):
        super().__init__('circle_client')

        # Create a client for the 'draw_circle' service
        self.client = self.create_client(DrawCircle, 'draw_circle')

        # Wait until service is available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for draw_circle service...')

        self.send_request()  # Proceed to send request

    def send_request(self):
        req = DrawCircle.Request()  # Create a request object
        req.radius = float(input('Enter radius: '))
        req.repeat = int(input('How many circles?: '))

        # Call service asynchronously
        future = self.client.call_async(req)
        future.add_done_callback(self.callback)

    def callback(self, future):
        if future.result().success:
            self.get_logger().info('Circle drawing succeeded!')
        else:
            self.get_logger().info('Circle drawing failed.')

def main():
    rclpy.init()
    rclpy.spin(CircleClient())  # Run the client node
    rclpy.shutdown()