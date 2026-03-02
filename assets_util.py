import pygame
from config import *

def create_duck_surface(color=RED):
    frames = []
    for i in range(3):
        surf = pygame.Surface((DUCK_WIDTH, DUCK_HEIGHT), pygame.SRCALPHA)
        # Body
        pygame.draw.ellipse(surf, color, (10, 20, 44, 30))
        # Head
        pygame.draw.circle(surf, color, (45, 20), 12)
        # Eye
        pygame.draw.circle(surf, BLACK, (48, 18), 3)
        # Beak
        pygame.draw.polygon(surf, (255, 165, 0), [(55, 18), (62, 22), (55, 26)])
        # Wing (animate based on frame index)
        wing_y = 20 + (i * 5)
        pygame.draw.ellipse(surf, (150, 0, 0), (20, wing_y, 20, 10))
        
        frames.append(surf)
    return frames

def create_crosshair_surface():
    surf = pygame.Surface((CROSSHAIR_SIZE, CROSSHAIR_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, RED, (CROSSHAIR_SIZE//2, CROSSHAIR_SIZE//2), CROSSHAIR_SIZE//2, 2)
    pygame.draw.line(surf, RED, (CROSSHAIR_SIZE//2, 0), (CROSSHAIR_SIZE//2, CROSSHAIR_SIZE), 2)
    pygame.draw.line(surf, RED, (0, CROSSHAIR_SIZE//2), (CROSSHAIR_SIZE, CROSSHAIR_SIZE//2), 2)
    return surf

def create_background():
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    sky.fill(SKY_BLUE)
    # Evenly distributed fluffy clouds
    cloud_positions = [
        (100, 80),
        (350, 140),
        (600, 70),
        (850, 160),
        (1080, 90),
    ]
    # Cloud shape templates: list of (dx, dy, radius) offsets from base position
    cloud_shapes = [
        [(-30, 5, 28), (0, 0, 35), (30, 5, 28), (0, -15, 25), (15, -10, 22)],
        [(-25, 8, 25), (5, 0, 32), (35, 8, 25), (5, -12, 22)],
        [(-35, 5, 30), (-5, -5, 35), (25, 0, 30), (0, -18, 25), (30, -12, 20)],
        [(-20, 5, 22), (10, 0, 30), (40, 5, 22), (10, -12, 20)],
        [(-30, 5, 28), (0, 0, 35), (30, 5, 28), (-15, -12, 22), (15, -12, 22)],
    ]
    for i, (bx, by) in enumerate(cloud_positions):
        shape = cloud_shapes[i % len(cloud_shapes)]
        for dx, dy, r in shape:
            # Soft outer glow
            glow = pygame.Surface((r * 2 + 8, r * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 255, 80), (r + 4, r + 4), r + 4)
            sky.blit(glow, (bx + dx - r - 4, by + dy - r - 4))
            # Solid cloud body
            part = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(part, (255, 255, 255, 220), (r, r), r)
            sky.blit(part, (bx + dx - r, by + dy - r))
    
    ground = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
    ground.fill((34, 139, 34)) # Forest Green
    return sky, ground
