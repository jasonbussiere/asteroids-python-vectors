import math

class Vector2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar):
        return Vector2D(self.x*scalar, self.y*scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2)

    def distance_to(self, other):
        difference_vector=self-other
        return difference_vector.magnitude()
    
    def distance_to_squared(self, other):
        difference_vector=self-other
        return difference_vector.x**2 + difference_vector.y**2

    