import pygame
from config import *

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets = INITIAL_BULLETS
        self.reloading = False
        self.reload_timer = 0
        self.shoot_cooldown = 0.2
        self.cooldown_timer = 0
        self.active = True

    def update(self, dt):
        # Move crosshair to mouse
        mx, my = pygame.mouse.get_pos()
        self.pos.x = mx
        self.pos.y = my
        
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
            
        if self.reloading:
            self.reload_timer += dt
            if self.reload_timer >= RELOAD_TIME:
                self.bullets = INITIAL_BULLETS
                self.reloading = False
                self.reload_timer = 0

    def can_shoot(self):
        return self.bullets > 0 and not self.reloading and self.cooldown_timer <= 0

    def shoot(self):
        self.bullets -= 1
        self.cooldown_timer = self.shoot_cooldown
        if self.bullets <= 0:
            self.reloading = True
            
    def draw(self, screen, surface):
        rect = surface.get_rect(center=(self.pos.x, self.pos.y))
        screen.blit(surface, rect)
