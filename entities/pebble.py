import pygame
import random
import math
from config import *

class Pebble:
    def __init__(self, surface):
        self.surface = surface
        self.size = PEBBLE_SIZE
        self.reset()

    def reset(self):
        # Spawn at random X at the bottom
        self.x = random.randint(50, SCREEN_WIDTH - 50 - self.size)
        self.y = SCREEN_HEIGHT
        
        # Physics
        # Physics
        self.speed_y = -random.uniform(PEBBLE_SPEED_START * 0.8, PEBBLE_SPEED_START * 1.2)
        self.gravity = GRAVITY * 0.8 # Slightly less gravity for pebbles to feel "lofted"
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.alive = True
        self.hit = False

    def update(self, dt):
        if not self.alive:
            return

        # Upward/Downward motion
        self.speed_y += self.gravity * dt
        self.y += self.speed_y * dt
        
        # Rotation could be added for polish
        self.rect.topleft = (self.x, self.y)
        
        # Die if off bottom after being launched
        if self.y > SCREEN_HEIGHT + 10 and self.speed_y > 0:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.surface, (self.x, self.y))

class PebbleManager:
    def __init__(self, pebble_surface):
        self.pebble_surface = pebble_surface
        self.active_pebbles = []
        self.spawn_timer = 0
        self.current_interval = PEBBLE_INITIAL_INTERVAL

    def update(self, dt, round_num):
        if round_num <= 1:
            return

        # Handle difficulty scaling: decrease interval
        # Interval decreases by 10% each round after round 2
        base_interval = PEBBLE_INITIAL_INTERVAL * math.pow(0.9, max(0, round_num - 2))
        self.current_interval = max(PEBBLE_INTERVAL_MIN, base_interval)

        self.spawn_timer += dt
        if self.spawn_timer >= self.current_interval:
            self.spawn_timer = 0
            self.active_pebbles.append(Pebble(self.pebble_surface))

        # Update pebbles
        for pebble in self.active_pebbles:
            pebble.update(dt)
        
        # Clean up
        self.active_pebbles = [p for p in self.active_pebbles if p.alive and not p.hit]

    def draw(self, screen):
        for pebble in self.active_pebbles:
            pebble.draw(screen)

    def reset(self):
        self.active_pebbles = []
        self.spawn_timer = 0
