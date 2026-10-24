
from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from systems.vectors import Vector2D


class GameObject:
    def __init__(self, x, y, color, radius):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.color = color
        self.radius = radius

    def update(self):
        self.position += self.velocity
        self.wrap_around(VIEW_WIDTH, VIEW_HEIGHT)

    def draw(self, view):
        raise NotImplementedError("subclasses of GameObjects must implement draw()")

    def wrap_around(self, width, height):
        self.position.x %= width
        self.position.y %= height

    def has_collided_with(self,other:'GameObject'):
        distance_sqared=self.position.distance_to_squared(other.position)
        radii_sum_squared=(self.radius + other.radius)**2
        return distance_sqared < radii_sum_squared

    # double dispatch entry point
    def on_impact_with(self, other:'GameObject'):
        pass

    # default handlers , subclasses override as needed
    def hit_by_laser(self, laser):
        pass

    def hit_by_asteroid(self, asteroid):
        pass

    def hit_by_ship(self, ship):
        pass