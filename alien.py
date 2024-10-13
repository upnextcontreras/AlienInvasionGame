'''

Space Invaders Project CPSC386 
Christopher Contreras
Kristian Losenara

 '''
import pygame as pg
from vector import Vector
from laser import Laser  # Make sure Laser is imported here
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]


    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v  # Base velocity of the alien

        self.type = randint(0, 2)  # Get alien type and assign it to self.type

        self.timer = Timer(images=Alien.alien_images[self.type], delta=(self.type + 1) * 600, start_index=self.type % 2)

        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dying = False
        self.dead = False

        self.laser_timer = randint(200, 500)  # Adjusted random timer for firing lasers

        # Initialize explosion timer
        self.explosion_images = [pg.image.load(f'images_other/alien_boom_frames/explosion{n}.png') for n in range(6)]  # Replace with your actual explosion frames
        self.explosion_timer = Timer(images=self.explosion_images, delta=1000, loop_continuously=False)  # Timer to control animation

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self.x + self.rect.width >= sr.right or self.x <= 0

    def fire_laser(self):
        """Alien fires a laser."""
        if self.laser_timer <= 0:
            # Fire a laser from the alien's position and reset the timer
            new_laser = Laser(self.ai_game, position=self.rect.midbottom, direction=1, color=(255, 0, 0))  # Red laser going down
            self.ai_game.alien_lasers.add(new_laser)
            self.laser_timer = randint(200, 500)  # Reset the laser timer to a new random interval (faster firing)
        else:
            self.laser_timer -= 1

    def update(self):
        """Update the alien's position and attempt to fire lasers, handle explosion if needed."""
        if self.dying:
            self.handle_explosion()  # Handle the explosion if alien is dying
        else:
            remaining_aliens = len(self.ai_game.fleet.aliens)  # Get the number of remaining aliens

            # Increase velocity as the number of remaining aliens decreases
            speed_multiplier = max(1, 5 - remaining_aliens // 10)  # Example logic: speed up as the number of aliens drops

            self.x += self.v.x * speed_multiplier
            self.y += self.v.y * speed_multiplier

            self.fire_laser()  # Alien attempts to fire a laser during its update cycle

            self.image = self.timer.current_image()
            self.draw()

    def handle_explosion(self):
        """Handle the explosion animation and remove the alien after it's done."""
        if not self.explosion_timer.finished():  # If the explosion is still ongoing
            self.image = self.explosion_timer.current_image()  # Get the current explosion frame
            self.screen.blit(self.image, self.rect)  # Draw the explosion frame
  

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()