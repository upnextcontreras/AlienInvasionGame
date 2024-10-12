import pygame as pg
from vector import Vector
from laser import Laser
from time import sleep
from pygame.sprite import Sprite
from timer import Timer  
from sound import Sound

class Ship(Sprite):
    def __init__(self, ai_game, v=Vector()):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.sound = Sound()
        self.sb = None

        # Load the ship image created using a pixel editor
        self.image = pg.image.load('images/ship.png')  # Replace with your pixel art ship image
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
        self.explosion_images = [pg.image.load(f'images_other/ship_boom_frames/frame_0{n}.png') for n in range(11)]  # Replace with your actual explosion frames
        self.explosion_timer = Timer(images=self.explosion_images, delta=30, loop_continuously=False)  # Timer to control animation

         # Flags to manage state
        self.dying = False  # Ship is hit but animation still running
        self.dead = False    # Ship is completely destroyed
        self.invincible = False  # Add flag for invincibility after hit
        self.invincibility_duration = 2000  # Set invincibility to 2 seconds (2000 ms)
        self.invincibility_start_time = 0  # Track the time when invincibility starts

    def set_fleet(self, fleet): 
        self.fleet = fleet

    def set_sb(self, sb): 
        self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()
        self.ai_game.ship_hit_flag = False  # Reset the ship hit flag

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
        if not self.invincible and self.stats.ships_left > 0:  # Check if the ship is not invincible
            self.stats.ships_left -= 1
            print(f"Only {self.stats.ships_left} ships left now")
            self.sb.prep_ships()

            # Trigger the ship explosion animation
            self.dying = True
            self.explosion_timer.reset()  # Reset the explosion animation to start from the first frame

            # Set the ship hit flag to True so we can prevent level-up
            self.ai_game.ship_hit_flag = True

            # Clear lasers and fleet while the ship is resetting
            self.lasers.empty()
            self.fleet.aliens.empty()

            sleep(0.5)  # Brief delay before resetting

            # Set invincibility after getting hit
            self.invincible = True
            self.invincibility_start_time = pg.time.get_ticks()  # Get the time when invincibility starts
        elif self.stats.ships_left == 0:
            self.ai_game.game_over()

    def fire_laser(self):
        """Fire a laser from the ship."""
        self.fired += 1
        if self.fired % self.settings.ship_fire_every != 0: 
            return
        laser = Laser(self.ai_game, position=self.rect.midtop, direction=-1)  # Laser going up
        self.lasers.add(laser)
        self.sound.play_laser()

    def open_fire(self): 
        self.firing = True

    def cease_fire(self): 
        self.firing = False

    def update(self):
        """Update ship's position and handle firing."""
        if self.dying:
            self.handle_explosion()
            return  # Skip movement and firing when the ship is dying

        # Manage invincibility timeout
        if self.invincible:
            current_time = pg.time.get_ticks()
            if current_time - self.invincibility_start_time > self.invincibility_duration:
                self.invincible = False  # Disable invincibility after the duration

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
            self.sound.play_explosion() #put explosion here to better line up 
            self.dying = False
            self.dead = True
            self.reset_ship()  # Reset the ship's position and state

            # Reset the ship's image to its original state
        self.image = pg.image.load('images/ship.png')  # Reset to the original ship image


def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
