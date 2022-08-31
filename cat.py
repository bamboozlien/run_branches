import pygame
from pygame.sprite import Sprite


class Cat(Sprite):
    """A class to manage the cat."""
    def __init__(self, ai_game):
        """Initialize the cat and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the cat image and get its rect.
        self.image = pygame.image.load('images/branches.bmp')
        self.rect = self.image.get_rect()

        # Start each new cat at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal values for the cat's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the cat's position based on movement flags."""
        # Update the cat's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.cat_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.cat_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the cat at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_cat(self):
        """Center the cat on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)