from dataclasses import dataclass
from typing import Self

import pygame


@dataclass(frozen=True)
class WheelState:
    angle: float
    angle_degrees: float
    throttle: float
    brake: float
    clutch: float
    raw_axes: tuple[float, ...]


class MozaR5:
    """Read steering and pedal state from a Pygame-supported wheel device."""

    def __init__(
        self,
        device_index: int = 0,
        name_filter: str = "MOZA",
        steering_axis: int = 0,
        throttle_axis: int = 1,
        brake_axis: int = 2,
        clutch_axis: int = 3,
        wheel_range_degrees: float = 900.0,
        steering_deadzone: float = 0.0,
        pedal_range: tuple[float, float] = (0.0, 1.0),
        invert_pedals: bool = False,
    ) -> None:
        if not 0.0 <= steering_deadzone < 1.0:
            raise ValueError("steering_deadzone must be in the range [0.0, 1.0)")
        if wheel_range_degrees <= 0.0:
            raise ValueError("wheel_range_degrees must be positive")

        pygame.init()
        pygame.joystick.init()

        count = pygame.joystick.get_count()
        if count == 0:
            raise RuntimeError("No joystick devices found")

        selected_index = self._find_device(device_index, name_filter)
        self.joystick = pygame.joystick.Joystick(selected_index)
        self.joystick.init()

        axis_count = self.joystick.get_numaxes()
        axes = (
            steering_axis,
            throttle_axis,
            brake_axis,
            clutch_axis,
        )
        for axis in axes:
            if axis < 0 or axis >= axis_count:
                raise RuntimeError(
                    f"Joystick axis {axis} is unavailable; device has {axis_count} axes"
                )

        self.device_index = selected_index
        self.steering_axis = steering_axis
        self.throttle_axis = throttle_axis
        self.brake_axis = brake_axis
        self.clutch_axis = clutch_axis
        self.wheel_range_degrees = wheel_range_degrees
        self.steering_deadzone = steering_deadzone
        self.pedal_range = pedal_range
        self.invert_pedals = invert_pedals
        self._closed = False

    def _find_device(self, device_index: int, name_filter: str) -> int:
        count = pygame.joystick.get_count()

        if name_filter:
            matches: list[int] = []
            needle = name_filter.casefold()
            for index in range(count):
                name = pygame.joystick.Joystick(index).get_name()
                if needle in name.casefold():
                    matches.append(index)

            if not matches:
                available = [
                    pygame.joystick.Joystick(index).get_name() for index in range(count)
                ]
                raise RuntimeError(
                    f"No joystick matched {name_filter!r}; available devices: {available}"
                )
            if device_index >= len(matches):
                raise RuntimeError(
                    f"Matched joystick index {device_index} is unavailable "
                    f"(found {len(matches)} matching devices)"
                )
            return matches[device_index]

        if device_index < 0 or device_index >= count:
            raise RuntimeError(
                f"Joystick index {device_index} is unavailable (found {count} devices)"
            )
        return device_index

    @staticmethod
    def _clamp(value: float) -> float:
        return max(-1.0, min(1.0, value))

    def _scale_pedal(self, value: float) -> float:
        low, high = self.pedal_range
        if low >= high:
            raise ValueError("pedal_range low value must be less than high value")
        scaled = (value - low) / (high - low)
        scaled = max(0.0, min(1.0, scaled))
        # print(f"Scaling pedal value: {value:.2f} from range {self.pedal_range} to {scaled:.2f}")
        return 1.0 - scaled if self.invert_pedals else scaled

    def read(self) -> WheelState:
        if self._closed:
            raise RuntimeError("Wheel device has been closed")

        pygame.event.pump()

        axis_count = self.joystick.get_numaxes()
        raw_axes = tuple(
            float(self.joystick.get_axis(index)) for index in range(axis_count)
        )

        angle = self._clamp(raw_axes[self.steering_axis])
        if abs(angle) < self.steering_deadzone:
            angle = 0.0
        else:
            sign = 1.0 if angle >= 0.0 else -1.0
            magnitude = (abs(angle) - self.steering_deadzone) / (
                1.0 - self.steering_deadzone
            )
            angle = sign * min(1.0, magnitude)

        return WheelState(
            angle=angle,
            angle_degrees=angle * self.wheel_range_degrees / 2.0,
            throttle=self._scale_pedal(raw_axes[self.throttle_axis]),
            brake=self._scale_pedal(raw_axes[self.brake_axis]),
            clutch=self._scale_pedal(raw_axes[self.clutch_axis]),
            raw_axes=raw_axes,
        )

    @property
    def name(self) -> str:
        return self.joystick.get_name()

    def close(self) -> None:
        if not self._closed:
            self.joystick.quit()
            pygame.joystick.quit()
            pygame.quit()
            self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
