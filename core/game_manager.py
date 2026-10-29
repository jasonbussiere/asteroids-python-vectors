from __future__ import annotations
import random

from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from core.particle_manager import ParticleManager
from game_objects.asteroid import Asteroid
from game_objects.game_objects import GameObject
from game_objects.laser import Laser
from game_objects.ship import Ship
from systems.vectors import Vector2D




class GameManager:
    def __init__(self, view):
        self.view=view
        self.ship=None
        self.game_objects: list[GameObject]=[]
        self.score=0
        self.is_game_over=False
        self.particle_manager=ParticleManager()

    def init_game_objects(self):
        # Track game state
        self.is_game_over=False
        self.score=0
        
        #instantiate game objects
        self.ship=Ship(self.view.get_width()/2, self.view.get_height()/2)
        self.game_objects=[self.ship]
        self.spawn_asteroids(count=4)
        
        return self.game_objects

    def spawn_asteroids(self, count: int):
        for _ in range(count):
            pos=self.get_random_edge_position()
            self.game_objects.append(Asteroid.create_random_at(pos))

    def get_random_edge_position(self)-> Vector2D:
        width, height=self.view.get_size()
        if random.random() < 0.5:
            x=random.choice([0, width])
            y=random.uniform(0, height)
        else:
            x=random.uniform(0, width)
            y=random.choice([0, height])
        return Vector2D(x, y)
    


    def process_inputs(self, keys, delta_time):
        if self.ship and not self.ship.is_destroyed:
                #pass keys list to ship, ship handles key press behavior
                new_laser = self.ship.handle_input(keys, delta_time)
                if new_laser:
                    self.game_objects.append(new_laser)

    def check_colisions(self):
        for i in range(len(self.game_objects)):
            for j in range(i+1, len(self.game_objects)):
                #only check colisions if both are still alive!
                a: GameObject=self.game_objects[i]
                b: GameObject=self.game_objects[j]
                if not a.is_destroyed and not b.is_destroyed:
                    if a.position.distance_to(b.position) < (a.radius + b.radius):
                        a.on_impact_with(b)
                        b.on_impact_with(a)

    def clean_up_objects(self):
        surviving_objects=[]

        for obj in self.game_objects:
            if obj.is_destroyed:
                particle_count=12 if obj.radius<20 else 25
                self.particle_manager.create_explosion(
                    position=obj.position,
                    count=particle_count,
                    color=(220,220,220)
                )
                if obj.scored:
                    self.score += obj.point_value

                if obj.fragments is not None:
                    surviving_objects.extend(obj.fragments)
            else:
                surviving_objects.append(obj)

        self.game_objects=surviving_objects

        if self.ship and self.ship.is_destroyed:
            self.particle_manager.create_explosion(
                position=self.ship.position,
                count=35,
                color=(255, 60, 0)
            )
            self.ship = None
            self.is_game_over=True

    def draw(self, view):
        for obj in self.game_objects:
            obj.draw(view)

        self.particle_manager.draw(view)

    def update(self, delta_time: float):
        for obj in self.game_objects:
            obj.update(delta_time)

        self.particle_manager.update(delta_time)
