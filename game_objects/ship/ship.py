
import random
from typing import Optional

import pygame

from core.constants import FRICTION, SHIP_COLOR, SHIP_RADIUS, TURN_AMOUNT
from game_objects.game_objects import GameObject
from game_objects.laser import Laser
from game_objects.ship.ship_strategies import ControlStrategy, KeyboardControlStrategy, SingleLaserStrategy, StandardThrusterStrategy, ThrustStrategy, WeaponStrategy
from systems.vectors import Vector2D




class Ship(GameObject):
    def __init__(
            self,
            x:float,
            y:float,
            controls:Optional[ControlStrategy]=None,
            thrusters:Optional[ThrustStrategy]=None,
            weapon:Optional[WeaponStrategy]=None,
            color=SHIP_COLOR,
            radius=SHIP_RADIUS,
            friction=FRICTION,
            turn_amount=TURN_AMOUNT
            ):
        super().__init__(
            x,
            y,
            color=color,
            radius=radius,
            )
        self.angle=0.0
        self.friction=friction
        self.turn_amount=turn_amount

        #instantiate ship sub components
        self.controls=controls or KeyboardControlStrategy()
        self.thrusters=thrusters or StandardThrusterStrategy()
        self.weapon=weapon or SingleLaserStrategy()
    
    @property
    def heading(self)-> Vector2D:
        return Vector2D(0, -1).rotate(self.angle)

    def update(self, delta_time):
        self.velocity *= FRICTION ** delta_time
        super().update(delta_time)
        if self.weapon:
            self.weapon.update(delta_time)
            
        super().update(delta_time)

    def draw(self, view):
        self.thrusters.draw_flames(view, self)
        pygame.draw.polygon(
            view,
            self.color,
            self.get_vertices()
        )

    def get_vertices(self)->list[tuple[float,float]]:
        """Returns the 4 vertices for classic indented spaceship"""
        nose = Vector2D(0, -self.radius).rotate(self.angle)
        left_fin = Vector2D(-self.radius * 0.7, self.radius * 0.8).rotate(self.angle)
        indent = Vector2D(0, self.radius * 0.4).rotate(self.angle)
        right_fin = Vector2D(self.radius * 0.7, self.radius * 0.8).rotate(self.angle)

        nose_pos=self.position + nose
        left_pos=self.position + left_fin
        indent_pos=self.position + indent
        right_pos=self.position + right_fin
        return [
            (nose_pos.x, nose_pos.y),
            (right_pos.x, right_pos.y),
            (indent_pos.x, indent_pos.y),
            (left_pos.x, left_pos.y),
        ]

    def handle_input(self, keys, delta_time: float)->list[Laser]:
        intent=self.controls.get_intent()
        self.angle += intent.turn * self.turn_amount
        self.thrusters.is_active=intent.thrust
        if intent.thrust:
            self.thrusters.apply_thrust(self, delta_time)

        projectiles=[]
        if intent.fire:
            projectiles.extend(self.weapon.fire(self))

        return projectiles

    #Colision double disacth behavior
    def on_impact_with(self, other):
        other.hit_by_ship(self)

    def hit_by_asteroid(self, asteroid):
        self.destroy()