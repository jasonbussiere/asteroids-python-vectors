
import pygame

from core.constants import LASER_COLOR, LASER_LIFETIME, LASER_RADIUS
from game_objects.game_objects import GameObject
from systems.vectors import Vector2D

class Laser(GameObject):
    def __init__(
            self,
            x=0.0,
            y=0.0,
            laser_color=LASER_COLOR,
            laser_size=LASER_RADIUS,
            laser_lifetime=LASER_LIFETIME
        ):

        #Intitialize baseline
        super().__init__(x=0.0, y=0.0, color=laser_color, radius=laser_size)
        self.position=Vector2D(x, y)
        self.velocity=Vector2D(0.0, 0.0)
        self.base_lifetime=laser_lifetime
        self.lifetime = laser_lifetime
        self.is_destroyed=False
        self.is_active=False

    def fire(self, position:Vector2D, heading: Vector2D, speed:float=500.0,ship_velocity:Vector2D|None=None):
        self.is_destroyed=False
        self.is_active = True
        self.lifetime=self.base_lifetime

        self.position.x=position.x
        self.position.y=position.y

        self.velocity = heading * speed
        if ship_velocity is not None:
            self.velocity += ship_velocity

    def draw(self, view):
        # draw line segment behind position based on velocity direction
        if self.velocity.magnitude() > 0.0:
            dir_vec=self.velocity.normalize()
            tail_pos=self.position - (dir_vec * 12) #12px last length
            pygame.draw.line(
                view,
                self.color,
                (int(self.position.x), int(self.position.y)),
                (int(tail_pos.x), int(tail_pos.y)),
                2
            )

    def wrap_around(self, width, height):
        if self.is_active:
            super().wrap_around(width, height)

    def update(self, delta_time):
        if not self.is_active or self.is_destroyed:
            return
        
        super().update(delta_time)

        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.destroy()

    def reset(self):
        super().reset()
        self.is_destroyed=False
        self.is_active=False
        self.lifetime=self.base_lifetime
        self.velocity=Vector2D(0.0, 0.0)

    def on_impact_with(self, other: GameObject, pool=None) -> None:
        other.hit_by_laser(self, pool=pool)
        self.destroy()

