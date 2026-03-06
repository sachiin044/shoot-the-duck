import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class SnowParticle:
    def __init__(self):
        self.reset()
        # Initial random spread
        self.x = random.uniform(-100, SCREEN_WIDTH + 100)
        self.y = random.uniform(-100, SCREEN_HEIGHT)

    def reset(self):
        # Reset to top with some randomness to simulate wind
        self.x = random.uniform(-100, SCREEN_WIDTH + 100)
        self.y = random.uniform(-50, -20)
            
        self.size = random.randint(2, 4)
        # Varying shades of white/off-white for depth
        grey_val = random.randint(230, 255)
        self.color = (grey_val, grey_val, 255, random.randint(150, 220))
        
        # Snow falls very slowly
        self.speed_y = random.uniform(30, 60)
        self.speed_x = random.uniform(10, 40) # Slight diagonal drift
        
        self.phase = random.uniform(0, math.pi * 2)
        self.freq = random.uniform(0.5, 1.2)
        self.flutter_amp = random.uniform(5, 15)

    def update(self, dt):
        self.y += self.speed_y * dt
        # Gentle swaying as it falls
        self.phase += self.freq * dt
        sway = math.sin(self.phase) * self.flutter_amp
        self.x += (self.speed_x + sway) * dt

        if self.y > SCREEN_HEIGHT or self.x > SCREEN_WIDTH + 100:
            self.reset()

    def draw(self, screen):
        # Draw a small soft circle for the snowflake
        snow_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(snow_surf, self.color, (self.size, self.size), self.size)
        screen.blit(snow_surf, (int(self.x), int(self.y)))

class SnowManager:
    def __init__(self, count=100):
        self.snowflakes = [SnowParticle() for _ in range(count)]

    def update(self, dt):
        for snow in self.snowflakes:
            snow.update(dt)

    def draw(self, screen):
        for snow in self.snowflakes:
            snow.draw(screen)
