import pygame as pg
from pygame.sprite import Sprite
from random import randint

class Laser(Sprite):
    @staticmethod
    def random_color(): 
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def __init__(self, ai_game, position, direction=-1, color=None):  # Add direction and color as parameters
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = color if color else Laser.random_color()  # Default to random color if none is provided
        self.rect = pg.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
        self.rect.midtop = position  # Use the passed position for laser placement
        self.y = float(self.rect.y)
        self.direction = direction  # -1 for up, 1 for down (aliens)

    def update(self):
        """Move the laser up or down based on the direction."""
        self.y += self.settings.laser_speed * self.direction
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
