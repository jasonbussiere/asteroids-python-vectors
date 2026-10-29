import random

import pygame

from game_objects.game_objects import GameObject
from systems.vectors import Vector2D


class Particle(GameObject):
    def __init__(self, position: Vector2D, color=(200,200,200)):
        super().__init__(position.x, position.y, color, radius=0)

        angle=random.uniform(0, 360)
        speed=random.uniform(50, 180)
        self.velocity=Vector2D(speed, 0).rotate(angle)
        self.color=color
        self.lifetime=random.uniform(0.3, 0.6)
        self.max_lifetime=self.lifetime

    def update(self, delta_time):
        super().update(delta_time)
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.is_destroyed=True

    def draw(self, view):
        current_radius=max(1, int(5* (self.lifetime/self.max_lifetime)))
        pygame.draw.circle(
            view,
            self.color,
            (int(self.position.x), int(self.position.y)),
            current_radius
        )
        