import pygame
import random

from midi2 import MIDI2

pygame.init()

FPS = 60
FONT_SIZE = 64
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('assets/AmericanTypewriter.ttc', FONT_SIZE)
PRESETS = ["24TET", "18TET", "MACROTET", "31-EDO"]
currentPreset = 0

keys = {}
# src = MIDISource("MIDI 2.0 Keyboard")
midi2_obj = MIDI2("MIDI 2.0 Keyboard")
pygame.display.set_caption("MIDI 2.0 Keyboard")
first_row = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
second_row = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
third_row = ["z", "x", "c", "v", "b", "n", "m"]
all_keys = first_row + second_row + third_row

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
    full_idx = all_keys.index(key)
    if PRESETS[currentPreset] == "24TET":
        inc = full_idx/24 * 12
        semitone = int(inc)
        frac_of_semitone = inc - semitone
    elif PRESETS[currentPreset] == "18TET":
        inc = full_idx/18 * 12
        semitone = int(inc)
        frac_of_semitone = inc-semitone
    elif PRESETS[currentPreset] == "31-EDO":
        inc = full_idx/31 * 12
        semitone = int(inc)
        frac_of_semitone = inc-semitone
    elif PRESETS[currentPreset] == "MACROTET":
        container = None
        if key in first_row:
            container = first_row
        elif key in second_row:
            container = second_row
        elif key in third_row:
            container = third_row
        else:
            return
        idx = container.index(key)
        inc = idx/len(container) * 12
        semitone = int (inc)
        frac_of_semitone = inc - semitone
    else:
        return
    midi2_obj.note_on_pitch_7_9(full_idx, 2**16-1, 60+semitone, frac_of_semitone)

def key_unpress_atr3(key):
    full_idx = all_keys.index(key)
    if PRESETS[currentPreset] == "24TET":
        inc = full_idx/24 * 12
        semitone = int(inc)
        frac_of_semitone = inc - semitone
    elif PRESETS[currentPreset] == "18TET":
        inc = full_idx/18 * 12
        semitone = int(inc)
        frac_of_semitone = inc-semitone
    elif PRESETS[currentPreset] == "31-EDO":
        inc = full_idx/31 * 12
        semitone = int(inc)
        frac_of_semitone = inc-semitone
    elif PRESETS[currentPreset] == "MACROTET":
        container = None
        if key in first_row:
            container = first_row
        elif key in second_row:
            container = second_row
        elif key in third_row:
            container = third_row
        else:
            return
        idx = container.index(key)
        inc = idx/len(container) * 12
        semitone = int (inc)
        frac_of_semitone = inc - semitone
    else:
        return
    midi2_obj.note_on_pitch_7_9(full_idx, 2**16-1, 60+semitone, frac_of_semitone)

def key_press(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.rpnc_pitch_7_25(60+note_idx, 60+note_idx, note_idx/len(list(keys.keys())))
    midi2_obj.note_on(60+note_idx, 2**16-1)
def key_unpress(key):
    note_idx = list(keys.keys()).index(key)
    midi2_obj.rpnc_pitch_7_25(60+note_idx, 60+note_idx, note_idx/len(list(keys.keys())))
    midi2_obj.note_off(60+note_idx, 2**16-1)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in all_keys:
                    keys[event.unicode] = True
                    key_press(event.unicode)
                elif event.unicde == " ":
                    currentPreset = (currentPreset+1) % len(PRESETS)
            elif event.type == pygame.KEYUP:
                if event.unicode in all_keys:
                    keys[event.unicode] = False
                    key_unpress(event.unicode)
            
        # random_background()
        WIN.fill((0,0,0))
        draw_letters()
    pygame.quit()

if __name__ == "__main__":
    main()