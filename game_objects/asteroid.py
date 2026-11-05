import math
import random

import pygame

from core.constants import AST_COLOR, AST_LG_RADIUS, MIN_AST_RADIUS
from game_objects.game_objects import GameObject
from systems.vectors import Vector2D

class Asteroid(GameObject):
    def __init__(self, x:float=0.0, y:float=0.0,ast_color=AST_COLOR, ast_size=AST_LG_RADIUS):
        super().__init__(x, y, color=ast_color, radius=ast_size)
        self.reconfigure(Vector2D(x,y), ast_color, ast_size)

    def reconfigure(self, position:Vector2D, ast_color=AST_COLOR, ast_size=AST_LG_RADIUS):
        """Intitializes or resets asteroids parameters for ObjectPool recycling"""
        self.position=Vector2D(position.x, position.y)
        self.color=ast_color
        self.radius=ast_size
        self.is_destroyed=False
        self.scored=False
        self.fragments=None

        self.angle=random.uniform(0, 360)
        self.speed=random.uniform(40, 120)
        self.radians=math.radians(self.angle)
        self.velocity=Vector2D(math.cos(self.radians) * self.speed, math.sin(self.radians) * self.speed)
        self.local_vertices=self._generate_asteroid_shape()
        self.point_value=int(6000 / max(1, self.radius))

    def _generate_asteroid_shape(self)->list[Vector2D]:
        """Creates a randomized, jagged polygon contour."""
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

    def setup_at(self, pos: Vector2D, radius: int = AST_LG_RADIUS):
        """Configure position and regenerate shape for pooled instances."""
        self.reconfigure(pos, ast_color=AST_COLOR, ast_size=radius)

    def reset(self):
        """Clears active/destruction flags before returning to vault"""
        self.is_destroyed=False
        self.scored=False
        self.fragments=None
    
    def draw(self, view):
        pygame.draw.polygon(
            view,
            self.color,
            self.get_vertices(),
            2
        )

    def split(self, pool=None):
        if self.radius < MIN_AST_RADIUS:
            return []

        new_radius = int(self.radius / 2)
        fragments=[]

        for _ in range(2):
            if pool is not None:
                # Fetch recycled object from pool
                fragment=pool.get(Asteroid)
                # Reset position, radius, velocity and vertices
                fragment.setup_at(self.position, radius=new_radius)
            else:
                # Fallback instantiation if no pool was passed
                fragment=Asteroid(self.position.x, self.position.y, ast_size=new_radius)
        
            fragments.append(fragment)
        return fragments

    def get_vertices(self)-> list[tuple[float, float]]:
        world_points=[]
        for p in self.local_vertices:
            rotated=p.rotate(self.angle)
            world_points.append((self.position.x + rotated.x, self.position.y + rotated.y))

        return world_points
    
    def on_impact_with(self, other: GameObject, pool=None):
        other.hit_by_asteroid(self, pool=pool)

    def hit_by_laser(self, laser, pool=None):
        self.destroy()
        self.scored=True
        self.fragments = self.split(pool=pool)

    # TODO asteroid factory / Object pool (asteroid/laser)

    


    
