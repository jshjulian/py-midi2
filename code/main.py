from coremidi.core import *
from ump import MIDIMessageCreator as m
import time

while True:
  src = None
  dst = None
  answer = input("1) Input\n2) Output\n")
  if answer == "1":
    src = MIDISource("python midi note sender")
    break
  elif answer == "2":
    dst = MIDIDestination("python midi note receiver")
    break
  
def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
    
def play_maj_chord(note:int):
  x = m.midi2_0_note_on(note, 2**16-1)
  y = m.midi2_0_note_on(note+4, 2**16-1)
  z = m.midi2_0_note_on(note+7, 2**16-1)
  src.send(x.list_of_words())
  src.send(y.list_of_words())
  src.send(z.list_of_words())
  x = m.midi2_0_note_off(note, 2**16-1)
  y = m.midi2_0_note_off(note+4, 2**16-1)
  z = m.midi2_0_note_off(note+7, 2**16-1)
  time.sleep(2)
  src.send(x.list_of_words())
  src.send(y.list_of_words())
  src.send(z.list_of_words())

def play_min_chord(note:int):
  x = m.midi2_0_note_on(note, 2**16-1)
  y = m.midi2_0_note_on(note+3, 2**16-1)
  z = m.midi2_0_note_on(note+7, 2**16-1)
  src.send(x.list_of_words())
  src.send(y.list_of_words())
  src.send(z.list_of_words())
  x = m.midi2_0_note_off(note, 2**16-1)
  y = m.midi2_0_note_off(note+3, 2**16-1)
  z = m.midi2_0_note_off(note+7, 2**16-1)
  time.sleep(2)
  src.send(x.list_of_words())
  src.send(y.list_of_words())
  src.send(z.list_of_words())

def play_251(note:int):
   min2 = (note, note+3, note+7)
   maj5_2nd = (note, note+5, note+9)
   maj1_1st = (note+2, note+5, note+10)
   for chord in (min2, maj5_2nd, maj1_1st):
      for n in chord:
         cmd = m.midi2_0_note_on(n, 2**16-1)
         src.send(cmd.list_of_words())
      
      if chord == maj5_2nd:
        time.sleep(1)
        cmd = m.midi2_0_per_note_pitch_bend(note+5, 0)
        src.send(cmd.list_of_words())
        time.sleep(1)
      else:
        time.sleep(2)
      
      for n in chord:
         cmd = m.midi2_0_note_off(n, 0)
         src.send(cmd.list_of_words())


while True:
  if src == None:
     print (dst.recv())
     q = input("press q: ")
     if q == 'q':
        break
  note = input("Note Number: ")
  
  if note == "q":
    break
  elif is_integer(note):
    x = m.midi2_0_note_on(note, 2**14)
    y = m.midi2_0_pitch_bend(2**5)
    y2 = m.midi2_0_pitch_bend(2**16//2)
    src.send(y2.list_of_words())
    z = m.midi2_0_note_off(note, 0)

    src.send(x.list_of_words())
    time.sleep(1)
    src.send(y.list_of_words())
    time.sleep(1)
    src.send(y2.list_of_words())
    src.send(z.list_of_words())
    
    # play_251(int(note))

    # mode = input("Major or Minor: ")
    # if mode == "Major":
    #   play_maj_chord(int(note))
    # else:
    #   play_min_chord(int(note))
     
  
  