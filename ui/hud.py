import pygame
from config import *

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 24, bold=True)

    def draw(self, screen, score_manager, player):
        # Draw Score
        score_text = self.font.render(f"SCORE: {score_manager.score:06}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Draw Round
        round_text = self.font.render(f"ROUND: {score_manager.round}", True, WHITE)
        screen.blit(round_text, (SCREEN_WIDTH // 2 - 50, 20))
        
        # Draw Bullets
        bullet_str = "|" * player.bullets
        if player.reloading:
            bullet_str = "RELOADING..."
        bullet_text = self.font.render(f"SHOTS: {bullet_str}", True, WHITE)
        screen.blit(bullet_text, (20, SCREEN_HEIGHT - 50))
        
        # Draw Hits/Misses
        stats_text = self.font.render(f"HIT: {score_manager.hits}  MISS: {score_manager.misses}", True, WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH - 300, 20))
        
        # Draw Combo & Multiplier
        if score_manager.combo > 1:
            combo_text = self.font.render(f"COMBO: {score_manager.combo}", True, GREEN)
            screen.blit(combo_text, (20, 60))
            
            multi_text = self.font.render(f"x{score_manager.multiplier:.1f}", True, GREEN)
            screen.blit(multi_text, (20, 90))

    def draw_menu(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_font = pygame.font.SysFont("monospace", 72, bold=True)
        title = title_font.render("DUCK HUNT", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        
        prompt = self.font.render("CLICK TO START", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 400))

    def draw_game_over(self, screen, score_manager):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((150, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Title
        title_font = pygame.font.SysFont("monospace", 72, bold=True)
        title = title_font.render("GAME OVER", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Stats Font
        stat_font = pygame.font.SysFont("monospace", 36, bold=True)
        
        # Calculate overall accuracy
        accuracy = 0
        if score_manager.shots_fired > 0:
            accuracy = (score_manager.hits / score_manager.shots_fired) * 100
            
        stats = [
            f"FINAL SCORE: {score_manager.score}",
            f"ROUND REACHED: {score_manager.round}",
            f"TOTAL HITS: {score_manager.hits}",
            f"TOTAL MISSES: {score_manager.misses}",
            f"ACCURACY: {accuracy:.1f}%"
        ]
        
        start_y = 250
        for i, stat_text in enumerate(stats):
            color = GREEN if i == 0 else WHITE
            text_surf = stat_font.render(stat_text, True, color)
            screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, start_y + (i * 50)))
        
        # Prompt
        prompt = self.font.render("CLICK TO RESTART", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 600))
