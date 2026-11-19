# NOTE: i was gonna write a class here that gives you access to a framebuffer of the last published values
# import rclpy
#  kil me!!
# import threading


# import threading
# import pygame
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image

# class PygameImageViewer(Node):
#     def __init__(self):
#         super().__init__('pygame_image_viewer')
#         self.subscription = self.create_subscription(
#             Image, '/camera/image_raw', self.listener_callback, 10
#         )
#         self.latest_msg = None
#         self.lock = threading.Lock()

#     def listener_callback(self, msg):
#         if msg.encoding == 'rgb8':
#             with self.lock:
#                 self.latest_msg = msg

# def main():
#     rclpy.init()
#     node = PygameImageViewer()

#     # Spin ROS in a background thread so Pygame owns the main thread
#     spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
#     spin_thread.start()

#     pygame.init()
#     screen = None
#     clock = pygame.time.Clock()
#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         with node.lock:
#             msg = node.latest_msg
#             node.latest_msg = None

#         if msg is not None:
#             if screen is None:
#                 screen = pygame.display.set_mode((msg.width, msg.height))
            
#             surface = pygame.image.frombuffer(msg.data, (msg.width, msg.height), 'RGB')
#             screen.blit(surface, (0, 0))
#             pygame.display.flip()

#         clock.tick(60)

#     pygame.quit()
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
