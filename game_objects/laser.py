import math

import pygame

from game_objects.game_objects import GameObject
from systems.vectors import Vector2D



class Laser(GameObject):
    def __init__(self, x, y, ship_angle):
        super().__init__(x, y)

        radians=math.radians(ship_angle)

        dir_x = math.cos(radians)
        dir_y = math.sin(radians)

        self.velocity=Vector2D(dir_x, dir_y)

        self.velocity.multiply(15)

    def draw(self, view):
        pygame.draw.circle(
            view,
            (255, 255, 0),
            (int(self.position.x), int(self.position.y)),
            3
        )

    def is_out_of_bounds(self, width, height):
        return (
            self.position.x < 0
            or self.position.x > width
            or self.position.y < 0
            or self.position.y > height
        )
