import math

import pygame



from core.constants import FRICTION, LASER_COOLDOWN_DELAY, LASER_SPEED, SHIP_COLOR, SHIP_RADIUS, SHIP_SIZE, THRUST_POWER, TURN_AMOUNT
from game_objects.game_objects import GameObject
from game_objects.laser import Laser
from systems.vectors import Vector2D

class Ship(GameObject):
    def __init__(
            self,
            x,
            y,
            ship_color=SHIP_COLOR,
            ship_radius=SHIP_RADIUS,
            rotation=0,
            friction=FRICTION,
            thrust_power=THRUST_POWER,
            laser_speed=LASER_SPEED,
            laser_cooldown_delay=LASER_COOLDOWN_DELAY
    ):

        super().__init__(x, y, color=ship_color, radius=ship_radius )

        self.rotation=rotation
        self.friction=friction
        self.thrust_power=thrust_power

        self.laser_speed=laser_speed
        self.laser_cooldown_delay=laser_cooldown_delay

        self.laser_cooldown=0

    def thrust(self):
        radians=math.radians(self.rotation)

        accel_x=math.sin(radians) * self.thrust_power
        accel_y=-math.cos(radians) * self.thrust_power

        acceleration_vector = Vector2D(accel_x, accel_y)

        self.velocity.add(acceleration_vector)

    def turn_left(self, amount):
        self.rotation -= amount

    def turn_right(self, amount=TURN_AMOUNT):
        self.rotation += amount

    def shoot(self):

        radians=math.radians(self.rotation)
        
        dir_x = math.cos(radians)
        dir_y = math.sin(radians)
        
        laser_velocity=Vector2D(dir_x, dir_y)

        laser_velocity.multiply(self.laser_speed)

        return Laser(self.position.x, self.position.y, laser_velocity)

    def update(self):
        self.velocity.multiply(self.friction)
        super().update()
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        print("DEBUG: ",self.velocity.x, self.velocity.y)

    def draw(self, view):
        pygame.draw.circle(
            view,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.size
        )

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.turn_left(TURN_AMOUNT)

        if keys[pygame.K_RIGHT]:
            self.turn_right(TURN_AMOUNT)

        if keys[pygame.K_UP]:
            self.thrust()

        if keys[pygame.K_SPACE] and self.laser_cooldown == 0:
            self.laser_cooldown=self.laser_cooldown_delay
            return self.shoot()