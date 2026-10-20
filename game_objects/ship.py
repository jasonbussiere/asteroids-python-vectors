import math

import pygame



from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from game_objects.game_objects import GameObject
from game_objects.laser import Laser
from systems.vectors import Vector2D

class Ship(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rotation=0
        self.thrust_power=0.1
        self.color=(0, 255, 0)

    def thrust(self):
        radians=math.radians(self.rotation)

        accel_x=math.cos(radians) * self.thrust_power
        accel_y=math.sin(radians) * self.thrust_power

        acceleration_vector = Vector2D(accel_x, accel_y)

        self.velocity.add(acceleration_vector)

    def turn_left(self, amount):
        self.rotation -= amount

    def turn_right(self, amount):
        self.rotation += amount

    def shoot(self):
        return Laser(self.position.x, self.position.y, self.rotation)

    def update(self):
        self.velocity.multiply(0.99)
        super().update()
        self.wrap_around(VIEW_WIDTH, VIEW_HEIGHT)
        print("DEBUG: ",self.velocity.x, self.velocity.y)

    def draw(self, view):
        pygame.draw.circle(
            view,
            (0,255,0),
            (int(self.position.x), int(self.position.y)),
            15
        )

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.turn_left(5)

        if keys[pygame.K_RIGHT]:
            self.turn_right(5)

        if keys[pygame.K_UP]:
            self.thrust()

        if keys[pygame.K_SPACE]:
            self.shoot()