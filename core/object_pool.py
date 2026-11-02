from typing import Type, TypeVar

T = TypeVar("T")

class ObjectPool:
    def __init__(self):
        # Maps class types (ex. Laser, Asteroid) to lists of inactive instances
        self._vault: dict[type, list]={}

    def get(self, cls: Type[T])->T:
        """Retreives an instance of 'cls'. Auto-creates one if the pool is empty"""
        pool=self._vault.setdefault(cls, [])
        if pool:
            return pool.pop()

        # Auto-instantiate using the class constructor
        return cls()

    def release(self, obj: object):
        """Auto-detects objects type using type(obj) and recycles it."""
        reset = getattr(obj, "reset", None)
        if callable(reset):
            reset()

    def warm(self, cls: Type[T], count: int):
        """pre-allocates instances for a specific class."""
        pool=self._vault.setdefault(cls, [])
        for _ in range(count):
            pool.append(cls())
            


        