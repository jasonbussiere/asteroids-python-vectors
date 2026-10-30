import math
import random

import pygame

from core.constants import AST_COLOR, AST_LG_RADIUS, MIN_AST_RADIUS
from game_objects.game_objects import GameObject
from systems.vectors import Vector2D

class Asteroid(GameObject):
    def __init__(self, x, y,ast_color=AST_COLOR, ast_size=AST_LG_RADIUS):
        super().__init__(x, y, color=ast_color, radius=ast_size)
        self.angle:float=random.uniform(0,360)
        self.speed:float=random.uniform(-60.0, 180.0)
        radians=math.radians(self.angle)
        self.velocity=Vector2D(math.cos(radians) * self.speed, math.sin(radians) * self.speed)
        self.local_vertices=self._generate_asteroid_shape()

    @staticmethod
    def create_random_at(position:Vector2D)-> 'Asteroid':
        return Asteroid(position.x, position.y, ast_color=AST_COLOR, ast_size=AST_LG_RADIUS)

    def _generate_asteroid_shape(self)->list[Vector2D]:
        """Creates a randomized, jagged polygon contour"""
        points=[]
        num_points=random.randint(7,12)
        angle_step=360/num_points
        for i in range(num_points):
            angle=i*angle_step
            angle += random.uniform(-angle_step * 0.2, angle_step * 0.2)
            dist=self.radius * random.uniform(0.7, 1.3)
            vertex = Vector2D(0, -dist).rotate(angle)
            points.append(vertex)
        return points
    
    def draw(self, view):
        pygame.draw.polygon(
            view,
            self.color,
            self.get_vertices(),
            2
        )

    def split(self):

        if self.radius < MIN_AST_RADIUS:
            return []

        new_radius = self.radius / 2

        print("split triggered!")
        return [
            Asteroid(self.position.x, self.position.y, self.color, new_radius),
            Asteroid(self.position.x, self.position.y, self.color, new_radius)
        ]

    def get_vertices(self)-> list[tuple[float, float]]:
        world_points=[]
        for p in self.local_vertices:
            rotated=p.rotate(self.angle)
            world_points.append((self.position.x + rotated.x, self.position.y + rotated.y))

        return world_points
    
    def on_impact_with(self, other: GameObject):
        other.hit_by_asteroid(self)

    def hit_by_laser(self, laser):
        self.destroy()
        self.fragments = self.split()
        self.scored=True
        self.point_value=int(6000/max(1, self.radius))

    # TODO asteroid factory / Object pool (asteroid/laser)

    


    
