import math
import random

import pygame

from game_objects.game_objects import GameObject
from systems.vectors import Vector2D


class Asteroid(GameObject):
    def __init__(self, x, y, size=3):
        super().__init__(x, y)
        self.size=size
        self.radius=self.size*15
        angle=random.uniform(0,360)
        speed=random.uniform(1.0, 3.0)
        radians=math.radians(angle)
        self.velocity=Vector2D(math.cos(radians) * speed, math.sin(radians) * speed)

    def draw(self, view):
        pygame.draw.circle(
            view,
            (255, 0, 0),
            (int(self.position.x), int(self.position)),
            self.radius
        )

    
