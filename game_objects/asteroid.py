import math
import random

import pygame

from core.constants import AST_COLOR, AST_LG_SIZE, SIZE_MULTIPLIER
from game_objects.game_objects import GameObject
from systems.vectors import Vector2D


class Asteroid(GameObject):
    def __init__(self, x, y,ast_color=AST_COLOR, ast_size=AST_LG_SIZE):
        super().__init__(x, y, color=ast_color, size=ast_size)
        self.radius=self.size*SIZE_MULTIPLIER
        angle=random.uniform(0,360)
        speed=random.uniform(1.0, 3.0)
        radians=math.radians(angle)
        self.velocity=Vector2D(math.cos(radians) * speed, math.sin(radians) * speed)

    def draw(self, view):
        pygame.draw.circle(
            view,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

    
