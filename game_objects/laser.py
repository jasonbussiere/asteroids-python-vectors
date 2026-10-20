import math

import pygame

from core.constants import LASER_COLOR, LASER_LIFETIME, LASER_SIZE, LASER_SPEED, VIEW_HEIGHT, VIEW_WIDTH
from game_objects.game_objects import GameObject



class Laser(GameObject):
    def __init__(
            self,
            x,
            y,
            velocity,
            laser_color=LASER_COLOR,
            laser_size=LASER_SIZE,
            laser_lifetime=LASER_LIFETIME
        ):
        
        super().__init__(x, y, color=laser_color, size=laser_size)
        self.velocity = velocity
        self.lifetime = laser_lifetime
        self.laser_color = laser_color
        self.laser_size = laser_size

    def draw(self, view):
        pygame.draw.circle(
            view,
            self.laser_color,
            (int(self.position.x), int(self.position.y)),
            self.laser_size
        )

    def is_out_of_bounds(self):
        return (
            self.position.x < 0
            or self.position.x > VIEW_WIDTH
            or self.position.y < 0
            or self.position.y > VIEW_HEIGHT
        )

    def is_alive(self):
        return self.lifetime > 0

    def update(self):
        super().update()
        self.lifetime -= 1

