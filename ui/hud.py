import pygame
import time
import requests
import pyperclip
from config import *

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 24, bold=True)
        # Load and scale Logo - try multiple paths
        self.logo = None
        logo_paths = [
            "assets/kiitfest-main-logo (1).png",         # Run from Pygame/
            "Pygame/assets/kiitfest-main-logo (1).png",  # Run from root
        ]
        for path in logo_paths:
            try:
                full_logo = pygame.image.load(path).convert_alpha()
                # Use original size but cap at reasonable screen height (e.g., 80px)
                # and maintain aspect ratio
                max_h = 80
                if full_logo.get_height() > max_h:
                    aspect = full_logo.get_width() / full_logo.get_height()
                    self.logo = pygame.transform.smoothscale(full_logo, (int(max_h * aspect), max_h))
                else:
                    self.logo = full_logo
                print(f"Logo loaded from: {path}")
                break
            except Exception:
                continue
        if not self.logo:
            print("Warning: KIITfest logo not found.")
        
        # Menu State
        self.kfid = ""
        self.player_name = ""
        self.kfid_active = False
        self.validation_status = "" # "", "validating", "success", "error"
        self.error_msg = ""
        self.kfid_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350, 300, 50)
        self.start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 450, 300, 60)
        
        # Game Over / Leaderboard State
        self.show_leaderboard = False
        self.leaderboard_data = [] # List of MongoDB entries
        self.leaderboard_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 680, 300, 50)
        self.restart_hint_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 600, 300, 50) # Rect for the click prompt
        
        # Load Menu Background if exists
        self.menu_bg = None
        bg_paths = [
            "assets/menu_bg.png",
            "Pygame/assets/menu_bg.png"
        ]
        for path in bg_paths:
            try:
                self.menu_bg = pygame.image.load(path).convert()
                self.menu_bg = pygame.transform.smoothscale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"Menu background loaded from: {path}")
                break
            except Exception:
                continue

    def validate_kfid(self):
        """Calls the API to validate the entered KFID and get player name."""
        if not self.kfid.strip():
            self.error_msg = "PLEASE ENTER KFID"
            self.validation_status = "error"
            return False

        self.validation_status = "validating"
        self.error_msg = ""
        
        try:
            payload = {"kfid": self.kfid.strip()}
            response = requests.post(VALIDATE_API_URL, json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    self.player_name = data.get("name", "Unknown Player")
                    self.validation_status = "success"
                    return True
                else:
                    self.error_msg = result.get("message", "INVALID KFID")
                    self.validation_status = "error"
            else:
                self.error_msg = "SERVER ERROR"
                self.validation_status = "error"
        except Exception as e:
            print(f"Validation error: {e}")
            self.error_msg = "CONNECTION FAILED"
            self.validation_status = "error"
            
        return False

    def draw(self, screen, score_manager, player):
        # 1. Draw Logo (Center Top)
        # Default starting Y for things below the logo
        round_y = 20
        
        if self.logo:
            logo_rect = self.logo.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
            screen.blit(self.logo, logo_rect)
            round_y = logo_rect.bottom + 10
        else:
            round_y = 50

            
        # 2. Draw Round (Below Logo)
        round_text = self.font.render(f"ROUND: {score_manager.round}", True, WHITE)
        screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, round_y))

        # 3. Draw Score
        score_text = self.font.render(f"SCORE: {score_manager.score:06}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # 4. Draw Bullets
        bullet_str = "|" * player.bullets
        if player.reloading:
            bullet_str = "RELOADING..."
        bullet_text = self.font.render(f"SHOTS: {bullet_str}", True, WHITE)
        screen.blit(bullet_text, (20, SCREEN_HEIGHT - 50))
        
        # 5. Draw Hits/Misses (Dynamic Limit)
        stats_text = self.font.render(f"HIT: {score_manager.hits}  MISS: {score_manager.misses}/{score_manager.get_max_misses()}", True, WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH - stats_text.get_width() - 20, 20))
        
        # Draw Combo & Multiplier
        if score_manager.combo > 1:
            combo_text = self.font.render(f"COMBO: {score_manager.combo}", True, BLACK)
            screen.blit(combo_text, (20, 60))
            
            multi_text = self.font.render(f"x{score_manager.multiplier:.1f}", True, BLACK)
            screen.blit(multi_text, (20, 90))
            
        # Draw Floating Penalties — bright red, larger font, right below the score
        penalty_font = pygame.font.SysFont("monospace", 32, bold=True)
        for ft in score_manager.floating_texts:
            text_surf = penalty_font.render(ft["text"], True, (255, 0, 0))  # Bright Red
            text_surf.set_alpha(int(min(255, ft["alpha"])))
            screen.blit(text_surf, (ft["pos"][0], ft["pos"][1]))

    def draw_countdown(self, screen, timer):
        # Calculate number and alpha
        import math
        number = math.ceil(timer)
        if number < 1: number = 1
        
        # Smooth fade out transition
        # At start of second (e.g. 1.0), alpha is 255. At end (0.0), alpha is 0.
        fade_progress = timer - math.floor(timer)
        if fade_progress == 0 and timer > 0: fade_progress = 1.0
        alpha = int(fade_progress * 255)
        
        # Use a large font
        count_font = pygame.font.SysFont("monospace", 150, bold=True)
        text_surf = count_font.render(str(number), True, RED)
        
        # Create a surface with alpha support
        fade_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        fade_surf.fill((200, 0, 0, alpha)) # Use RED components (200, 0, 0) for the alpha overlay
        text_surf.blit(fade_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, 
                                SCREEN_HEIGHT // 2 - text_surf.get_height() // 2))

    def draw_menu(self, screen):
        # 0. Draw Background Image or Overlay
        if self.menu_bg:
            screen.blit(self.menu_bg, (0, 0))
            # Optional subtle overlay to ensure text readability
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100)) # Lighter overlay if there's a background
            screen.blit(overlay, (0, 0))
        else:
            # Semi-transparent dark overlay (fallback)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 10, 15, 230)) # Very dark blue-ish
            screen.blit(overlay, (0, 0))
        
        # 1. Draw Logo (Prominent)
        if self.logo:
            # Scale logo larger for menu
            large_logo = pygame.transform.smoothscale(self.logo, (int(self.logo.get_width() * 2), int(self.logo.get_height() * 2)))
            logo_rect = large_logo.get_rect(midtop=(SCREEN_WIDTH // 2, 50))
            screen.blit(large_logo, logo_rect)
        
        # 2. Draw Title
        title_font = pygame.font.SysFont("Impact", 84) if "Impact" in pygame.font.get_fonts() else pygame.font.SysFont("monospace", 84, bold=True)
        title_surf = title_font.render("SHOOT THE DUCK", True, GOLD)
        
        # Add a subtle shadow to title
        shadow_surf = title_font.render("SHOOT THE DUCK", True, (50, 50, 0))
        screen.blit(shadow_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + 4, 184))
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 180))
        
        # 3. KFID Label and Input Box
        label_font = pygame.font.SysFont("monospace", 24, bold=True)
        label_surf = label_font.render("ENTER KFID:", True, WHITE)
        screen.blit(label_surf, (self.kfid_rect.x, self.kfid_rect.y - 35))
        
        # Validation Status/Error Message
        status_font = pygame.font.SysFont("monospace", 18, bold=True)
        if self.validation_status == "validating":
            status_surf = status_font.render("VALIDATING...", True, GOLD)
            screen.blit(status_surf, (self.kfid_rect.x, self.kfid_rect.bottom + 5))
        elif self.validation_status == "error":
            status_surf = status_font.render(self.error_msg, True, RED)
            screen.blit(status_surf, (self.kfid_rect.x, self.kfid_rect.bottom + 5))
        elif self.validation_status == "success":
            status_surf = status_font.render(f"WELCOME, {self.player_name}", True, GREEN)
            screen.blit(status_surf, (self.kfid_rect.x, self.kfid_rect.bottom + 5))

        # Input Box
        box_color = PEBBLE_HIGHLIGHT if self.kfid_active else DARK_GRAY
        pygame.draw.rect(screen, box_color, self.kfid_rect, border_radius=10)
        pygame.draw.rect(screen, GOLD if self.kfid_active else WHITE, self.kfid_rect, 2, border_radius=10)
        
        # KFID Text
        text_surf = self.font.render(self.kfid + ("|" if (time.time() % 1 > 0.5 and self.kfid_active) else ""), True, WHITE)
        screen.blit(text_surf, (self.kfid_rect.x + 15, self.kfid_rect.y + 10))
        
        # 4. Start Button
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.start_button_rect.collidepoint(mouse_pos)
        btn_color = BUTTON_HOVER if is_hover else BUTTON_COLOR
        
        # Button Shadow
        pygame.draw.rect(screen, (50, 0, 0), (self.start_button_rect.x + 4, self.start_button_rect.y + 4, 300, 60), border_radius=15)
        # Button Body
        pygame.draw.rect(screen, btn_color, self.start_button_rect, border_radius=15)
        # Button Border
        pygame.draw.rect(screen, WHITE, self.start_button_rect, 2, border_radius=15)
        
        # Button Text
        btn_font = pygame.font.SysFont("Impact", 36) if "Impact" in pygame.font.get_fonts() else pygame.font.SysFont("monospace", 36, bold=True)
        btn_text = btn_font.render("START GAME", True, WHITE)
        screen.blit(btn_text, (self.start_button_rect.centerx - btn_text.get_width() // 2, 
                               self.start_button_rect.centery - btn_text.get_height() // 2))

    def handle_menu_event(self, event):
        """Returns True if 'START GAME' was clicked and KFID is validated."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.kfid_rect.collidepoint(event.pos):
                self.kfid_active = True
                self.validation_status = "" # Reset status on click
            else:
                self.kfid_active = False
                
            if self.start_button_rect.collidepoint(event.pos):
                if self.validate_kfid():
                    return True
        
        if event.type == pygame.KEYDOWN and self.kfid_active:
            # Handle Ctrl+V (Paste)
            if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                try:
                    pasted_text = pyperclip.paste().strip()
                    # Limit combined length
                    allowed_len = 15 - len(self.kfid)
                    if allowed_len > 0:
                        self.kfid += pasted_text[:allowed_len]
                        self.validation_status = "" # Reset on paste
                except Exception as e:
                    print(f"Paste error: {e}")
            elif event.key == pygame.K_BACKSPACE:
                self.kfid = self.kfid[:-1]
                self.validation_status = "" # Reset on backspace
            elif event.key == pygame.K_RETURN:
                if self.validate_kfid():
                    return True
            else:
                # Limit KFID length
                if len(self.kfid) < 15 and event.unicode.isprintable():
                    self.kfid += event.unicode
                    self.validation_status = "" # Reset on type
        
        return False

    def draw_game_over(self, screen, score_manager):
        # 1. Background Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((150, 0, 0, 200)) # Darker red for Game Over
        screen.blit(overlay, (0, 0))
        
        if self.show_leaderboard:
            self._draw_leaderboard_table(screen)
            # Re-draw the button as "CLOSE" or just let them click it
            self._draw_button(screen, self.leaderboard_btn_rect, "BACK TO STATS", GOLD)
            return

        # Title
        title_font = pygame.font.SysFont("Impact", 84) if "Impact" in pygame.font.get_fonts() else pygame.font.SysFont("monospace", 84, bold=True)
        title = title_font.render("GAME OVER", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        # Stats Font
        stat_font = pygame.font.SysFont("monospace", 36, bold=True)
        
        accuracy = 0
        if score_manager.shots_fired > 0:
            accuracy = (score_manager.hits / score_manager.shots_fired) * 100
            
        stats = [
            f"FINAL SCORE: {score_manager.score}",
            f"ROUND REACHED: {score_manager.round}",
            f"TOTAL HITS: {score_manager.hits}",
            f"ACCURACY: {accuracy:.1f}%"
        ]
        
        start_y = 220
        for i, stat_text in enumerate(stats):
            color = GOLD if i == 0 else WHITE
            text_surf = stat_font.render(stat_text, True, color)
            screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, start_y + (i * 60)))
        
        # 2. Restart Prompt (Centerish)
        prompt_font = pygame.font.SysFont("monospace", 28, bold=True)
        prompt = prompt_font.render("CLICK ANYWHERE OR PRESS ENTER TO RESTART", True, WHITE)
        if (time.time() % 1.0 > 0.5): # Blinking effect
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 580))
            
        # 3. Leaderboard Button
        self._draw_button(screen, self.leaderboard_btn_rect, "TOP 10 LEADERBOARD")

    def _draw_button(self, screen, rect, text, color=BUTTON_COLOR):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        btn_color = BUTTON_HOVER if is_hover else color
        
        # Shadow
        pygame.draw.rect(screen, (40, 0, 0), (rect.x + 4, rect.y + 4, rect.width, rect.height), border_radius=10)
        # Body
        pygame.draw.rect(screen, btn_color, rect, border_radius=10)
        # Border
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        
        btn_font = pygame.font.SysFont("monospace", 20, bold=True)
        text_surf = btn_font.render(text, True, WHITE)
        screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2, 
                               rect.centery - text_surf.get_height() // 2))

    def _draw_leaderboard_table(self, screen):
        # Table Background
        table_w, table_h = 800, 600
        table_rect = pygame.Rect(SCREEN_WIDTH // 2 - table_w // 2, 50, table_w, table_h)
        pygame.draw.rect(screen, (30, 30, 35), table_rect, border_radius=20)
        pygame.draw.rect(screen, GOLD, table_rect, 3, border_radius=20)
        
        title_font = pygame.font.SysFont("Impact", 48) if "Impact" in pygame.font.get_fonts() else pygame.font.SysFont("monospace", 48, bold=True)
        title_surf = title_font.render("GLOBAL TOP 10", True, GOLD)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, table_rect.y + 20))
        
        header_font = pygame.font.SysFont("monospace", 24, bold=True)
        headers = ["RANK", "NAME", "SCORE", "ACC%"]
        col_x = [table_rect.x + 50, table_rect.x + 150, table_rect.x + 450, table_rect.x + 650]
        
        for i, header in enumerate(headers):
            h_surf = header_font.render(header, True, WHITE)
            screen.blit(h_surf, (col_x[i], table_rect.y + 100))
            
        pygame.draw.line(screen, DARK_GRAY, (table_rect.x + 30, table_rect.y + 135), (table_rect.right - 30, table_rect.y + 135), 2)
        
        row_font = pygame.font.SysFont("monospace", 22, bold=True)
        for i, entry in enumerate(self.leaderboard_data):
            row_y = table_rect.y + 150 + (i * 40)
            color = GREEN if i == 0 else (GOLD if i < 3 else WHITE) # Winner green, Top 3 Gold, others white
            
            # Rank
            r_surf = row_font.render(f"#{i+1}", True, color)
            screen.blit(r_surf, (col_x[0], row_y))
            
            # Name (Truncate if needed)
            name = entry.get("name", "Unknown")
            if len(name) > 15: name = name[:13] + ".."
            n_surf = row_font.render(name, True, color)
            screen.blit(n_surf, (col_x[1], row_y))
            
            # Score
            s_surf = row_font.render(f"{entry.get('score', 0):,}", True, color)
            screen.blit(s_surf, (col_x[2], row_y))
            
            # Accuracy
            a_surf = row_font.render(f"{entry.get('accuracy', 0)}%", True, color)
            screen.blit(a_surf, (col_x[3], row_y))

    def handle_game_over_event(self, event, score_manager):
        """Processes clicks on the game over screen, returns True if game should restart."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.leaderboard_btn_rect.collidepoint(event.pos):
                if not self.show_leaderboard:
                    # Fetch data only when opening
                    self.leaderboard_data = score_manager.get_top_scores()
                    self.show_leaderboard = True
                else:
                    self.show_leaderboard = False
                return False
            
            if not self.show_leaderboard:
                # If leaderboard is NOT showing, any other click restarts
                self.show_leaderboard = False
                return True
                
        if event.type == pygame.KEYDOWN and not self.show_leaderboard:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return True
                
        return False
