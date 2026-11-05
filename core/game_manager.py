from __future__ import annotations
import random

from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from core.object_pool import ObjectPool
from core.particle_manager import ParticleManager
from game_objects.asteroid import Asteroid
from game_objects.game_objects import GameObject
from game_objects.laser import Laser
from game_objects.ship.ship import Ship
from systems.vectors import Vector2D




class GameManager:
    def __init__(self, view):
        # Create the pool instance
        self.pool = ObjectPool()

        # Pre-warm high frequency object pools
        self.pool.warm(Laser, count=50)
        self.pool.warm(Asteroid, count=30)

        self.view=view
        self.ship=None
        self.game_objects: list[GameObject]=[]
        self.particle_manager=ParticleManager()
        self.is_game_over=False
        self.score=0

    def init_game_objects(self):
        self.reset_game()
        # Track game state
        self.is_game_over=False
        self.score=0
        
        #instantiate game objects
        self.ship=Ship(self.view.get_width()/2, self.view.get_height()/2)
        self.game_objects=[self.ship]
        self.spawn_asteroids(count=4)
        
        return self.game_objects

    def spawn_laser(self):
        """Fetch a laser from the pool and add it to the active scene."""
        ship = self.ship
        if ship is None:
            return

        laser=self.pool.get(Laser)
        laser.fire(
            ship.position,
            ship.heading,
            speed=ship.weapon.laser_speed,
            ship_velocity=ship.velocity,
        )
        self.game_objects.append(laser)


    def spawn_asteroids(self, count: int):
        """Fetch asteroids from the pool and add them to the active game objects list."""
        for _ in range(count):
            pos=self.get_random_edge_position()
            asteroid = self.pool.get(Asteroid)
            asteroid.setup_at(pos)
            self.game_objects.append(asteroid)

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
                has_fired = self.ship.handle_input(keys, delta_time)
                if has_fired:
                    self.spawn_laser()

    def check_colisions(self):
        for i in range(len(self.game_objects)):
            for j in range(i+1, len(self.game_objects)):
                #only check colisions if both are still alive!
                a: GameObject=self.game_objects[i]
                b: GameObject=self.game_objects[j]

                if (isinstance(a, Ship) and isinstance(b, Laser)
                    or isinstance(a, Laser) and isinstance(b, Ship)):
                    continue
                
                if not a.is_destroyed and not b.is_destroyed:
                    if a.has_collided_with(b):
                        a.on_impact_with(b, pool=self.pool)
                        b.on_impact_with(a, pool=self.pool)

    def clean_up_objects(self):
        surviving_objects=[]

        for obj in self.game_objects:
            if obj.is_destroyed:
                # spawn exploison particles
                if isinstance(obj, Asteroid):
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
                #recycle destroyed objects back in the pool
                if obj != self.ship:
                    self.pool.release(obj)
            else:
                # keep living objects in the game loop
                surviving_objects.append(obj)

        self.game_objects=surviving_objects

        # handle ship destruction
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

    def reset_game(self):
        """Release active pooled objects and clear transient game state."""
        for obj in self.game_objects:
            if isinstance(obj, (Laser, Asteroid)):
                self.pool.release(obj)
        self.game_objects.clear()
        self.particle_manager.clear()
        self.ship = None
