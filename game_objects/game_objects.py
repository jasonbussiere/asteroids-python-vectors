import math

from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from systems.vectors import Vector2D


class GameObject:
    def __init__(self, x, y, color, radius):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.color = color
        self.radius = radius

    def update(self):
        self.position.add(self.velocity)
        self.wrap_around(VIEW_WIDTH, VIEW_HEIGHT)

    def draw(self, view):
        pass

    def wrap_around(self, width, height):
        self.position.x %= width
        self.position.y %= height

    def collides_with(self,other):
        distance = math.sqrt((self.position.x - other.postion.x)**2 + (self.position.y - other.positon.y)**2)
