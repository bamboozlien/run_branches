class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (239, 201, 201)

        # Cat settings
        self.cat_limit = 3

        # Bullet settings
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Vacuum cleaner settings
        self.fleet_drop_speed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the cleaner point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.cat_speed = 1.5
        self.bullet_speed = 1.5
        self.vacuum_speed = 0.7

        # fleet_direction of 1 represents right; -1 - left.
        self.fleet_direction = 1

        # Scoring
        self.vacuum_points = 50

    def increase_speed(self):
        """Increase speed settings and vacuum point values."""
        self.cat_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.vacuum_speed *= self.speedup_scale

        self.vacuum_points = int(self.vacuum_points * self.score_scale)
