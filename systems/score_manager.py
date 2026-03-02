import time
from config import *

class ScoreManager:
    def __init__(self):
        # Persistent Stats
        self.score = 0
        self.round = 1
        self.total_spawned = 0
        
        # Combo & Multiplier
        self.combo = 0
        self.multiplier = 1.0
        
        # Round Stats
        self.hits = 0
        self.misses = 0
        self.shots_fired = 0
        
        # Difficulty state
        self.speed_mult = 1.0
        self.max_ducks_on_screen = 2
        self.ducks_to_next_round = 10

    def register_shot(self):
        """Track every bullet fired for accuracy calculation."""
        self.shots_fired += 1

    def register_hit(self, duck_type, spawn_time):
        """
        Process a duck hit with combo and reaction time bonuses.
        """
        self.hits += 1
        self.combo += 1
        self.update_multiplier()
        
        # 1. Base Points by Type
        base_points = DUCK_TYPES.get(duck_type, {}).get("base_score", 100)
        
        # 2. Reaction Time Bonus
        reaction_time = time.time() - spawn_time
        rt_bonus = max(0, REACTION_BONUS_MAX - (reaction_time * REACTION_BONUS_COEFF))
        
        # 3. Final Calculation
        shot_score = int((base_points * self.multiplier) + rt_bonus)
        self.score += shot_score
        
        print(f"Hit! {duck_type} | Combo: {self.combo} | Multi: {self.multiplier} | RT: {reaction_time:.2f}s | Score: +{shot_score}")
        
        self.check_round_progression()

    def register_miss(self):
        """Handle duck escape and combo reset."""
        self.misses += 1
        self.combo = 0
        self.update_multiplier()
        self.check_round_progression()

    def update_multiplier(self):
        """Update multiplier based on current combo streak."""
        for threshold, mult in COMBO_TIERS:
            if self.combo >= threshold:
                self.multiplier = mult
                break

    def check_round_progression(self):
        """Check if round is over and calculate bonuses."""
        if self.hits + self.misses >= self.ducks_to_next_round:
            # Round Finish Logic
            accuracy_bonus = self.calculate_accuracy_bonus()
            round_bonus = self.calculate_round_bonus()
            
            total_bonus = accuracy_bonus + round_bonus
            self.score += total_bonus
            
            print(f"Round Over! Accuracy Bonus: {accuracy_bonus} | Round Bonus: {round_bonus}")
            self.advance_round()

    def calculate_accuracy_bonus(self):
        """Calculate bonus based on hit/shot ratio."""
        if self.shots_fired == 0: return 0
        accuracy = self.hits / self.shots_fired
        
        for threshold, bonus in ACCURACY_TIERS:
            if accuracy >= threshold:
                return bonus
        return 0

    def calculate_round_bonus(self):
        """Perfect round bonus logic."""
        # Check if all ducks were hit and no misses
        if self.misses == 0 and self.hits >= self.ducks_to_next_round:
            return PERFECT_ROUND_BONUS
        return 0

    def advance_round(self):
        self.round += 1
        self.speed_mult *= DUCK_SPEED_INCREMENT
        self.ducks_to_next_round += 2
        self.max_ducks_on_screen = min(5, 2 + self.round // 3)
        self.reset_round_stats()

    def reset_round_stats(self):
        """Reset temporary stats for the new round."""
        self.hits = 0
        self.misses = 0
        self.shots_fired = 0

    def get_difficulty_modifier(self):
        """
        Returns a dict of modifiers based on current miss pressure.
        Miss Count Effects:
        1-2: Normal
        3: Faster Spawning
        4: Faster Ducks
        5: GAME OVER (handled by main)
        """
        modifiers = {"spawn_rate": 1.0, "speed": 1.0}
        
        if self.misses == 3:
            modifiers["spawn_rate"] = 1.5 # 50% faster
        elif self.misses == 4:
            modifiers["speed"] = 1.3 # 30% faster
            
        return modifiers

    def reset(self):
        self.__init__()
