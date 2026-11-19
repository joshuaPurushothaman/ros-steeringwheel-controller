import pygame

import moza_r5


class FakeWheel:
    def __init__(self):
        try:
            self.wheel = moza_r5.MozaR5(
                device_index=0,
                name_filter="",
                steering_axis=0,
                throttle_axis=2,
                brake_axis=5,
                wheel_range_degrees=900.0,
                steering_deadzone=0.05,
                pedal_range=(0.0, 1.0),
                invert_pedals=False,
            )

            print(f"FAKEWHEEL: Using joystick: {self.wheel.joystick.get_name()}")
        except RuntimeError:
            self.wheel = None
            pygame.init()
            print("FAKEWHEEL: No joystick found. Using fake joystick from keyboard.")

    def get_steering_angle(self):
        if self.wheel:
            return self.wheel.read().angle
        else:
            pygame.event.pump()
            return (
                pygame.key.get_pressed()[pygame.K_RIGHT]
                - pygame.key.get_pressed()[pygame.K_LEFT]
            )

    def get_throttle(self):
        if self.wheel:
            return self.wheel.read().throttle
        else:
            pygame.event.pump()
            return pygame.key.get_pressed()[pygame.K_UP]

    def get_brake(self):
        if self.wheel:
            return self.wheel.read().brake
        else:
            pygame.event.pump()
            return pygame.key.get_pressed()[pygame.K_DOWN]
