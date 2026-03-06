import time
import pymongo
from datetime import datetime
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
        self.ducks_to_next_round = 9 # Increased from 6 for longer rounds
        self.total_time = 0.0  # Seconds since game start
        
        # Miss-based scaling
        self.miss_speed_mult = 1.0
        self.miss_density_bonus = 0
        
        # Penalties & Visual Effects
        self.floating_texts = [] # List of {"text": str, "pos": [x,y], "alpha": float, "life": float}

    def get_max_misses(self):
        """Returns the game over miss threshold."""
        return MAX_MISSES_ALLOWED

    def update(self, dt):
        """Update total time for continuous scaling."""
        self.total_time += dt
        
        # Update floating texts
        for ft in self.floating_texts[:]:
            ft["life"] -= dt
            ft["alpha"] = max(0, ft["life"] * 255) # Fade out over 1s
            ft["pos"][1] += 20 * dt # Slowly drop down
            if ft["life"] <= 0:
                self.floating_texts.remove(ft)

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
        """Handle duck escape and combo reset with difficulty penalty."""
        self.misses += 1
        self.combo = 0
        
        # Apply difficulty penalty on miss
        self.miss_speed_mult *= SPEED_INCREMENT_PER_MISS
        self.miss_density_bonus = int(self.misses * DENSITY_INCREMENT_PER_MISS)
        
        self.update_multiplier()
        self.check_round_progression()

    def register_penalty(self):
        """Decrease score and add floating visual penalty near the score UI."""
        self.score = max(0, self.score - PEBBLE_PENALTY)
        # Position near the score (which is at 20, 20)
        self.floating_texts.append({
            "text": f"-{PEBBLE_PENALTY}",
            "pos": [20, 50], # Just below "SCORE: 000000" (score drawn at y=20, ~28px tall → bottom ~48)
            "alpha": 255.0,
            "life": 1.8 # Duration in seconds
        })
        print(f"Penalty! -{PEBBLE_PENALTY} | Score: {self.score}")

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
        
        # 1. Update Speed: dampened growth in later rounds
        if self.round >= SPEED_DAMPENING_START_ROUND:
            # Apply dampening to current speed mult then add increment
            self.speed_mult *= SPEED_DAMPENING_FACTOR
            self.speed_mult *= (1.0 + (DUCK_SPEED_INCREMENT - 1.0) * 0.5) # Reduced growth
        else:
            self.speed_mult *= DUCK_SPEED_INCREMENT
            
        # 2. Update Density: Aggressive growth from Round 3 onwards
        self.ducks_to_next_round += 3 # Increased from 2
        if self.round <= 3:
            # Low density for early game (Rounds 1-3)
            self.max_ducks_on_screen = 2
        elif self.round >= 4:
            # Fixed density for late game rounds to maintain playability
            self.max_ducks_on_screen = 3
        
        self.reset_round_stats()

    def reset_round_stats(self):
        """Reset temporary stats for the new round."""
        self.hits = 0
        self.misses = 0
        self.shots_fired = 0

    def get_difficulty_modifier(self):
        """
        Returns a dict of modifiers based on misses and elapsed time.
        """
        modifiers = {"spawn_rate": 1.0, "speed": 1.0}
        
        # 1. Continuous Time-Based Speed (Very slow 0.1% every 10s)
        time_speed_mult = 1.0 + (self.total_time / 1000)
        
        # 2. Combine with round-based speed (self.speed_mult) and miss-based penalty
        modifiers["speed"] = self.speed_mult * time_speed_mult * self.miss_speed_mult
        
        # Enforce strict bird limit for late game rounds as requested
        if self.round >= 4:
            modifiers["density_bonus"] = 0
        else:
            modifiers["density_bonus"] = self.miss_density_bonus
        
        # 3. Round-Specific Spikes (Milestone difficulty for Round 4/5)
        spike_mult = 1.0
        if self.round == 4:
            spike_mult = 1.00 # Reduced from 1.05 to 1.00 as requested
        elif self.round >= 5:
            spike_mult = 1.05 # Reduced from 1.20 to 1.05 as requested
            
        modifiers["speed"] *= spike_mult
        
        # 4. Dynamic Spawn Rate matching density
        # Significantly faster spawns from Round 4 onwards
        spawn_reduction = 0.15 * (self.round - 1)
        if self.round == 3:
            spawn_reduction += 0.05 # Mild spike for Round 3
        elif self.round >= 4:
            spawn_reduction += 0.15 # Reduced spike for Round 4 (from 0.35)
        
        modifiers["spawn_rate"] = max(0.3, 1.0 - spawn_reduction)
            
        return modifiers

    def save_to_leaderboard(self, kfid, name):
        """Saves final score and accuracy to local MongoDB if it's a new high score."""
        if not kfid:
            print("Leaderboard: Skipping save, no KFID.")
            return

        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]
            
            # Calculate final accuracy
            accuracy = 0
            if self.shots_fired > 0:
                accuracy = round((self.hits / self.shots_fired) * 100, 1)
                
            entry = {
                "kfid": kfid,
                "name": name,
                "score": self.score,
                "accuracy": accuracy,
                "round": self.round,
                "timestamp": datetime.now()
            }

            # Check for existing record
            existing = collection.find_one({"kfid": kfid})
            if existing:
                if self.score > existing.get("score", 0):
                    collection.update_one({"kfid": kfid}, {"$set": entry})
                    print(f"Leaderboard: New High Score! Updated {name} ({kfid}) to {self.score}")
                else:
                    print(f"Leaderboard: Score {self.score} not higher than existing {existing.get('score')}. Skipping update.")
            else:
                collection.insert_one(entry)
                print(f"Leaderboard: First entry for {name} ({kfid}) saved with score {self.score}")
            
            client.close()
        except Exception as e:
            print(f"Leaderboard: Failed to save to MongoDB: {e}")

    def get_top_scores(self):
        """Fetches top 10 scores from local MongoDB."""
        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]
            
            top_scores = list(collection.find().sort("score", -1).limit(10))
            client.close()
            return top_scores
        except Exception as e:
            print(f"Leaderboard: Failed to fetch from MongoDB: {e}")
            return []

    def reset(self):
        self.__init__()
