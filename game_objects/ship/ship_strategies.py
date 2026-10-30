from abc import ABC, abstractmethod
import random

import pygame

from game_objects.laser import Laser
from systems.vectors import Vector2D

#*****************************************************#
#** Controls Strategy
#*****************************************************#

#data container representing desired action for the current frame
class ShipIntent:
    def __init__(
            self,
            turn:float=0.0,
            thrust:bool=False,
            fire:bool=False
        )->None:
        self.turn=turn
        self.thrust=thrust
        self.fire=fire

#interface
class ControlStrategy(ABC):
    @abstractmethod
    def get_intent(self)->ShipIntent:
        raise NotImplementedError

#concrete strategy for human player keyboard controls
class KeyboardControlStrategy(ControlStrategy):
    def __init__(self)->None:
        self.previous_fire_state:bool=False

    def get_intent(self)->ShipIntent:
        keys=pygame.key.get_pressed()
        turn_val:float=0.0
        if keys[pygame.K_LEFT]:
            turn_val -= 1.0
        if keys[pygame.K_RIGHT]:
            turn_val += 1.0

        is_thrusting=bool(keys[pygame.K_UP])
        current_fire_state=bool(keys[pygame.K_SPACE])
        is_firing=current_fire_state and not self.previous_fire_state
        self.previous_fire_state=current_fire_state
        
        return ShipIntent(
            turn_val,
            is_thrusting,
            is_firing
        )

#*****************************************************#
#** Thruster Strategy
#*****************************************************#

class ThrustStrategy(ABC):
    def __init__(self) -> None:
        self.is_active:bool=False

    @abstractmethod
    def apply_thrust(self, ship, delta_time:float)->None:
        raise NotImplementedError

    @abstractmethod
    def draw_flames(self, view, ship)->None:
        raise NotImplementedError

class StandardThrusterStrategy(ThrustStrategy):
    def __init__(self, thrust_power:float=400.0):
        super().__init__()
        self.thrust_power=thrust_power

    def apply_thrust(self, ship, delta_time:float):
        acceleration = ship.heading * self.thrust_power
        ship.velocity += acceleration * delta_time

    def _get_flame_vertices(self, ship, anchor_scale:float, min_len:float, max_len:float):
        width = ship.radius * anchor_scale
        base_offset=ship.radius * 0.6

        left_anchor=Vector2D(-width, base_offset).rotate(ship.angle)
        right_anchor=Vector2D(width, base_offset).rotate(ship.angle)

        flame_len=ship.radius * random.uniform(min_len, max_len)
        flame_tip=Vector2D(0, flame_len).rotate(ship.angle)

        left_pos=ship.position + left_anchor
        right_pos=ship.position + right_anchor
        flame_tip_pos = ship.position + flame_tip

        return [
            (left_pos.x, left_pos.y),
            (flame_tip_pos.x, flame_tip_pos.y),
            (right_pos.x, right_pos.y)
        ]

    def draw_flames(self, view, ship) -> None:
        if not self.is_active:
            return

        bright_orange=(255,140,0)
        bright_yellow=(255, 240, 0)
        outer_flame=self._get_flame_vertices(ship, anchor_scale=0.6, min_len=1.3, max_len=1.7)
        inner_flame=self._get_flame_vertices(ship, anchor_scale=0.4, min_len=0.8, max_len=1.1)

        pygame.draw.polygon(view, bright_orange, outer_flame, 2)
        pygame.draw.polygon(view, bright_yellow, inner_flame)

#*****************************************************#
#** Weapon Strategy
#*****************************************************#

class WeaponStrategy(ABC):
    def __init__(self, cooldown_delay: float=0.25)->None:
        self.cooldown_delay=cooldown_delay
        self.cooldown_timer=0.0

    def update(self, delta_time:float)->None:
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

    @abstractmethod
    def fire(self, ship)->list[Laser]:
        raise NotImplementedError

class SingleLaserStrategy(WeaponStrategy):
    def __init__(self, laser_speed:float=600, cooldown_delay:float=0.15):
        super().__init__(cooldown_delay)
        self.laser_speed=laser_speed

    def fire(self, ship)->list[Laser]:
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.cooldown_delay
            muzzle_pos=ship.position + (ship.heading * ship.radius)
            laser_velocity=ship.velocity + (ship.heading * self.laser_speed)
            return [Laser(muzzle_pos.x, muzzle_pos.y, laser_velocity)]
        return []

