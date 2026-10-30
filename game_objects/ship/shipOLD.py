import math
import random

import pygame

from core.constants import FRICTION, LASER_COOLDOWN_DELAY, LASER_SPEED, SHIP_COLOR, SHIP_RADIUS, THRUST_POWER, TURN_AMOUNT
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
            angle=0,
            friction=FRICTION,
            thrust_power=THRUST_POWER,
            laser_speed=LASER_SPEED,
            laser_cooldown_delay=LASER_COOLDOWN_DELAY
    ):

        super().__init__(x, y, color=ship_color, radius=ship_radius )

        self.angle=angle
        self.friction=friction
        self.thrust_power=thrust_power

        self.laser_speed=laser_speed
        self.laser_cooldown_delay=laser_cooldown_delay

        self.laser_cooldown=0
        self.is_accelerating=False

    def get_thruster_vertices(self):
        left_anchor=Vector2D(-self.radius * 0.4, self.radius * 0.8).rotate(self.angle)
        right_anchor=Vector2D(self.radius * 0.4, self.radius * 0.8).rotate(self.angle)

        flame_length=self.radius * random.uniform(1.3, 1.7)
        flame_tip=Vector2D(0, flame_length).rotate(self.angle)

        left_anchor_pos=self.position + left_anchor
        right_anchor_pos=self.position + right_anchor
        flame_tip_pos = self.position + flame_tip

        return [
            (left_anchor_pos.x, left_anchor_pos.y),
            (flame_tip_pos.x, flame_tip_pos.y),
            (right_anchor_pos.x, right_anchor_pos.y)
        ]

    def get_inner_thruster_vertices(self):
            left_anchor=Vector2D(-self.radius * 0.2, self.radius * 0.8).rotate(self.angle)
            right_anchor=Vector2D(self.radius * 0.2, self.radius * 0.8).rotate(self.angle)
    
            flame_length=self.radius * random.uniform(0.8, 1.1)
            flame_tip=Vector2D(0, flame_length).rotate(self.angle)
    
            left_anchor_pos=self.position + left_anchor
            right_anchor_pos=self.position + right_anchor
            flame_tip_pos = self.position + flame_tip
    
            return [
                (left_anchor_pos.x, left_anchor_pos.y),
                (flame_tip_pos.x, flame_tip_pos.y),
                (right_anchor_pos.x, right_anchor_pos.y)
            ]
    
    def get_vertices(self):
        nose = Vector2D(0, -self.radius).rotate(self.angle)
        left_fin = Vector2D(-self.radius * 0.8, self.radius * 0.8).rotate(self.angle)
        right_fin = Vector2D(self.radius * 0.8, self.radius * 0.8).rotate(self.angle)

        nose_pos=self.position + nose
        left_pos=self.position + left_fin
        right_pos=self.position + right_fin
        return [
            (nose_pos.x, nose_pos.y),
            (left_pos.x, left_pos.y),
            (right_pos.x, right_pos.y)
        ]

    def thrust(self, delta_time):
        radians=math.radians(self.angle)

        accel_x=math.sin(radians) * self.thrust_power
        accel_y=-math.cos(radians) * self.thrust_power

        acceleration_vector = Vector2D(accel_x, accel_y)

        self.velocity += acceleration_vector * delta_time

    def turn_left(self, amount=TURN_AMOUNT):
        self.angle -= amount

    def turn_right(self, amount=TURN_AMOUNT):
        self.angle += amount

    def shoot(self):

        print("pew pew!")
        
        radians=math.radians(self.angle)
        
        dir_x = math.sin(radians)
        dir_y = -math.cos(radians)
        
        laser_velocity=Vector2D(dir_x, dir_y)

        laser_velocity *= self.laser_speed

        return Laser(self.position.x, self.position.y, laser_velocity)

    def update(self, delta_time):
        self.velocity *= self.friction ** delta_time
        super().update(delta_time)
        if self.laser_cooldown > 0:
            self.laser_cooldown -= delta_time

    def draw(self, view):
        print(self.is_accelerating)
        if self.is_accelerating:
            flame_color=(255, 140, 0)
            pygame.draw.polygon(
                view,
                flame_color,
                self.get_thruster_vertices(),
                2
            )

            inner_flame_color=(255, 240, 0)
            pygame.draw.polygon(
                view,
                inner_flame_color,
                self.get_inner_thruster_vertices(),
                
            )
            
        pygame.draw.polygon(
            view,
            self.color,
            self.get_vertices()
        )

    def handle_input(self, keys, delta_time):
        self.is_accelerating=False

        if keys[pygame.K_LEFT]:
            self.turn_left(TURN_AMOUNT)

        if keys[pygame.K_RIGHT]:
            self.turn_right(TURN_AMOUNT)

        if keys[pygame.K_UP]:
            self.is_accelerating=True
            self.thrust(delta_time)

        new_laser=[]
        if keys[pygame.K_SPACE] and self.laser_cooldown <= 0:
            self.laser_cooldown=self.laser_cooldown_delay
            new_laser=self.shoot()
            return new_laser

    def on_impact_with(self, other):
        other.hit_by_ship(self)

    def hit_by_asteroid(self, asteroid):
        self.destroy()