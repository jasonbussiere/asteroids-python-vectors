
import pygame

from core.constants import LASER_COLOR, LASER_LIFETIME, LASER_RADIUS
from game_objects.game_objects import GameObject

class Laser(GameObject):
    def __init__(
            self,
            x,
            y,
            velocity,
            laser_color=LASER_COLOR,
            laser_size=LASER_RADIUS,
            laser_lifetime=LASER_LIFETIME
        ):
        
        super().__init__(x, y, color=laser_color, radius=laser_size)
        self.velocity = velocity
        self.lifetime = laser_lifetime

    def draw(self, view):
        pygame.draw.circle(
            view,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

    def wrap_around(self, width, height):
        pass

    def update(self, delta_time):
        super().update(delta_time)
        self.lifetime -= 1
        if self.lifetime <= 0:
            super().destroy()

    def on_impact_with(self, other):
        other.hit_by_laser(self)

    def hit_by_asteroid(self, asteroid):
        self.destroy()

