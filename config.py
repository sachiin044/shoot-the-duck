import pygame
import ctypes
import os

# Enable High DPI awareness for Windows
if os.name == 'nt':
    try:
        # High DPI awareness for Windows 8.1+ (1) or legacy Windows (SetProcessDPIAware)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Screen settings
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
FPS = 60
FULLSCREEN_ENABLED = True

# API and Database Constants
VALIDATE_API_URL = "https://pvs.kiitfest.org/api/validate"
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "Leaderboard"
COLLECTION_NAME = "leaderboard"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
PEBBLE_BASE = (100, 95, 90)
PEBBLE_SHADOW = (60, 55, 50)
PEBBLE_HIGHLIGHT = (160, 155, 150)
GOLD = (255, 215, 0)
DARK_GRAY = (40, 40, 40)
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER = (255, 50, 50)


# Game Balance
INITIAL_BULLETS = 3
DUCK_BASE_SPEED = 180  # Further reduced for easier early rounds
DUCK_SPEED_INCREMENT = 1.05  # Slower scaling per round
SPAWN_RATE_START = 0.5  # Further reduced from 1.0 (original was 2.0)
SPAWN_RATE_MIN = 0.1    # Further reduced from 0.3 (original was 0.5)
RELOAD_TIME = 1.0  # Seconds

# Assets
DUCK_WIDTH = 512
DUCK_HEIGHT = 512
CROSSHAIR_SIZE = 100

# Physics
GRAVITY = 500  # Pixels per second squared for falling ducks
ZIGZAG_ACCEL = 100.0 # Reduced from 150 for much smoother transitions
ZIGZAG_DAMPING = 0.86 
MIN_DIRECTION_CHANGE_INTERVAL = 1.4 # Increased from 1.0 for less frequent turns

# Duck Types and Scores
DUCK_TYPES = {
    "normal": {"base_score": 100, "speed_mod": 1.0},
    "fast": {"base_score": 200, "speed_mod": 1.5},
    "zigzag": {"base_score": 250, "speed_mod": 1.2},
    "golden": {"base_score": 500, "speed_mod": 1.8}
}

# Combo/Multiplier Tiers
COMBO_TIERS = [
    (10, 3.0),
    (5, 2.0),
    (3, 1.5),
    (0, 1.0)
]

# Bonuses
REACTION_BONUS_MAX = 300
REACTION_BONUS_COEFF = 0.1
PERFECT_ROUND_BONUS = 2000
ACCURACY_TIERS = [
    (0.9, 1000),
    (0.75, 500),
    (0.6, 200)
]

# State Constants
MENU = "MENU"
COUNTDOWN = "COUNTDOWN"
PLAYING = "PLAYING"
ROUND_OVER = "ROUND_OVER"
GAME_OVER = "GAME_OVER"

# Difficulty Scaling
SPEED_INCREMENT_PER_MISS = 1.02  # Minimal penalty for missing
DENSITY_INCREMENT_PER_MISS = 0.5
MAX_MISSES_ALLOWED = 6 # More lives for the player
SPEED_DAMPENING_FACTOR = 0.96  # Slow down birds slightly each round after start
SPEED_DAMPENING_START_ROUND = 5
MAX_DUCKS_CAP = 40 # Increased from 25 to allow massive density

# Pebble Hazard
PEBBLE_SIZE = 50
PEBBLE_INITIAL_INTERVAL = 5.0 # Seconds
PEBBLE_INTERVAL_MIN = 1.0
PEBBLE_SPEED_START = 800
PEBBLE_PENALTY = 50
