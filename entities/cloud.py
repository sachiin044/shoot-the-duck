import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


# ── Muted blue cloud palette ────────────────────────────────────
_CLOUD_OUTER  = (180, 205, 230)   # soft steel-blue glow
_CLOUD_MID    = (200, 220, 240)   # muted pastel blue
_CLOUD_INNER  = (225, 237, 250)   # light blue-white
_CLOUD_CORE   = (242, 248, 255)   # near-white highlight


class Cloud:
    """Minimalist, elongated cloud with muted blue tones that drifts across the sky."""

    def __init__(self, x=None, y=None, speed=None):
        self.y = y if y is not None else random.randint(30, 220)

        # Big, round cloud proportions
        self.width = random.randint(280, 450)
        self.height = random.randint(80, 130)

        # Gentle drift speed (pixels / second)
        self.speed = speed if speed is not None else random.uniform(12, 35)

        # Initial x – spread across or just off-screen
        self.x = x if x is not None else random.uniform(
            -self.width, SCREEN_WIDTH + self.width
        )

        # Pre-render for performance
        self.surface = self._render()

    # ── rendering ────────────────────────────────────────────────
    def _render(self):
        pad = 24
        w = self.width + pad * 2
        h = self.height + pad * 2
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = w // 2, h // 2

        # Build shape from overlapping ellipses
        blobs = [(cx, cy, self.width * 0.50, self.height * 0.50)]
        for _ in range(random.randint(5, 8)):
            bx = cx + random.uniform(-self.width * 0.32, self.width * 0.32)
            by = cy + random.uniform(-self.height * 0.22, self.height * 0.22)
            bw = random.uniform(self.width * 0.22, self.width * 0.38)
            bh = random.uniform(self.height * 0.28, self.height * 0.45)
            blobs.append((bx, by, bw, bh))

        # Layer 1 – outer glow (very faint muted blue)
        for bx, by, bw, bh in blobs:
            r = pygame.Rect(0, 0, int(bw * 2.4), int(bh * 2.4))
            r.center = (int(bx), int(by))
            pygame.draw.ellipse(surf, (*_CLOUD_OUTER, 20), r)

        # Layer 2 – mid tone
        for bx, by, bw, bh in blobs:
            r = pygame.Rect(0, 0, int(bw * 1.9), int(bh * 1.9))
            r.center = (int(bx), int(by))
            pygame.draw.ellipse(surf, (*_CLOUD_MID, 50), r)

        # Layer 3 – inner fill
        for bx, by, bw, bh in blobs:
            r = pygame.Rect(0, 0, int(bw * 1.4), int(bh * 1.4))
            r.center = (int(bx), int(by))
            pygame.draw.ellipse(surf, (*_CLOUD_INNER, 100), r)

        # Layer 4 – bright core highlight (slight upward offset for depth)
        for bx, by, bw, bh in blobs:
            r = pygame.Rect(0, 0, int(bw * 0.85), int(bh * 0.8))
            r.center = (int(bx), int(by - bh * 0.1))
            pygame.draw.ellipse(surf, (*_CLOUD_CORE, 145), r)

        return surf

    # ── update / draw ────────────────────────────────────────────
    def update(self, dt):
        self.x += self.speed * dt
        if self.x > SCREEN_WIDTH + self.width:
            self.x = -self.width - 30
            self.y = random.randint(30, 220)
            self.surface = self._render()       # slight variation on wrap

    def draw(self, surface):
        surface.blit(
            self.surface,
            (self.x - self.surface.get_width() // 2,
             self.y - self.surface.get_height() // 2),
        )


class CloudManager:
    """Manages a layer of floating clouds."""

    def __init__(self, count=6):
        # Space clouds evenly across the screen so they don't overlap
        total_span = SCREEN_WIDTH + 400  # include off-screen buffer
        spacing = total_span // count
        self.clouds = []
        for i in range(count):
            x = -200 + i * spacing + random.randint(-30, 30)  # slight jitter
            self.clouds.append(Cloud(x=x))
        self.clouds.sort(key=lambda c: c.y)   # depth order

    def update(self, dt):
        for c in self.clouds:
            c.update(dt)

    def draw(self, surface):
        for c in self.clouds:
            c.draw(surface)
