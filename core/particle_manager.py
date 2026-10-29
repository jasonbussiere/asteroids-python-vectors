from game_objects.particle import Particle
from systems.vectors import Vector2D


class ParticleManager:
    def __init__(self):
        self.particles: list[Particle] = []

    def create_explosion(self, position: Vector2D, count: int=15, color=(200,200,200)):
        for _ in range(count):
            self.particles.append(Particle(position, color=color))

    def update(self, delta_time: float):
        for particle in self.particles:
            particle.update(delta_time)
        self.particles= [p for p in self.particles if not p.is_destroyed]

    def draw(self, view):
        for particle in self.particles:
            particle.draw(view)