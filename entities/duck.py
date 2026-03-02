import pygame
import math
import random
import time
from config import *

class Duck:
    def __init__(self, x, y, speed_mult=1.0, duck_type="normal"):
        self.type = duck_type
        self.spawn_time = time.time()
        self.pos = pygame.Vector2(x, y)
        
        # Adjust speed based on type
        type_speed_mod = DUCK_TYPES.get(self.type, {}).get("speed_mod", 1.0)
        self.speed = DUCK_BASE_SPEED * speed_mult * type_speed_mod * random.uniform(0.8, 1.2)
        # Track base Y for precise pattern calculation
        self.base_y = y
        self.direction = pygame.Vector2(1, 0)
        
        # Flight curve parameters
        self.pattern = random.choice(["zigzag", "sinusoidal", "diagonal", "dive"])
        self.timer = 0
        self.zigzag_interval = random.uniform(0.6, 1.2)
        self.amplitude = random.uniform(20, 60)
        self.frequency = random.uniform(1.5, 3.5)
        
        # Complexity layers
        self.diagonal_slope = random.choice([-0.4, -0.3, 0.3, 0.4])  # rise/run
        self.dive_triggered = False
        self.dive_time = random.uniform(1.5, 3.0)  # seconds before diving
        self.speed_burst_timer = 0
        self.speed_burst_interval = random.uniform(2.0, 4.0)
        self.speed_burst_active = False
        self.current_speed = self.speed
        
        self.alive = True
        self.hit = False
        self.escaping = False
        self.falling = False
        self.velocity = pygame.Vector2(0, 0)
        
        # Set initial direction based on side
        if x > SCREEN_WIDTH / 2:
            self.direction.x = -1
        else:
            self.direction.x = 1
            
        # Animation
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = random.uniform(8, 14)  # wing flap speed
            
        self.rect = pygame.Rect(self.pos.x, self.pos.y, DUCK_WIDTH, DUCK_HEIGHT)

    def update(self, dt):
        self.timer += dt
        
        if self.falling:
            self.velocity.y += GRAVITY * dt
            self.pos += self.velocity * dt
            if self.pos.y > SCREEN_HEIGHT:
                self.alive = False
        elif self.escaping:
            self.velocity.y = -self.speed * 1.5
            self.pos += self.velocity * dt
            if self.pos.y < -DUCK_HEIGHT:
                self.alive = False
        else:
            # Speed burst logic: occasional quick dashes
            self.speed_burst_timer += dt
            if self.speed_burst_active:
                if self.speed_burst_timer >= 0.3:  # burst lasts 0.3s
                    self.speed_burst_active = False
                    self.current_speed = self.speed
                    self.speed_burst_timer = 0
            elif self.speed_burst_timer >= self.speed_burst_interval:
                self.speed_burst_active = True
                self.current_speed = self.speed * 1.8
                self.speed_burst_timer = 0
            
            # Horizontal motion
            self.pos.x += self.direction.x * self.current_speed * dt
            
            # Pattern vertical motion (Absolute positioning relative to base_y)
            if self.pattern == "zigzag":
                offset = (math.cos(self.timer * math.pi / self.zigzag_interval) * 30)
                self.pos.y = self.base_y + offset
            elif self.pattern == "sinusoidal":
                offset = math.sin(self.timer * self.frequency) * self.amplitude
                self.pos.y = self.base_y + offset
            elif self.pattern == "diagonal":
                # Fly at an angle, gradually changing altitude
                self.base_y += self.diagonal_slope * self.current_speed * dt
                # Clamp to keep on screen
                self.base_y = max(50, min(SCREEN_HEIGHT - 250, self.base_y))
                self.pos.y = self.base_y
            elif self.pattern == "dive":
                # Fly straight, then suddenly dive down and pull back up
                if not self.dive_triggered and self.timer >= self.dive_time:
                    self.dive_triggered = True
                if self.dive_triggered:
                    # Sharp V-shaped dive: go down then back up
                    dive_phase = self.timer - self.dive_time
                    if dive_phase < 0.5:
                        self.pos.y = self.base_y + (dive_phase / 0.5) * 120
                    elif dive_phase < 1.0:
                        self.pos.y = self.base_y + ((1.0 - dive_phase) / 0.5) * 120
                    else:
                        self.pos.y = self.base_y
                        self.dive_triggered = False
                        self.dive_time = self.timer + random.uniform(1.5, 3.0)
                else:
                    self.pos.y = self.base_y
            else:  # linear
                self.base_y += random.uniform(-10, 10) * dt
                self.pos.y = self.base_y
            
            # Screen bounce/escape check
            if self.pos.x < -DUCK_WIDTH or self.pos.x > SCREEN_WIDTH:
                self.escaping = True

        self.rect.topleft = (self.pos.x, self.pos.y)
        
        # Update animation frame
        if not self.falling and not self.hit:
            self.animation_timer += dt
            if self.animation_timer >= 1 / self.animation_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 3

    def is_missed(self):
        """Returns true if the duck has escaped the screen without being hit."""
        return self.escaping and (self.pos.y < -DUCK_HEIGHT)

    def die(self):
        self.hit = True
        self.falling = True
        self.velocity = pygame.Vector2(0, 0) # Stop horizontal movement

    def draw(self, screen, frames):
        # frames should be a list of wing animation surfaces
        draw_surf = frames[self.frame_index]

        if self.direction.x < 0:
            draw_surf = pygame.transform.flip(draw_surf, True, False)
            
        if self.falling:
            draw_surf = pygame.transform.flip(draw_surf, False, True)
            
        screen.blit(draw_surf, self.rect)
