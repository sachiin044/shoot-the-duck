import pygame

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Game Balance
INITIAL_BULLETS = 3
DUCK_BASE_SPEED = 150  # Pixels per second
DUCK_SPEED_INCREMENT = 1.1  # Multiplied each round
SPAWN_RATE_START = 2.0  # Seconds between spawns
SPAWN_RATE_MIN = 0.5
RELOAD_TIME = 1.0  # Seconds

# Assets
DUCK_WIDTH = 64
DUCK_HEIGHT = 64
CROSSHAIR_SIZE = 48

# Physics
GRAVITY = 500  # Pixels per second squared for falling ducks

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
PLAYING = "PLAYING"
ROUND_OVER = "ROUND_OVER"
GAME_OVER = "GAME_OVER"
