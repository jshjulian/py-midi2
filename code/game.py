import pygame
import random

from coremidi.core import *
from ump import MIDIMessageCreator as m

from midi2 import MIDI2

pygame.init()

FPS = 60
FONT_SIZE = 64
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('assets/AmericanTypewriter.ttc', FONT_SIZE)

keys = {}
# src = MIDISource("MIDI 2.0 Keyboard")
midi2_obj = MIDI2("MIDI 2.0 Keyboard")
pygame.display.set_caption("MIDI 2.0 Keyboard")
first_row = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
second_row = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
third_row = ["z", "x", "c", "v", "b", "n", "m"]
letter_pos = {}

for i, letter in enumerate(first_row):
    letter_pos[letter] = (i+1)*FONT_SIZE, FONT_SIZE

for i, letter in enumerate(second_row):
    letter_pos[letter] = (FONT_SIZE//8 + (i+1)*FONT_SIZE), 2*FONT_SIZE

for i, letter in enumerate(third_row):
    letter_pos[letter] = (FONT_SIZE//4 + (i+1)*FONT_SIZE), 3*FONT_SIZE

class Color:
    def __init__(self, r=None, g=None, b=None):
        if r == None or g == None or b == None:
            self.r = random.randint(0,255)
            self.g = random.randint(0,255)
            self.b = random.randint(0,255)
        else:
            self.r = r
            self.g = g
            self.b = b

    def tuple(self):
        return self.r, self.g, self.b
    
    def opposite(self):
        return 255-self.r, 255-self.g, 255-self.b
    
def random_background():
    WIN.fill(Color().tuple())
    pygame.display.update()

def draw_letters():
    for letter in keys:
        if keys[letter] and letter in letter_pos:
            img = FONT.render(letter, True, Color().tuple())
            x,y = letter_pos[letter]
            WIN.blit(img, (x+50,y))
    pygame.display.update()

def key_press_atr3(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.note_on_pitch_7_9(note_idx, 2**16-1, 60+note_idx, note_idx / len(list(keys.keys())))
def key_unpress_atr3(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.note_off_pitch_7_9(note_idx, 2**16-1, 60+note_idx, note_idx / len(list(keys.keys())))

def key_press(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.rpnc_pitch_7_25(note_idx, 60+note_idx, note_idx/len(list(keys.keys())))
    midi2_obj.note_on(note_idx, 2**16-1)
def key_unpress(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.rpnc_pitch_7_25(note_idx, 60+note_idx, note_idx/len(list(keys.keys())))
    midi2_obj.note_off(note_idx, 2**16-1)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                keys[event.unicode] = True
                key_press(event.unicode)
            elif event.type == pygame.KEYUP:
                keys[event.unicode] = False
                key_unpress(event.unicode)
            
        # random_background()
        WIN.fill((0,0,0))
        draw_letters()
    pygame.quit()

if __name__ == "__main__":
    main()