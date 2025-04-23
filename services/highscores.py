import json
import os
from datetime import datetime
import services.config as config


class HighScoreManager:
    def __init__(self):
        self.high_scores_file = config.HIGH_SCORES_FILE
        self.max_scores = config.MAX_HIGH_SCORES

    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            return []

    def save_score(self, score, player_name):
        """Save a new high score and return the updated list"""
        try:
            high_scores = self.load_scores()

            # Add new score with player name
            new_score = {
                'score': score,
                'name': player_name,
                'date': datetime.now().strftime("%Y-%m-%d")
            }

            high_scores.append(new_score)

            # Sort by score in descending order
            high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)

            # Keep only top scores
            high_scores = high_scores[:self.max_scores]

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.high_scores_file), exist_ok=True)

            # Save to file
            with open(self.high_scores_file, 'w') as f:
                json.dump(high_scores, f)

            return high_scores
        except Exception as e:
            print(f"Error saving high score: {e}")
            return []

    def is_high_score(self, score):
        """Check if a score qualifies as a high score"""
        high_scores = self.load_scores()

        if len(high_scores) < self.max_scores:
            return True

        return score > high_scores[-1]['score']

    def get_rank(self, score):
        """Get the rank of a score in the high scores list"""
        high_scores = self.load_scores()

        for i, hs in enumerate(high_scores):
            if score > hs['score']:
                return i + 1

        if len(high_scores) < self.max_scores:
            return len(high_scores) + 1

        return None