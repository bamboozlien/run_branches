import pygame
from pygame.sprite import Sprite


class Vacuum(Sprite):
    """A class to represent a single vacuum cleaner."""

    def __init__(self, ai_game):
        """Initialize the cleaner and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the cleaner image and get its rect.
        self.image = pygame.image.load('images/vacuum_1.bmp')
        self.rect = self.image.get_rect()

        # Start each new cleaner at the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the cleaner's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the cleaner right or left."""
        self.x += (self.settings.vacuum_speed *
        self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if cleaner is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
