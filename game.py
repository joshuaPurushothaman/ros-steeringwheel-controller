import pygame

from fake_wheel import FakeWheel


class Game:
    def __init__(self):
        self.wheel = FakeWheel()
        # The wheel doesn't work if the video subsystem isn't initialized!
        self.screen = pygame.display.set_mode((0,0), pygame.NOFRAME | pygame.FULLSCREEN)
        pygame.display.set_caption("F1Tenth Steering Wheel Controller")

    def run_loop(self):
        running = True
        while running:
            # Process the event queue (required so Pygame updates internal key states)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if (
                pygame.key.get_pressed()[pygame.K_ESCAPE]
                or pygame.key.get_pressed()[pygame.K_q]
            ):
                running = False

            self.screen.fill((30, 30, 30))
            self._write_vals_to_screen()
            self._draw_camera_pov()
            pygame.display.flip()

    def _write_vals_to_screen(self):
        # Clear the screen with a dark background
        self.screen.fill((30, 30, 30))

        # Print the current steering angle, throttle, and brake values to the screen
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(
            f"steering: {self.wheel.get_steering_angle():+.2f}, throttle: {self.wheel.get_throttle():.2f}, brake: {self.wheel.get_brake():.2f}",
            True,
            "lightskyblue",
        )
        text_rect = text_surface.get_rect(center=(350, 20))
        self.screen.blit(text_surface, text_rect)

    def _draw_camera_pov(self):
        # surface = pygame.image.frombuffer(msg.data, (msg.width, msg.height), 'RGB')
        # screen.blit(surface, (0, 0))
