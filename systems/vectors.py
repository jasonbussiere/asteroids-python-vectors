import math

class Vector2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def substract(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def multiply(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2)

    def distance_to(self, vector):
        diff_x = self.x - vector.x
        diff_y = self.y - vector.y
        return Vector2D(diff_x, diff_y).magnitude()