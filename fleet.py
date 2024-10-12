import pygame as pg
from vector import Vector
from alien import Alien
from time import sleep
from pygame.sprite import Sprite
from sound import Sound

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()  # Group to hold the alien sprites
        self.fleet_lasers = pg.sprite.Group()  # Group for fleet's lasers
        self.sound = Sound()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        self.spacing = 1.4

        self.total_aliens = 0  # Track total number of aliens created

        self.create_fleet()

    def reset_fleet(self):
        """Clear the existing fleet and create a new one."""
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        """Create a fleet of aliens by adding rows of aliens."""
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        current_y = alien_height

        # Create rows of aliens
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            self.create_row(current_y)
            current_y += self.spacing * alien_height

    def create_row(self, y):
        """Create a row of aliens and add them to the fleet."""
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        current_x = alien_width

        # Add aliens in a row
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
            new_alien = Alien(self.ai_game, v=self.v)
            new_alien.rect.y = y
            new_alien.y = y
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += self.spacing * alien_width

            # Increment total aliens created
            self.total_aliens += 1

    def check_edges(self):
        """Return True if any alien reaches the edge of the screen."""
        for alien in self.aliens:
            if alien.check_edges(): 
                return True
        return False

    def check_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False

    def update(self): 
        """Update the position of the fleet and check for collisions."""
        # Check for collisions between ship lasers and aliens
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    # If all aliens are destroyed and the ship wasn't hit, level up #need to check cond here 
        if not self.aliens:
            self.ship.lasers.empty()
            self.create_fleet()
            self.stats.level += 1  # Increase level
            self.sb.prep_level()
            return

        # Check for collisions between ship and aliens
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!")
            self.ship.ship_hit()
            return

        # Check if any alien has reached the bottom of the screen
        if self.check_bottom():
            return

        # Reverse fleet direction if an alien reaches the edge of the screen
        if self.check_edges():
            self.v.x *= -1
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed

        # Update the position of each alien
        for alien in self.aliens:
            alien.update()

    def draw(self): 
        """Draw all aliens in the fleet."""
        for alien in self.aliens:
            alien.draw()

def main():
    print('\nRun from alien_invasions.py\n')

if __name__ == "__main__":
    main()
