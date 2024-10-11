import pygame as pg
from vector import Vector
from laser import Laser
from time import sleep
from pygame.sprite import Sprite
from timer import Timer  # Assuming you have a Timer class to manage frame animations

class Ship(Sprite):
    def __init__(self, ai_game, v=Vector()):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.sb = None

        # Load the ship image created using a pixel editor
        self.image = pg.image.load('images/ship.bmp')  # Replace with your pixel art ship image
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # Set position variables
        scr_r = self.screen_rect
        self.x = float(scr_r.midbottom[0])
        self.y = float(scr_r.height)
        self.v = v

        # Laser management
        self.lasers = pg.sprite.Group()
        self.firing = False
        self.fleet = None
        self.fired = 0

        # Explosion animation frames (8-12 frames)
        self.explosion_images = [pg.image.load(f'images_other/ship_boom{n}.png') for n in range(3)]  # Replace with your actual explosion frames
        self.explosion_timer = Timer(images=self.explosion_images, delta=100, loop_continuously=False)  # Timer to control animation

        # Flags to manage state
        self.dying = False  # Ship is hit but animation still running
        self.dead = False    # Ship is completely destroyed

    def set_fleet(self, fleet): 
        self.fleet = fleet

    def set_sb(self, sb): 
        self.sb = sb

    def reset_ship(self):
        """Reset the ship to its starting position and state."""
        self.lasers.empty()  # Clear any active lasers
        self.center_ship()  # Reset the ship's position to the center

        # Reset ship state variables
        self.dying = False  # The ship is no longer dying
        self.dead = False   # The ship is no longer dead

        # Reset the ship's image to its original state
        self.image = pg.image.load('images/ship.bmp')  # Load the original ship image


    def center_ship(self):         
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def bound(self):
        x, y, scr_r = self.x, self.y, self.screen_rect
        self.x = max(0, min(x, scr_r.width - self.rect.width))
        self.y = max(0, min(y, scr_r.height - self.rect.height))

    def ship_hit(self):
        """Handle when the ship is hit."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            print(f"Only {self.stats.ships_left} ships left now")
            self.sb.prep_ships()

            # Trigger the ship explosion animation
            self.dying = True
            self.explosion_timer.reset()  # Reset the explosion animation to start from the first frame

            # Clear lasers and fleet while the ship is resetting
            self.lasers.empty()
            self.fleet.aliens.empty()

            sleep(0.5)  # Brief delay before resetting
        else:
            self.ai_game.game_over()

    def fire_laser(self):
        """Fire a laser."""
        self.fired += 1
        if self.fired % self.settings.ship_fire_every != 0: 
            return
        laser = Laser(self.ai_game)
        self.lasers.add(laser)

    def open_fire(self): 
        self.firing = True

    def cease_fire(self): 
        self.firing = False

    def update(self):
        """Update ship's position and handle firing."""
        if self.dying:
            self.handle_explosion()
            return  # Skip movement and firing when the ship is dying

        self.x += self.v.x 
        self.y += self.v.y
        self.bound()

        if self.firing:
            self.fire_laser()

        self.lasers.update()

        # Remove lasers that are off-screen
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        # Draw lasers
        for laser in self.lasers.sprites():
            laser.draw()

        self.draw()

    def draw(self): 
        """Draw the ship on the screen."""
        if not self.dying:
            self.rect.x, self.rect.y = self.x, self.y
            self.screen.blit(self.image, self.rect)

    def handle_explosion(self):
        """Handle the explosion animation and reset the ship after it finishes."""
        if not self.explosion_timer.finished():  # If the explosion is still ongoing
            self.image = self.explosion_timer.current_image()  # Get the current explosion frame
            self.screen.blit(self.image, self.rect)  # Draw the explosion frame
        else:
            # Once the explosion finishes, reset the ship
            self.dying = False
            self.dead = True
            self.reset_ship()  # Reset the ship's position and state

            # Reset the ship's image to its original state
            self.image = pg.image.load('images/ship.bmp')  # Reset to the original ship image


def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
