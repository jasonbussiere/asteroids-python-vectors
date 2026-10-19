class Ship(GameObject):
    def __init(self, x, y):
        super().__initi__(x, y)
        self.angle=0
        self.thrust_power=0.1
        self.color=(0, 255, 0)