import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from cat import Cat
from vacuum import Vacuum
from bullet import Bullet


class RunBranches:
    """Overall class to manage game assets and behaviour."""
    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.cat = Cat(self)
        self.vacuums = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.cat.update()
                self._update_bullets()
                self._update_vacuums()

            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_cats()

        # Get rid of any remaining cleaners and bullets.
        self.vacuums.empty()
        self.bullets.empty()

        # Create a new fleet and center the cat.
        self._create_fleet()
        self.cat.center_cat()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self._fire_bullet()
        elif event.key == pygame.K_SPACE:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.cat.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_vacuum_collisions()

    def _check_bullet_vacuum_collisions(self):
        """Respond to bullet-cleaner collisions."""
        # Remove any bullets and cleaners that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.vacuums, True, True)

        if collisions:
            for vacuums in collisions.values():
                self.stats.score += self.settings.vacuum_points * len(vacuums)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.vacuums:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_vacuums(self):
        """
        Check if the fleet is at edge,
        then update the positions of all cleaners in the fleet.
        """
        self._check_fleet_edges()
        self.vacuums.update()

        # Look for cleaner-cat collisions.
        if pygame.sprite.spritecollideany(self.cat, self.vacuums):
            self._cat_hit()

        # Look for cleaners hitting the bottom of the screen.
        self._check_vacuums_bottom()

    def _create_fleet(self):
        """Create the fleet of vacuum cleaners."""
        # Create a cleaner and find the number of cleaners in a row.
        # Spacing between each cleaner is equal to one cleaner width.
        vacuum = Vacuum(self)
        vacuum_width, vacuum_height = vacuum.rect.size
        available_space_x = self.settings.screen_width - (2 * vacuum_width)
        number_vacuums_x = available_space_x // (2 * vacuum_width)

        # Determine the number of rows of cleaners that fit on the screen.
        cat_height = self.cat.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * vacuum_height) - cat_height)
        number_rows = available_space_y // (2 * vacuum_height)

        # Create the full fleet of vacuum cleaners.
        for row_number in range(number_rows):
            for vacuum_number in range(number_vacuums_x):
                self._create_vacuum(vacuum_number, row_number)

    def _create_vacuum(self, vacuum_number, row_number):
        """Create a cleaner and place it in the row."""
        vacuum = Vacuum(self)
        vacuum_width, vacuum_height = vacuum.rect.size
        vacuum.x = vacuum_width + 2 * vacuum_width * vacuum_number
        vacuum.rect.x = vacuum.x
        vacuum.rect.y = vacuum.rect.height + 2 * vacuum.rect.height * row_number
        self.vacuums.add(vacuum)

    def _check_fleet_edges(self):
        """Respond appropriately if any cleaners have reached an edge."""
        for vacuum in self.vacuums.sprites():
            if vacuum.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for vacuum in self.vacuums.sprites():
            vacuum.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _cat_hit(self):
        """Respond to the cat being hit by a cleaner."""
        if self.stats.cats_left > 0:
            # Decrement cats_left and update scoreboard.
            self.stats.cats_left -= 1
            self.sb.prep_cats()

            # Get rid of any remaining cleaners and bullets.
            self.vacuums.empty()
            self.bullets.empty()

            # Create a new fleet and center the cat.
            self._create_fleet()
            self.cat.center_cat()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_vacuums_bottom(self):
        """Check if any cleaners have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for vacuum in self.vacuums.sprites():
            if vacuum.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the cat got hit.
                self._cat_hit()
                break

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.cat.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.vacuums.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = RunBranches()
    ai.run_game()