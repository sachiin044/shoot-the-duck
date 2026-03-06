import random
from entities.duck import Duck
from config import *

class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_rate = SPAWN_RATE_START
        self.active_ducks = []

    def update(self, dt, speed_mult, max_ducks, surfaces_dict, rate_mult=1.0):
        self.spawn_timer += dt
        
        # 1. Faster Population Recovery
        # If density is very low (e.g. at round start or after a miss), 
        # spawn immediately until we have at least 3 birds
        instant_populate = len(self.active_ducks) < min(3, max_ducks)
        
        # 2. Timing logic
        adjusted_rate = self.spawn_rate / rate_mult
        
        if len(self.active_ducks) < max_ducks:
            if self.spawn_timer >= adjusted_rate or instant_populate:
                # Spawn in larger bursts for high density rounds
                burst_size = 5 if max_ducks >= 5 else 1
                to_spawn = min(burst_size, max_ducks - len(self.active_ducks))
                
                for _ in range(to_spawn):
                    self.spawn_duck(speed_mult, surfaces_dict)
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

    def spawn_duck(self, speed_mult, surfaces_dict):
        side = random.choice(["left", "right"])
        if side == "left":
            x = -DUCK_WIDTH
        else:
            x = SCREEN_WIDTH
            
        y = random.uniform(100, SCREEN_HEIGHT - 300)
        
        # Randomize duck type
        weights = [0.6, 0.2, 0.15, 0.05] # normal, fast, zigzag, golden
        duck_type = random.choices(list(DUCK_TYPES.keys()), weights=weights)[0]
        
        # Pick random color from palette
        color_name = random.choice(list(surfaces_dict.keys()))
        surfaces = surfaces_dict[color_name]
        
        new_duck = Duck(x, y, speed_mult, duck_type, surfaces)
        self.active_ducks.append(new_duck)

    def draw(self, screen):
        for duck in self.active_ducks:
            duck.draw(screen)
