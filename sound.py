import pygame as pg 
import time


class Sound:
    def __init__(self): 
        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        pg.mixer.music.load('sounds/FE.mp3')
        pg.mixer.music.set_volume(0.2)
                                             
    def play_background(self): 
        pg.mixer.music.play(-1, 0.0)
        self.music_playing = True
        
    def play_pickup(self): 
        if self.music_playing: self.pickup.play()
        
    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(3.0)       # sleep until game over sound has finished
        
    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False 
    
        
    
    
