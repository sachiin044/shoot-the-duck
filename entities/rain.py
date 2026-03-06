import pygame
import random
from config import *

class RainDrop:
    def __init__(self):
        self.reset()
        # Randomized starting position for initial drops to prevent a "wall" or rain
        self.y = random.uniform(0, SCREEN_HEIGHT)

    def reset(self):
        self.x = random.uniform(-100, SCREEN_WIDTH)
        self.y = random.uniform(-100, -10)
        self.speed = random.uniform(500, 800) # Reduced from 800-1200 for a gentler fall
        self.length = random.uniform(20, 35)
        self.width = random.randint(1, 2)
        # Cool blue-grey rain color with alpha
        self.color = (170, 190, 210, 120)

    def update(self, dt):
        # Diagonal fall (simulating wind - reduced speed)
        self.x += 120 * dt 
        self.y += self.speed * dt
        
        if self.y > SCREEN_HEIGHT + 20 or self.x > SCREEN_WIDTH + 20:
            self.reset()

    def draw(self, screen):
        # Draw as a thin diagonal line
        pygame.draw.line(screen, self.color, (self.x, self.y), 
                         (self.x + 5, self.y + self.length), self.width)

class PuddleRipple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1.0
        self.max_radius = random.uniform(10, 25)
        self.alpha = 130
        self.speed = random.uniform(30, 60)
        self.alive = True

    def update(self, dt):
        self.radius += self.speed * dt
        self.alpha = max(0, 130 * (1 - self.radius / self.max_radius))
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.alive = False

    def draw(self, screen):
        if self.alpha > 0:
            # Draw a subtle circle for the ripple
            ripple_surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surf, (200, 220, 255, int(self.alpha)), 
                               (int(self.radius), int(self.radius)), int(self.radius), 1)
            screen.blit(ripple_surf, (int(self.x - self.radius), int(self.y - self.radius)))

class RainManager:
    def __init__(self, count=250):
        self.drops = [RainDrop() for _ in range(count)]
        self.ripples = []
        self.ripple_spawn_timer = 0

    def update(self, dt):
        for drop in self.drops:
            drop.update(dt)
            
        # Periodically spawn ripples in the "ground" area
        self.ripple_spawn_timer += dt
        if self.ripple_spawn_timer >= 0.04:
            # Puddles and wet ground are in the lower field
            rx = random.uniform(0, SCREEN_WIDTH)
            ry = random.uniform(SCREEN_HEIGHT - 170, SCREEN_HEIGHT - 10)
            self.ripples.append(PuddleRipple(rx, ry))
            self.ripple_spawn_timer = 0

        for ripple in self.ripples[:]:
            ripple.update(dt)
            if not ripple.alive:
                self.ripples.remove(ripple)

    def draw(self, screen):
        # Ripples are drawn on the ground layer
        for ripple in self.ripples:
            ripple.draw(screen)
            
        # Rain is drawn over everything
        for drop in self.drops:
            drop.draw(screen)
