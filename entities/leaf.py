import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT

LEAF_COLORS = [
    (218, 165, 32, 200),  # Goldenrod
    (205, 87, 0, 200),    # OrangeRed
    (160, 40, 20, 200),    # Deep Red
    (139, 69, 19, 200)    # SaddleBrown
]

class LeafParticle:
    def __init__(self):
        self.reset()
        # Random initial position
        self.x = random.uniform(-50, SCREEN_WIDTH)
        self.y = random.uniform(-100, SCREEN_HEIGHT)

    def reset(self):
        self.x = random.uniform(-50, SCREEN_WIDTH)
        self.y = random.uniform(-50, -20)
        self.size = random.randint(4, 8)
        self.color = random.choice(LEAF_COLORS)
        self.speed_y = random.uniform(30, 80)
        self.speed_x = random.uniform(20, 60)
        self.phase = random.uniform(0, math.pi * 2)
        self.freq = random.uniform(1.5, 3.0)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-100, 100)

    def update(self, dt):
        self.y += self.speed_y * dt
        # S-curve drift
        self.phase += self.freq * dt
        drift = math.sin(self.phase) * 50
        self.x += (self.speed_x + drift) * dt
        self.rotation += self.rot_speed * dt

        if self.y > SCREEN_HEIGHT or self.x > SCREEN_WIDTH + 50:
            self.reset()

    def draw(self, screen):
        # Draw a small rotated ellipse for the leaf
        leaf_surf = pygame.Surface((self.size * 2, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surf, self.color, (0, 0, self.size * 2, self.size))
        rotated_leaf = pygame.transform.rotate(leaf_surf, self.rotation)
        screen.blit(rotated_leaf, (int(self.x), int(self.y)))

class LeafManager:
    def __init__(self, count=40):
        self.leaves = [LeafParticle() for _ in range(count)]

    def update(self, dt):
        for leaf in self.leaves:
            leaf.update(dt)

    def draw(self, screen):
        for leaf in self.leaves:
            leaf.draw(screen)
