import random
from entities.duck import Duck
from config import *

class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_rate = SPAWN_RATE_START
        self.active_ducks = []

    def update(self, dt, speed_mult, max_ducks, rate_mult=1.0):
        self.spawn_timer += dt
        
        # Only spawn if below cap
        adjusted_rate = self.spawn_rate / rate_mult
        if len(self.active_ducks) < max_ducks:
            if self.spawn_timer >= adjusted_rate:
                self.spawn_duck(speed_mult)
                self.spawn_timer = 0

        # Update and filter ducks
        missed_count = 0
        for duck in self.active_ducks[:]:
            duck.update(dt)
            if not duck.alive:
                if duck.is_missed():
                    missed_count += 1
                self.active_ducks.remove(duck)
        return missed_count

    def spawn_duck(self, speed_mult):
        side = random.choice(["left", "right"])
        if side == "left":
            x = -DUCK_WIDTH
        else:
            x = SCREEN_WIDTH
            
        y = random.uniform(100, SCREEN_HEIGHT - 300)
        
        # Randomize duck type
        weights = [0.6, 0.2, 0.15, 0.05] # normal, fast, zigzag, golden
        duck_type = random.choices(list(DUCK_TYPES.keys()), weights=weights)[0]
        
        new_duck = Duck(x, y, speed_mult, duck_type)
        self.active_ducks.append(new_duck)

    def draw(self, screen, surface):
        for duck in self.active_ducks:
            duck.draw(screen, surface)
