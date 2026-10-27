from __future__ import annotations
from abc import abstractmethod
from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from systems.vectors import Vector2D


class GameObject:
    def __init__(self, x, y, color, radius):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.color = color
        self.radius = radius
        self.is_destroyed=False

        self.fragments=[]
        self.scored=False
        self.point_value=0

    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.wrap_around(VIEW_WIDTH, VIEW_HEIGHT)

    def draw(self, view):
        raise NotImplementedError("subclasses of GameObjects must implement draw()")

    def wrap_around(self, width, height):
        self.position.x %= width
        self.position.y %= height

    def has_collided_with(self,other:GameObject)-> None:
        distance_sqared=self.position.distance_to_squared(other.position)
        radii_sum_squared=(self.radius + other.radius)**2
        return distance_sqared < radii_sum_squared

    def destroy(self):
        self.is_destroyed=True

    # double dispatch entry point
    @abstractmethod
    def on_impact_with(self, other:GameObject) -> None:
        pass

    # default handlers , subclasses override as needed
    @abstractmethod
    def hit_by_laser(self, laser:GameObject)-> None:
        pass

    @abstractmethod
    def hit_by_asteroid(self, asteroid:GameObject)-> None:
        pass

    @abstractmethod
    def hit_by_ship(self, ship:GameObject)-> None:
        pass

    