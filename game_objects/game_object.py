from systems.vectors import Vector2D


class GameObject:
    def __init__(self, x, y):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)

    def update(self):
        self.position.add(self.velocity)

    def draw(self):
        pass

    def wrap_around(self, width, height):
        self.position.x %= width
        self.position.y %= height
