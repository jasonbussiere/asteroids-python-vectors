import math

class Vector2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def multiply(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2)

    def distance_to(self, vector):
        return math.sqrt((vector.x - self.x)**2 + (vector.y - self.y)**2)