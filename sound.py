import pygame as pg 
import time


class Sound:
    def __init__(self): 

        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.levelup = pg.mixer.Sound('sounds/levelup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        self.ship_damage = pg.mixer.Sound('sounds/ship_damage.wav')
        self.menu_music = pg.mixer.Sound('sounds/menu_music.wav')
        self.laser_sound = pg.mixer.Sound('sounds/laser_sound.wav')
        self.aliendeath = pg.mixer.Sound('sounds/aliendeath.wav')

        # Load different versions of the background music at different speeds
        self.normal_music = 'sounds/FE.mp3'
        self.fast_music = 'sounds/FE1.mp3'
        self.faster_music = 'sounds/FE2.mp3'
        self.ship_explosion = 'sounds/ship_damage.wav'
        self.current_music = self.normal_music  # Start with the normal music
        self.music_playing = False
    def play_laser(self):
        self.laser_sound.play()

    def play_background(self): 
        pg.mixer.music.load(self.current_music)
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1, 0.0)  # Loop indefinitely
        self.music_playing = True

    def play_pickup(self): 
        if self.music_playing: 
            self.pickup.play()
    
    def play_explosion(self):
        self.ship_damage.play()

    def play_aliendeath(self):
        self.aliendeath.play()

    def play_levelup(self):
        self.levelup.play()

    def play_menu_music(self):
        self.menu_music.play()
        
    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(3.0)  # Sleep until the game over sound has finished
        
    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False 
    
    def adjust_music_speed(self, remaining_aliens, total_aliens):
        """Adjust background music based on the number of remaining aliens."""
        if total_aliens == 0:
            print('divided by 0')
        else:
            percentage = remaining_aliens / total_aliens
            
            if percentage > 0.6:
                # More than 60% of aliens remain, play normal music
                if self.current_music != self.normal_music:
                    self.current_music = self.normal_music
                    self.play_background()  # Restart music with the correct version
            elif 0.3 < percentage <= 0.6:
                # Between 30% and 60% aliens remain, play fast music
                if self.current_music != self.fast_music:
                    self.current_music = self.fast_music
                    self.play_background()  # Restart music with the correct version
            else:
                # Less than 30% aliens remain, play faster music
                if self.current_music != self.faster_music:
                    self.current_music = self.faster_music
                    self.play_background()  # Restart music with the correct version

    
        
    
    
