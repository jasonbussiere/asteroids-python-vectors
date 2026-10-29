import math
import random

import pygame

import core.constants
from game_objects.game_objects import GameObject
from systems.vectors import Vector2D
class Asteroid(GameObject):
    def __init__(self, x, y,ast_color=core.constants.AST_COLOR, ast_size=core.constants.AST_LG_RADIUS):
        super().__init__(x, y, color=ast_color, radius=ast_size)
        angle=random.uniform(0,360)
        speed=random.uniform(60.0, 180.0)
        radians=math.radians(angle)
        self.velocity=Vector2D(math.cos(radians) * speed, math.sin(radians) * speed)

    @staticmethod
    def create_random_at(position:Vector2D)-> 'Asteroid':
        return Asteroid(position.x, position.y, ast_color=core.constants.AST_COLOR, ast_size=core.constants.AST_LG_RADIUS)

    def draw(self, view):
        pygame.draw.circle(
            view,
            self.color,
            (int(self.position.x), int(self.position.y)),
            max(1,int(self.radius)),
            2
        )

    def split(self):

        if self.radius < core.constants.MIN_AST_RADIUS:
            return []

        new_radius = self.radius / 2

        print("split triggered!")
        return [
            Asteroid(self.position.x, self.position.y, self.color, new_radius),
            Asteroid(self.position.x, self.position.y, self.color, new_radius)
        ]

    def on_impact_with(self, other: GameObject):
        other.hit_by_asteroid(self)

    def hit_by_laser(self, laser):
        self.destroy()
        self.fragments = self.split()
        self.scored=True
        self.point_value=int(6000/max(1, self.radius))

    


    
