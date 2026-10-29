import math

class Vector2D:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __add__(self, other)->'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other)->'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar)->'Vector2D':
            return Vector2D(self.x*scalar, self.y*scalar)

    def __rmul__(self, other):
        pass

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0,0)
        return Vector2D(self.x/mag, self.y/mag)
    
    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2)

    def distance_to(self, other):
        difference_vector=self-other
        return difference_vector.magnitude()
    
    def distance_to_squared(self, other):
        difference_vector=self-other
        return difference_vector.x**2 + difference_vector.y**2

    def rotate(self, angle)->'Vector2D':
        radians=math.radians(angle)
        cos_a=math.cos(radians)
        sin_a=math.sin(radians)
        x=self.x * cos_a - self.y * sin_a
        y=self.x * sin_a + self.y * cos_a
        return Vector2D(x, y)
