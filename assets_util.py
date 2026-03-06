import pygame
import math
import random
from config import *

# ── Elegant modern palette ──────────────────────────────────────
_SKY_DEEP     = (25, 45, 90)      # Rich twilight blue
_SKY_ORANGE   = (255, 140, 70)    # Soft horizon orange
_SKY_GOLD     = (255, 210, 100)   # Warm sunlight
_MIST_COLOR   = (255, 230, 190)   # Warm horizon haze
_FIELD_DARK   = (40, 60, 30)      # Warmer deep green
_FIELD_MID    = (80, 100, 40)     # Olive green
_FIELD_LIGHT  = (130, 140, 60)    # Warm sunlight green
_GRASS_BASE   = (70, 90, 35)      # Warm grass base
_GRASS_TIP    = (180, 160, 80)    # Sun-kissed highlights
_HILL_SFT_1   = (40, 70, 40)      # Shadowed hill
_HILL_SFT_2   = (60, 90, 45)      # Foreground evening hill

# ── Night Palette ────────────────────────────────────────────────
_NIGHT_SKY_TOP      = (10, 15, 35)    # Deepest navy
_NIGHT_SKY_HOR      = (25, 35, 70)    # Soft horizon navy
_NIGHT_MIST         = (40, 50, 90)    # Cool blue haze
_NIGHT_MOON_GLOW    = (200, 220, 255) # Cool white moonlight
_NIGHT_FIELD_DARK   = (10, 25, 15)    # Silhouetted green
_NIGHT_FIELD_MID    = (20, 45, 25)    # Deep night grass
_NIGHT_FIELD_LIGHT  = (35, 65, 45)    # Moonlight highlights
_NIGHT_HILL_1       = (15, 30, 20)    # Distant night hill
_NIGHT_HILL_2       = (25, 40, 30)    # Mid night hill

# ── Autumn Palette ──────────────────────────────────────────────
_AUTM_SKY_TOP      = (255, 190, 180) # Pale pink sunset
_AUTM_SKY_HOR      = (255, 120, 40)  # Sunset orange
_AUTM_MIST         = (255, 200, 150) # Warm haze
_AUTM_FIELD_DARK   = (60, 35, 15)    # Rich autumn soil
_AUTM_FIELD_MID    = (100, 60, 20)   # Dry leaf brown
_AUTM_FIELD_LIGHT  = (150, 90, 30)   # Golden brown
_TREE_GOLD         = (218, 165, 32)  # Harvest gold
_TREE_ORANGE       = (205, 87, 0)    # Burnt orange
_TREE_RED          = (160, 40, 20)   # Deep autumn red

# ── Spring Palette ──────────────────────────────────────────────
_SPR_SKY_TOP       = (135, 206, 250) # Light sky blue
_SPR_SKY_HOR       = (200, 235, 255) # Soft pale blue
_SPR_FIELD_DARK    = (20, 100, 30)   # Lush forest green
_SPR_FIELD_MID     = (50, 160, 60)   # Fresh spring green
_SPR_FIELD_LIGHT   = (120, 220, 100) # Soft lime green
_TREE_LEAF_SPRING  = (144, 238, 144) # Light green leaves
_BLOOM_PINK        = (255, 182, 193) # Cherry blossom pink
_BLOOM_WHITE       = (255, 250, 240) # Floral white

# ── Monsoon Palette ─────────────────────────────────────────────
_MONS_SKY_TOP      = (45, 55, 65)    # Dark slate grey
_MONS_SKY_HOR      = (80, 95, 110)   # Cool blue-grey horizon
_MONS_MIST         = (100, 110, 120) # Rain mist
_MONS_FIELD_DARK   = (20, 35, 25)    # Wet dark earth
_MONS_FIELD_MID    = (35, 55, 45)    # Dark wet grass
_MONS_FIELD_LIGHT  = (50, 75, 65)    # Cool green highlights
_PUDDLE_COLOR      = (70, 85, 100)   # Reflective water base
# ── Winter Palette ──────────────────────────────────────────────
_WINT_SKY_TOP      = (180, 210, 240) # Pale cold blue
_WINT_SKY_HOR      = (220, 230, 240) # Winter haze light grey
_WINT_SNOW_BASE    = (245, 250, 255) # Pure white snow
_WINT_SNOW_SHADOW  = (210, 225, 245) # Soft bluish snow shadow
_WINT_TREE_SNOW    = (255, 255, 255) # Bright snow on branches
_WINT_TREE_DARK    = (40, 50, 65)    # Dark pine/branch color
_WINT_MIST         = (230, 240, 250) # Faint cold mist
# Bird Palette
BIRD_COLORS = {
    "sky_blue": (100, 180, 240),
    "emerald": (40, 180, 100),
    "yellow": (240, 210, 60),
    "coral": (240, 100, 90)
}


def create_duck_surface(color=RED):
    frames = []
    for i in range(3):
        surf = pygame.Surface((DUCK_WIDTH, DUCK_HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, color, (10, 20, 44, 30))
        pygame.draw.circle(surf, color, (45, 20), 12)
        pygame.draw.circle(surf, BLACK, (48, 18), 3)
        pygame.draw.polygon(surf, (255, 165, 0), [(55, 18), (62, 22), (55, 26)])
        wing_y = 20 + (i * 5)
        pygame.draw.ellipse(surf, (150, 0, 0), (20, wing_y, 20, 10))
        frames.append(surf)
    return frames


def create_pebble_surface():
    """Create a realistic irregular rocky pebble surface."""
    surf = pygame.Surface((PEBBLE_SIZE, PEBBLE_SIZE), pygame.SRCALPHA)
    center = PEBBLE_SIZE // 2
    
    # Generate irregular polygon points for a natural rocky look
    points = []
    num_points = random.randint(6, 9)
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # Random radius for irregularity
        dist = random.uniform(PEBBLE_SIZE * 0.3, PEBBLE_SIZE * 0.45)
        px = center + math.cos(angle) * dist
        py = center + math.sin(angle) * dist
        points.append((px, py))
    
    # 1. Base shape
    pygame.draw.polygon(surf, PEBBLE_BASE, points)
    
    # 2. Add some "cracks" and noise texture
    for _ in range(8):
        start = (random.randint(0, PEBBLE_SIZE), random.randint(0, PEBBLE_SIZE))
        end = (start[0] + random.randint(-5, 5), start[1] + random.randint(-5, 5))
        # Only draw if within polygon (simulated by distance check)
        if math.sqrt((start[0]-center)**2 + (start[1]-center)**2) < PEBBLE_SIZE * 0.4:
            pygame.draw.line(surf, PEBBLE_SHADOW, start, end, 1)
            
    # 3. Highlight side (Top-Left)
    highlight_points = points[:num_points // 2]
    if len(highlight_points) >= 3:
        pygame.draw.polygon(surf, (*PEBBLE_HIGHLIGHT, 100), highlight_points)
        
    # 4. Shadow side (Bottom-Right)
    shadow_points = points[num_points // 2:]
    if len(shadow_points) >= 3:
        pygame.draw.polygon(surf, (*PEBBLE_SHADOW, 100), shadow_points)

    return surf

def create_crosshair_surface():
    surf = pygame.Surface((CROSSHAIR_SIZE, CROSSHAIR_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, RED, (CROSSHAIR_SIZE // 2, CROSSHAIR_SIZE // 2), CROSSHAIR_SIZE // 2, 2)
    pygame.draw.line(surf, RED, (CROSSHAIR_SIZE // 2, 0), (CROSSHAIR_SIZE // 2, CROSSHAIR_SIZE), 2)
    pygame.draw.line(surf, RED, (0, CROSSHAIR_SIZE // 2), (CROSSHAIR_SIZE, CROSSHAIR_SIZE // 2), 2)
    return surf


def create_golden_hour_background():
    """Golden hour sky with gentle sun rays, soft glowing beams, and volumetric lighting."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    horizon_y = SCREEN_HEIGHT - 180
    
    # 1. Main Sky Gradient: Linear blend Day -> Golden -> Pink-ish
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        # Blend from a pale blue at the top to a warm gold/orange at the horizon
        if t < 0.7:
            # Upper sky: Soft blue to pale orange
            st = t / 0.7
            r = int(100 * (1-st) + 255 * st)
            g = int(150 * (1-st) + 180 * st)
            b = int(220 * (1-st) + 100 * st)
        else:
            # Lower sky: Warm orange to golden mist
            st = (t - 0.7) / 0.3
            r = int(255 * (1-st) + 255 * st)
            g = int(180 * (1-st) + 210 * st)
            b = int(100 * (1-st) + 150 * st)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Volumetric Soft Glow / Atmospheric Scattering
    # Large soft diffused glow around the sun area
    sun_x, sun_y = SCREEN_WIDTH * 0.7, horizon_y - 20
    for r in range(600, 0, -10):
        alpha = int(35 * (1 - r/600)**2)
        glow = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        # Warm pale yellow glow
        pygame.draw.circle(glow, (255, 240, 180, alpha), (r, r), r)
        sky.blit(glow, (sun_x - r, sun_y - r))
    
    # 2b. Explicit Sun Disk
    # A brighter, more defined central sun
    for r in range(45, 0, -5):
        alpha = int(180 * (1 - r/45))
        sun_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(sun_surf, (255, 255, 230, alpha), (r, r), r)
        sky.blit(sun_surf, (sun_x - r, sun_y - r))

    # 3. Soft Glowing Light Beams (God Rays)
    # Using many overlapping low-alpha polygons for a "soft" feel
    ray_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for i in range(12):
        angle = math.radians(150 + i * 20 + random.uniform(-8, 8))
        length = 1500
        # Wide fanned rays
        width = 0.15 + random.uniform(0, 0.1)
        p2 = (sun_x + math.cos(angle - width) * length, sun_y + math.sin(angle - width) * length)
        p3 = (sun_x + math.cos(angle + width) * length, sun_y + math.sin(angle + width) * length)
        
        # Draw multiple layers of each ray for softness
        for layer in range(5):
            alpha = int(8 * (1 - layer/5))
            pygame.draw.polygon(ray_surf, (255, 245, 200, alpha), [(sun_x, sun_y), p2, p3])
    sky.blit(ray_surf, (0, 0))

    # 4. Ground Refinement
    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_FIELD_LIGHT[0] * (1 - t) + _FIELD_DARK[0] * t)
        g = int(_FIELD_LIGHT[1] * (1 - t) + _FIELD_DARK[1] * t)
        b = int(_FIELD_LIGHT[2] * (1 - t) + _FIELD_DARK[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    hill_surf = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for x in range(SCREEN_WIDTH):
        hy = int(20 * math.sin(x * 0.004 + 1.2))
        pygame.draw.line(hill_surf, (*_HILL_SFT_1, 140), (x, 0), (x, 25 + hy))
    for x in range(SCREEN_WIDTH):
        hy = int(15 * math.sin(x * 0.006 + 2.5))
        pygame.draw.line(hill_surf, (*_HILL_SFT_2, 120), (x, 0), (x, 18 + hy))
    ground.blit(hill_surf, (0, 0))

    _draw_grass(ground, GH, _GRASS_BASE, _GRASS_TIP)
    return sky, ground

def create_night_background():
    """Cinematic night sky with cool moonlight rays, radial diffusion, and haze."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    horizon_y = SCREEN_HEIGHT - 180
    
    # 1. Deep Navy Gradient
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        r = int(10 * (1 - t) + 30 * t)
        g = int(15 * (1 - t) + 40 * t)
        b = int(45 * (1 - t) + 85 * t)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Moonlight Diffusion (Upper Corner)
    moon_x, moon_y = SCREEN_WIDTH * 0.8, 120
    for r in range(500, 0, -10):
        # Soft radial diffusion
        alpha = int(40 * (1 - r/500)**2)
        glow = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (200, 225, 255, alpha), (r, r), r)
        sky.blit(glow, (moon_x - r, moon_y - r))

    haze_surf = pygame.Surface((SCREEN_WIDTH, 300), pygame.SRCALPHA)
    for y in range(300):
        alpha = int(30 * (1 - y/300))
        pygame.draw.line(haze_surf, (*_NIGHT_MIST, alpha), (0, 300 - y), (SCREEN_WIDTH, 300 - y))
    sky.blit(haze_surf, (0, horizon_y - 120))

    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_NIGHT_FIELD_LIGHT[0] * (1 - t) + _NIGHT_FIELD_DARK[0] * t)
        g = int(_NIGHT_FIELD_LIGHT[1] * (1 - t) + _NIGHT_FIELD_DARK[1] * t)
        b = int(_NIGHT_FIELD_LIGHT[2] * (1 - t) + _NIGHT_FIELD_DARK[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    hill_surf = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for x in range(SCREEN_WIDTH):
        hy = int(20 * math.sin(x * 0.004 + 1.2))
        pygame.draw.line(hill_surf, (*_NIGHT_HILL_1, 140), (x, 0), (x, 25 + hy))
    for x in range(SCREEN_WIDTH):
        hy = int(15 * math.sin(x * 0.006 + 2.5))
        pygame.draw.line(hill_surf, (*_NIGHT_HILL_2, 120), (x, 0), (x, 18 + hy))
    ground.blit(hill_surf, (0, 0))

    # Night grass highlights (subdued)
    _draw_grass(ground, GH, _NIGHT_FIELD_DARK, (100, 120, 100))
    return sky, ground

def _draw_grass(ground, GH, base_color, tip_color):
    """Helper to draw grass blades on a ground surface."""
    random.seed(42)
    num_blades = 150
    for _ in range(num_blades):
        bx = random.randint(0, SCREEN_WIDTH)
        by = random.randint(20, GH - 20)
        depth = by / GH
        base_w = int(2 + depth * 3)
        h = int(8 + depth * 12)
        tilt = random.randint(-4, 4)
        points = [(bx - base_w//2, by), (bx + base_w//2, by), (bx + tilt, by - h)]
        color = (int(base_color[0] * (1-depth*0.3)), int(base_color[1] * (1-depth*0.3)), int(base_color[2] * (1-depth*0.3)))
        pygame.draw.polygon(ground, (*color, 250), points)
        pygame.draw.line(ground, (*tip_color, 120), (bx + tilt, by - h), (bx, by - h//2), 1)
    random.seed()

def create_autumn_background():
    """Warm autumn landscape with sunset sky, golden trees, and scattered leaves."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    horizon_y = SCREEN_HEIGHT - 180
    
    # 1. Soft Sunset Gradient (Pink to Orange)
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        # Upper sky: Pink to haze
        if t < 0.6:
            st = t / 0.6
            r = int(_AUTM_SKY_TOP[0] * (1-st) + _AUTM_SKY_HOR[0] * st)
            g = int(_AUTM_SKY_TOP[1] * (1-st) + _AUTM_SKY_HOR[1] * st)
            b = int(_AUTM_SKY_TOP[2] * (1-st) + _AUTM_SKY_HOR[2] * st)
        else:
            # Lower sky: Orange to horizon glow
            st = (t - 0.6) / 0.4
            r = int(_AUTM_SKY_HOR[0] * (1-st) + _AUTM_MIST[0] * st)
            g = int(_AUTM_SKY_HOR[1] * (1-st) + _AUTM_MIST[1] * st)
            b = int(_AUTM_SKY_HOR[2] * (1-st) + _AUTM_MIST[2] * st)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Procedural Distant Trees (Blurred)
    tree_layer = pygame.Surface((SCREEN_WIDTH, 400), pygame.SRCALPHA)
    random.seed(99) # Consistent trees
    for _ in range(12):
        tx = random.randint(-50, SCREEN_WIDTH)
        tw = random.randint(120, 220)
        th = random.randint(200, 300)
        ty = 350 - th
        # Draw a soft triangle-ish tree
        color = random.choice([_TREE_GOLD, _TREE_ORANGE, _TREE_RED])
        tree_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
        # Main foliage
        pygame.draw.polygon(tree_surf, (*color, 180), [(tw//2, 0), (0, th), (tw, th)])
        # Slight blur effect by drawing smaller overlapping versions
        for i in range(3):
            pygame.draw.polygon(tree_surf, (*color, 40), [(tw//2, i*10), (i*10, th), (tw-i*10, th)])
        # Trunk
        pygame.draw.rect(tree_surf, (50, 30, 10, 200), (tw//2 - 5, th - 30, 10, 30))
        
        # Blur the distant trees subtly
        tree_layer.blit(tree_surf, (tx, ty))
    
    # Simple blur pass (subtle)
    # Note: pygame doesn't have a fast blur, so we simulate depth with alpha and overlap
    sky.blit(tree_layer, (0, horizon_y - 300))

    # 3. Autumn Ground
    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_AUTM_FIELD_LIGHT[0] * (1 - t) + _AUTM_FIELD_DARK[0] * t)
        g = int(_AUTM_FIELD_LIGHT[1] * (1 - t) + _AUTM_FIELD_DARK[1] * t)
        b = int(_AUTM_FIELD_LIGHT[2] * (1 - t) + _AUTM_FIELD_DARK[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # Scattered dry leaves on ground
    for _ in range(80):
        lx = random.randint(0, SCREEN_WIDTH)
        ly = random.randint(40, GH - 10)
        size = random.randint(3, 7)
        l_color = random.choice([_TREE_GOLD, _TREE_ORANGE, (120, 70, 20)])
        pygame.draw.ellipse(ground, (*l_color, 200), (lx, ly, size*1.5, size))

    _draw_grass(ground, GH, _AUTM_FIELD_DARK, _TREE_GOLD)
    random.seed()
    return sky, ground

def create_spring_background():
    """Bright and refreshing spring landscape with light-green trees and blooms."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 1. Soft Blue Sky Gradient
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        r = int(_SPR_SKY_TOP[0] * (1-t) + _SPR_SKY_HOR[0] * t)
        g = int(_SPR_SKY_TOP[1] * (1-t) + _SPR_SKY_HOR[1] * t)
        b = int(_SPR_SKY_TOP[2] * (1-t) + _SPR_SKY_HOR[2] * t)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Fluffy White Clouds (Decorative/Static in background)
    random.seed(77)
    for _ in range(5):
        cx = random.randint(100, SCREEN_WIDTH - 100)
        cy = random.randint(50, 200)
        cw = random.randint(100, 200)
        pygame.draw.ellipse(sky, (255, 255, 255, 120), (cx, cy, cw, cw//2))
        pygame.draw.ellipse(sky, (255, 255, 255, 120), (cx+cw//3, cy-10, cw, cw//2))

    # 3. Fresh Spring Trees with Blooms
    tree_layer = pygame.Surface((SCREEN_WIDTH, 400), pygame.SRCALPHA)
    for _ in range(10):
        tx = random.randint(-50, SCREEN_WIDTH)
        tw = random.randint(100, 180)
        th = random.randint(180, 280)
        ty = 350 - th
        
        # Draw soft rounded spring tree
        tree_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
        # Foliage (Light Green)
        pygame.draw.ellipse(tree_surf, (*_TREE_LEAF_SPRING, 180), (0, 0, tw, th - 40))
        # Add some "blooms"
        for _ in range(15):
            bx = random.randint(10, tw-10)
            by = random.randint(10, th-60)
            b_color = random.choice([_BLOOM_PINK, _BLOOM_WHITE])
            pygame.draw.circle(tree_surf, (*b_color, 220), (bx, by), random.randint(2, 4))
            
        # Trunk
        pygame.draw.rect(tree_surf, (80, 60, 40, 200), (tw//2 - 4, th - 50, 8, 50))
        tree_layer.blit(tree_surf, (tx, ty))
    
    sky.blit(tree_layer, (0, SCREEN_HEIGHT - 180 - 300))

    # 4. Lush Spring Ground
    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_SPR_FIELD_LIGHT[0] * (1 - t) + _SPR_FIELD_DARK[0] * t)
        g = int(_SPR_FIELD_LIGHT[1] * (1 - t) + _SPR_FIELD_DARK[1] * t)
        b = int(_SPR_FIELD_LIGHT[2] * (1 - t) + _SPR_FIELD_DARK[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # Blooming flowers in the grass
    for _ in range(60):
        fx = random.randint(0, SCREEN_WIDTH)
        fy = random.randint(30, GH - 10)
        f_color = random.choice([_BLOOM_PINK, _BLOOM_WHITE, (255, 255, 100)]) # Pink, White, Yellow
        pygame.draw.circle(ground, (*f_color, 255), (fx, fy), random.randint(2, 3))

    _draw_grass(ground, GH, _SPR_FIELD_DARK, _SPR_FIELD_LIGHT)
    random.seed()
    return sky, ground

def _draw_puddles(ground, GH):
    """Draw static puddles on the ground for monsoon theme."""
    random.seed(44)
    for _ in range(8):
        px = random.randint(50, SCREEN_WIDTH - 150)
        py = random.randint(20, GH - 40)
        pw = random.randint(60, 140)
        ph = random.randint(15, 30)
        # Main puddle water
        pygame.draw.ellipse(ground, (*_PUDDLE_COLOR, 150), (px, py, pw, ph))
        # Subtle rim/reflection
        pygame.draw.ellipse(ground, (255, 255, 255, 30), (px+2, py+2, pw-4, ph-4), 1)
    random.seed()

def create_monsoon_background():
    """Realistic monsoon rainy background with dark clouds and wet ground."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 1. Dark Overcast Sky Gradient (Cool grey-blue)
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        r = int(_MONS_SKY_TOP[0] * (1-t) + _MONS_SKY_HOR[0] * t)
        g = int(_MONS_SKY_TOP[1] * (1-t) + _MONS_SKY_HOR[1] * t)
        b = int(_MONS_SKY_TOP[2] * (1-t) + _MONS_SKY_HOR[2] * t)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Distant Thunderheads (Darker cloud masses)
    random.seed(123)
    for _ in range(4):
        cx = random.randint(-100, SCREEN_WIDTH)
        cy = random.randint(-50, 100)
        cw = random.randint(300, 600)
        pygame.draw.ellipse(sky, (30, 35, 45, 100), (cx, cy, cw, cw//3))
        
    # 3. Ground Mist/Fog for depth
    mist_layer = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
    for y in range(150):
        alpha = int(100 * (1 - y/150))
        pygame.draw.line(mist_layer, (*_MONS_MIST, alpha), (0, y), (SCREEN_WIDTH, y))
    sky.blit(mist_layer, (0, SCREEN_HEIGHT - 180 - 100))

    # 4. Wet Monsoon Ground
    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_MONS_FIELD_DARK[0] * (1 - t) + _MONS_FIELD_MID[0] * t)
        g = int(_MONS_FIELD_DARK[1] * (1 - t) + _MONS_FIELD_MID[1] * t)
        b = int(_MONS_FIELD_DARK[2] * (1 - t) + _MONS_FIELD_MID[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    _draw_puddles(ground, GH)
    _draw_grass(ground, GH, _MONS_FIELD_DARK, _MONS_FIELD_LIGHT)
    
    random.seed()
    return sky, ground

def create_winter_background():
    """Realistic winter landscape with snow-covered trees and soft snowfall haze."""
    sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    horizon_y = SCREEN_HEIGHT - 180
    
    # 1. Pale Blue to Light Grey Gradient
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        r = int(_WINT_SKY_TOP[0] * (1-t) + _WINT_SKY_HOR[0] * t)
        g = int(_WINT_SKY_TOP[1] * (1-t) + _WINT_SKY_HOR[1] * t)
        b = int(_WINT_SKY_TOP[2] * (1-t) + _WINT_SKY_HOR[2] * t)
        pygame.draw.line(sky, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 2. Distant Snow-Capped Mountains (Soft depth blur effect)
    random.seed(88)
    for _ in range(3):
        mx = random.randint(-200, SCREEN_WIDTH)
        mw = random.randint(400, 800)
        mh = random.randint(300, 500)
        my = horizon_y - mh + 100
        pygame.draw.polygon(sky, (*_WINT_SKY_HOR, 150), [(mx, my+mh), (mx+mw//2, my), (mx+mw, my+mh)])
        # Snow caps
        pygame.draw.polygon(sky, (255, 255, 255, 100), [(mx+mw//4, my+mh//2), (mx+mw//2, my), (mx+3*mw//4, my+mh//2)])

    # 3. Distant Houses/Rooftops
    house_layer = pygame.Surface((SCREEN_WIDTH, 400), pygame.SRCALPHA)
    for _ in range(5):
        hx = random.randint(50, SCREEN_WIDTH - 150)
        hw = random.randint(60, 100)
        hh = random.randint(40, 60)
        hy = 350 - hh
        
        # House body
        pygame.draw.rect(house_layer, (60, 45, 40, 220), (hx, hy, hw, hh))
        # Roof (Triangle)
        roof_p1 = (hx - 10, hy)
        roof_p2 = (hx + hw//2, hy - 30)
        roof_p3 = (hx + hw + 10, hy)
        pygame.draw.polygon(house_layer, (80, 60, 50, 240), [roof_p1, roof_p2, roof_p3])
        # Snow on roof
        snow_p1 = (hx - 10, hy)
        snow_p2 = (hx + hw//2, hy - 35) # Slightly thicker
        snow_p3 = (hx + hw + 10, hy)
        pygame.draw.polygon(house_layer, (255, 255, 255, 220), [snow_p1, (hx+hw//2, hy-30), snow_p2, snow_p3])
        # Window
        pygame.draw.rect(house_layer, (240, 220, 100, 150), (hx + hw//4, hy + hh//3, 15, 15)) # Warm glow

    sky.blit(house_layer, (0, horizon_y - 300))

    # 4. Snow-Covered Trees
    tree_layer = pygame.Surface((SCREEN_WIDTH, 400), pygame.SRCALPHA)
    for _ in range(12):
        tx = random.randint(-50, SCREEN_WIDTH)
        tw = random.randint(80, 150)
        th = random.randint(150, 300)
        ty = 350 - th
        
        # Conifer shape
        tree_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
        # Main body (dark branches)
        pygame.draw.polygon(tree_surf, (*_WINT_TREE_DARK, 220), [(tw//2, 0), (0, th), (tw, th)])
        # Natural snow layering on branches
        for i in range(5):
            layer_y = i * (th // 5)
            layer_w = tw * (1 - i/6)
            pygame.draw.ellipse(tree_surf, (*_WINT_TREE_SNOW, 200), (tw//2 - layer_w//2, layer_y, layer_w, 15))
            
        tree_layer.blit(tree_surf, (tx, ty))
    
    sky.blit(tree_layer, (0, horizon_y - 280))

    # 4. Smooth White Ground with texture
    GH = 180
    ground = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        t = y / GH
        r = int(_WINT_SNOW_BASE[0] * (1 - t) + _WINT_SNOW_SHADOW[0] * t)
        g = int(_WINT_SNOW_BASE[1] * (1 - t) + _WINT_SNOW_SHADOW[1] * t)
        b = int(_WINT_SNOW_BASE[2] * (1 - t) + _WINT_SNOW_SHADOW[2] * t)
        pygame.draw.line(ground, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # Subtle snow texture and drift shadows
    for _ in range(40):
        sx = random.randint(0, SCREEN_WIDTH)
        sy = random.randint(10, GH - 20)
        sw = random.randint(40, 100)
        sh = random.randint(5, 15)
        pygame.draw.ellipse(ground, (*_WINT_SNOW_SHADOW, 80), (sx, sy, sw, sh))

    # Cold mist near ground
    mist_layer = pygame.Surface((SCREEN_WIDTH, GH), pygame.SRCALPHA)
    for y in range(GH):
        alpha = int(60 * (1 - y/GH))
        pygame.draw.line(mist_layer, (*_WINT_MIST, alpha), (0, y), (SCREEN_WIDTH, y))
    ground.blit(mist_layer, (0, 0))

    random.seed()
    return sky, ground

def create_background():
    """Legacy wrapper, defaults to day."""
    return create_golden_hour_background()


