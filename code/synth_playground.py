import pygame
import random
import time

from midi2 import MIDI2

pygame.init()

FPS = 60
FONT_SIZE = 32
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('assets/ChalkboardSE.ttc', FONT_SIZE)

shapes = []
dead_shape_idxs = []
midi2_obj = MIDI2("Synth Playground")
pygame.display.set_caption("Synth Playground")

class Shape:
    def __init__(self, name, atr_num, color=None):
      self.name = name
      self.atr_num = atr_num
      self.color = color
      if color == None:
        self.color = Color()
      self.pos = 0, 0
      self.size = 0
      self.grav_speed = random.randint(5,11)
      self.time_created = int(time.time() * 1000) % 100000000

    def set_size(self, size):
      self.size = size

    def set_pos(self, xy):
      self.pos = xy[0],xy[1]

    def move_down(self, idx):
       self.pos = self.pos[0], self.pos[1] + self.grav_speed
       if self.pos[1] > HEIGHT:
          shapes.remove(self)
          midi2_obj.note_off(idx, 2**16-1)
       else:
          vol_data = (2**32 -1) * (1-(self.pos[1]/HEIGHT))
          midi2_obj.rpnc_volume(idx, int(vol_data))

    def __str__(self):
      if self.name:
        return self.name + "\npos: " + str(self.pos) + "\ncreated at: " + str(self.time_created)
      else:
         return "None"


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

def add_shape(mode):
  if (mode == 1):
    shape = Shape("circle", 1, Color())
  elif (mode == 2):
     shape = Shape("square", 2, Color())
  elif (mode == 3):
     shape = Shape("triangle", 3, Color())
  elif (mode == 4):
     shape = Shape("star", 4, Color())
  else:
     return
  shape.set_pos(pygame.mouse.get_pos())
  shape.set_size(20)
  if len(dead_shape_idxs) == 0:
    idx = len(shapes)
    shapes.append(shape)
  else:
    idx = dead_shape_idxs[0]
    shapes[idx] = shape
    dead_shape_idxs.pop(0)
  pan_data = (shape.pos[0]/WIDTH) * (2**32-1)
  midi2_obj.rpnc_pan(idx, int(pan_data))
  midi2_obj.note_on(idx, int(shape.size/100 * 128) << 9, 1, mode)

def remove_shape(key):
  oldest = None, -1
  for i, s in enumerate(shapes):
    if ((key == 'q' and s.name == "circle") or\
        (key == 'w' and s.name == "square") or\
        (key == 'e' and s.name == "triangle") or\
        (key == 'r' and s.name == "star")):
      if not oldest[0] or oldest[0].time_created > s.time_created:
          oldest = s, i
  if oldest[0]:
    dead_shape_idxs.append(oldest[1])
    midi2_obj.note_off(oldest[1], int(oldest[0].size/100 * 128) << 9, 1, ("circle", "square", "triangle", "star").index(oldest[0].name))
    oldest[0].name = None


def draw_shape(shape):
    if shape.name == None:
       return
    
    if shape.atr_num == 1:
        pygame.draw.circle(WIN, shape.color.tuple(), shape.pos, shape.size)
    elif shape.atr_num == 2:
      pygame.draw.rect(WIN, shape.color.tuple(), pygame.Rect(shape.pos[0], shape.pos[1], shape.size*2, shape.size*2))
    elif shape.atr_num == 3:
       x = shape.pos[0]
       y = shape.pos[1]
       pygame.draw.polygon(WIN, shape.color.tuple(), ((x,y-shape.size), (x-shape.size, y+shape.size), (x+shape.size, y+shape.size)))
    elif shape.atr_num == 4:
       x = shape.pos[0]
       y = shape.pos[1]
       pygame.draw.polygon(WIN, shape.color.tuple(), ((x-shape.size//4, y-shape.size//4), (x, y-shape.size), (x+shape.size//4, y-shape.size//4), (x+shape.size, y-shape.size//3), (x+shape.size//4, y+shape.size//4), (x+2*shape.size//3, y+shape.size), (x, y+shape.size//2), (x-2*shape.size//3, y+shape.size), (x-shape.size//4, y+shape.size//4), (x-shape.size, y-shape.size//3)))
    # pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    mode = 0
    modes = ["None", "Sine", "Square", "Triangle", "Saw"]
    gravity = False
    t = 0
    while run:
        WIN.fill((0,0,0))

        mode_text = FONT.render("Mode: " + modes[mode], True, (255, 255, 255))
        gravity_text = FONT.render("Gravity: " + ("ON" if gravity else "OFF"), True, (255, 255, 255))
        WIN.blit(mode_text, (20,20))
        WIN.blit(gravity_text, (20, 52))
        clock.tick(FPS)
        t += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in ('1','2','3','4'):
                  mode = int(event.unicode)
                elif event.unicode == ' ':
                  gravity = not gravity
                elif event.unicode in ('q', 'w', 'e', 'r'):
                  remove_shape(event.unicode)
                  
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                add_shape(mode)                
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            
        for i, s in enumerate(shapes):
          if gravity:
            s.move_down(i)
            t = 0
          draw_shape(s)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()