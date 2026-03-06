import pygame
import sys
import time
import random
from config import *
from systems.state_manager import StateManager
from systems.spawner import Spawner
from systems.score_manager import ScoreManager
from entities.player import Player
from entities.cloud import CloudManager
from entities.pebble import PebbleManager
from ui.hud import HUD
from entities.leaf import LeafManager
from entities.snow import SnowManager
from entities.rain import RainManager
from assets_util import (create_duck_surface, create_crosshair_surface, 
                         create_golden_hour_background, create_night_background, 
                         create_autumn_background, create_winter_background,
                         create_monsoon_background,
                         create_pebble_surface, BIRD_COLORS)

class DuckHuntGame:
    def __init__(self):
        pygame.init()
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE if FULLSCREEN_ENABLED else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption("Duck Hunt - Production Quality")
        self.clock = pygame.time.Clock()
        
        # Core Systems
        self.state_manager = StateManager()
        self.spawner = Spawner()
        self.score_manager = ScoreManager()
        self.player = Player()
        self.hud = HUD()
        
        # Assets
        self.duck_surfaces = {
            name: create_duck_surface(color)
            for name, color in BIRD_COLORS.items()
        }
        self.crosshair_surf = create_crosshair_surface()
        
        # Day/Night/Autumn/Spring Backgrounds
        self.day_sky, self.day_ground = create_golden_hour_background()
        self.night_sky, self.night_ground = create_night_background()
        self.autumn_sky, self.autumn_ground = create_autumn_background()
        self.winter_sky, self.winter_ground = create_winter_background()
        self.monsoon_sky, self.monsoon_ground = create_monsoon_background()
        
        self.pebble_surf = create_pebble_surface()
        self.pebble_manager = PebbleManager(self.pebble_surf)
        
        self.leaf_manager = LeafManager(count=40)
        self.snow_manager = SnowManager(count=100)
        self.rain_manager = RainManager(count=300)
        self.cloud_manager = CloudManager(count=6)
        
        # State Variables
        self.countdown_timer = 3.0
        self.is_day = True
        self.last_round = 1
        self.bg_transition_alpha = 0.0 # 0 to 255
        self.transition_speed = 85.0 # Slightly slower for cinematic feel
        
        # Monsoon/Lightning State
        self.lightning_timer = random.uniform(3.0, 8.0)
        self.lightning_alpha = 0.0
        
        # Transition surfaces
        self.prev_sky = self.day_sky
        self.prev_ground = self.day_ground
        
        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state_manager.is_state(PLAYING):
                    if self.player.can_shoot():
                        self.player.shoot()
                        self.score_manager.register_shot() # Track accuracy
                        self.check_collisions()
                elif self.state_manager.is_state(GAME_OVER):
                    if self.hud.handle_game_over_event(event, self.score_manager):
                        self.reset_game()
                        self.countdown_timer = 3.0
                        self.state_manager.change_state(COUNTDOWN)
            
            # Handle Menu Events
            if self.state_manager.is_state(MENU):
                if self.hud.handle_menu_event(event):
                    self.reset_game()
                    self.countdown_timer = 3.0
                    self.state_manager.change_state(COUNTDOWN)

    def check_collisions(self):
        crosshair_rect = self.crosshair_surf.get_rect(center=(self.player.pos.x, self.player.pos.y))
        hit_something = False
        
        # Check against active ducks
        for duck in self.spawner.active_ducks:
            if duck.alive and not duck.hit and crosshair_rect.colliderect(duck.rect):
                duck.die()
                self.score_manager.register_hit(duck.type, duck.spawn_time)
                hit_something = True
                break # Only hit one duck per shot
        
        # Check against pebbles (hazards)
        if not hit_something:
            for pebble in self.pebble_manager.active_pebbles:
                if pebble.alive and crosshair_rect.colliderect(pebble.rect):
                    pebble.hit = True
                    self.score_manager.register_penalty()
                    hit_something = True
                    break
        
        if not hit_something:
            # Optionally track shots for accuracy
            pass

    def update(self, dt):
        # Clouds drift in every state (menu, playing, game-over)
        self.cloud_manager.update(dt)
        if self.score_manager.round == 3:
            self.leaf_manager.update(dt)
        elif self.score_manager.round == 4:
            self.snow_manager.update(dt)
        elif self.score_manager.round == 5:
            self.rain_manager.update(dt)
            # Lightning logic
            self.lightning_alpha = max(0.0, self.lightning_alpha - 500.0 * dt)
            self.lightning_timer -= dt
            if self.lightning_timer <= 0:
                self.lightning_alpha = 180.0 # Flash!
                self.lightning_timer = random.uniform(4.0, 10.0)
        self.score_manager.update(dt)

        if self.state_manager.is_state(COUNTDOWN):
            pygame.mouse.set_visible(False)
            self.countdown_timer -= dt
            if self.countdown_timer <= 0:
                self.state_manager.change_state(PLAYING)

        if self.state_manager.is_state(MENU):
            pygame.mouse.set_visible(True)
        
        if self.state_manager.is_state(GAME_OVER):
            pygame.mouse.set_visible(True)

        if self.state_manager.is_state(PLAYING):
            pygame.mouse.set_visible(False)
            self.player.update(dt)

            # Apply dynamic difficulty modifiers
            mods = self.score_manager.get_difficulty_modifier()
            current_speed_mult = self.score_manager.speed_mult * mods["speed"]
            current_max_ducks = self.score_manager.max_ducks_on_screen + mods["density_bonus"]

            misses = self.spawner.update(dt, current_speed_mult, current_max_ducks, self.duck_surfaces, mods["spawn_rate"])
            self.pebble_manager.update(dt, self.score_manager.round)

            for _ in range(misses):
                self.score_manager.register_miss()

            # Game over condition (Dynamic miss limit)
            if self.score_manager.misses >= self.score_manager.get_max_misses():
                self.score_manager.save_to_leaderboard(self.hud.kfid, self.hud.player_name)
                self.state_manager.change_state(GAME_OVER)
            
            # Day/Night Toggle on Round Change
            if self.score_manager.round != self.last_round:
                # Keep track of what we're coming FROM
                self.prev_sky, self.prev_ground = self.get_background_surfaces(self.last_round, self.is_day)
                
                self.is_day = not self.is_day
                self.last_round = self.score_manager.round
                self.bg_transition_alpha = 255.0 # Start full fade overlay
        
        # Update transition fading
        if self.bg_transition_alpha > 0:
            self.bg_transition_alpha = max(0.0, self.bg_transition_alpha - self.transition_speed * dt)

    def get_background_surfaces(self, round_num, is_day):
        """Helper to get sky/ground surfaces for a specific state."""
        if round_num == 3:
            return self.autumn_sky, self.autumn_ground
        elif round_num == 4:
            return self.winter_sky, self.winter_ground
        elif round_num == 5:
            return self.monsoon_sky, self.monsoon_ground
        elif is_day:
            return self.day_sky, self.day_ground
        else:
            return self.night_sky, self.night_ground

    def draw(self):
        # 1. Background Selection (Current destination)
        target_sky, target_ground = self.get_background_surfaces(self.score_manager.round, self.is_day)
        
        # Draw Target (Base)
        self.screen.blit(target_sky, (0, 0))
        
        # 2. Draw Transition Overlay (Fade out from previous)
        if self.bg_transition_alpha > 0:
            temp_sky = self.prev_sky.copy()
            temp_sky.set_alpha(int(self.bg_transition_alpha))
            self.screen.blit(temp_sky, (0, 0))
        
        # Spawner / Duck layer (Only if playing or countdown)
        if self.state_manager.is_state(PLAYING) or self.state_manager.is_state(COUNTDOWN):
            self.spawner.draw(self.screen)
        
        # Floating clouds layer
        self.cloud_manager.draw(self.screen)
        
        # Autumn Leaves (Round 3 only)
        if self.score_manager.round == 3:
            self.leaf_manager.draw(self.screen)
            
        # Winter Snow (Round 4 only)
        if self.score_manager.round == 4:
            self.snow_manager.draw(self.screen)
            
        # Monsoon Rain (Round 5 only)
        if self.score_manager.round == 5:
            self.rain_manager.draw(self.screen)
            # Draw lightning flash overlay
            if self.lightning_alpha > 0:
                flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                flash_surf.fill((255, 255, 255))
                flash_surf.set_alpha(int(self.lightning_alpha))
                self.screen.blit(flash_surf, (0, 0))
            
        # Draw Pebbles
        self.pebble_manager.draw(self.screen)
        
        # Determine Ground to draw
        ground_to_draw = target_ground
        if self.bg_transition_alpha > 0:
            # Blend current and previous ground
            ground_to_draw = target_ground.copy()
            temp_ground = self.prev_ground.copy()
            temp_ground.set_alpha(int(self.bg_transition_alpha))
            ground_to_draw.blit(temp_ground, (0, 0))

        if self.state_manager.is_state(PLAYING):
            self.screen.blit(ground_to_draw, (0, SCREEN_HEIGHT - 180))
            self.hud.draw(self.screen, self.score_manager, self.player)
            self.player.draw(self.screen, self.crosshair_surf)
        
        elif self.state_manager.is_state(COUNTDOWN):
            self.screen.blit(ground_to_draw, (0, SCREEN_HEIGHT - 180))
            self.hud.draw(self.screen, self.score_manager, self.player)
            self.hud.draw_countdown(self.screen, self.countdown_timer)
            self.player.draw(self.screen, self.crosshair_surf)
        
        elif self.state_manager.is_state(MENU):
            self.screen.blit(ground_to_draw, (0, SCREEN_HEIGHT - 180))
            self.hud.draw_menu(self.screen)
            self.player.draw(self.screen, self.crosshair_surf)
            
        elif self.state_manager.is_state(GAME_OVER):
            self.screen.blit(ground_to_draw, (0, SCREEN_HEIGHT - 180))
            self.hud.draw_game_over(self.screen, self.score_manager)
            self.player.draw(self.screen, self.crosshair_surf)

        pygame.display.flip()

    def reset_game(self):
        self.score_manager.reset()
        self.spawner.active_ducks = []
        self.pebble_manager.reset()
        self.player = Player()
        self.last_round = 1
        self.is_day = True
        self.bg_transition_alpha = 0

if __name__ == "__main__":
    game = DuckHuntGame()
    game.run()
