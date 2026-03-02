import pygame
import sys
import time
from config import *
from systems.state_manager import StateManager
from systems.spawner import Spawner
from systems.score_manager import ScoreManager
from entities.player import Player
from ui.hud import HUD
from assets_util import create_duck_surface, create_crosshair_surface, create_background

class DuckHuntGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Duck Hunt - Production Quality")
        self.clock = pygame.time.Clock()
        
        # Core Systems
        self.state_manager = StateManager()
        self.spawner = Spawner()
        self.score_manager = ScoreManager()
        self.player = Player()
        self.hud = HUD()
        
        # Assets
        self.duck_surf = create_duck_surface()
        self.crosshair_surf = create_crosshair_surface()
        self.sky_surf, self.ground_surf = create_background()
        
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
                elif self.state_manager.is_state(MENU) or self.state_manager.is_state(GAME_OVER):
                    self.reset_game()
                    self.state_manager.change_state(PLAYING)

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
        
        if not hit_something:
            # Optionally track shots for accuracy
            pass

    def update(self, dt):
        if self.state_manager.is_state(PLAYING):
            self.player.update(dt)
            
            # Apply dynamic difficulty modifiers
            mods = self.score_manager.get_difficulty_modifier()
            current_speed_mult = self.score_manager.speed_mult * mods["speed"]
            
            misses = self.spawner.update(dt, current_speed_mult, self.score_manager.max_ducks_on_screen, mods["spawn_rate"])
            
            for _ in range(misses):
                self.score_manager.register_miss()
            
            # Game over condition?
            if self.score_manager.misses >= 5: # Example: 5 misses and game over
                self.state_manager.change_state(GAME_OVER)

    def draw(self):
        # Parallax Background
        self.screen.blit(self.sky_surf, (0, 0))
        
        if self.state_manager.is_state(PLAYING):
            self.spawner.draw(self.screen, self.duck_surf)
            self.screen.blit(self.ground_surf, (0, SCREEN_HEIGHT - 150))
            self.hud.draw(self.screen, self.score_manager, self.player)
            self.player.draw(self.screen, self.crosshair_surf)
        
        elif self.state_manager.is_state(MENU):
            self.screen.blit(self.ground_surf, (0, SCREEN_HEIGHT - 150))
            self.hud.draw_menu(self.screen)
            self.player.draw(self.screen, self.crosshair_surf)
            
        elif self.state_manager.is_state(GAME_OVER):
            self.screen.blit(self.ground_surf, (0, SCREEN_HEIGHT - 150))
            self.hud.draw_game_over(self.screen, self.score_manager)
            self.player.draw(self.screen, self.crosshair_surf)

        pygame.display.flip()

    def reset_game(self):
        self.score_manager.reset()
        self.spawner.active_ducks = []
        self.player = Player()

if __name__ == "__main__":
    game = DuckHuntGame()
    game.run()
