import flet as ft
from coremidi.core import *
from ump import MIDIMessageCreator as m
import time

src = MIDISource("FlutterApp.py")
dst = MIDIDestination("FlutterRecv.py")
class KeyBoard():
    def __init__(self):
        self.keyToNote = {"A": 60, "W": 61, "S": 62, "E": 63, "D": 64, "F": 65, "T": 66, "G": 67, "Y": 68, "H": 69, "U": 70, "J": 71, "K": 72}
        self.cc_dict = {10: 64 << 25}
        self.noteOns = [False] * 13

    def note_on(self, key):
        midiNote = self.keyToNote[key]
        self.noteOns[midiNote-60] = True
        msg = m.midi2_0_note_on(midiNote, 2**16-1)
        src.send(msg.list_of_words())

    def note_off(self, key):
        midiNote = self.keyToNote[key]
        self.noteOns[midiNote-60] = False
        msg = m.midi2_0_note_off(midiNote, 2**16-1)
        src.send(msg.list_of_words())

    def cc_up(self, index):
        if index in self.cc_dict:
            if self.cc_dict[index] >= 2**32 -1:
                return
            num = self.cc_dict[index] >> 25
            num += 1
            self.cc_dict[index] = num << 25
        else:
            self.cc_dict[index] = 1 << 25
        if self.cc_dict[index] >= 2**32 -1:
            self.cc_dict[index] = 2**32 -1
        msg = m.midi2_0_cc(index, self.cc_dict[index])
        src.send(msg.list_of_words())

    def cc_down(self, index):
        if index in self.cc_dict:
            if self.cc_dict[index] <= 0:  
              return
            num = self.cc_dict[index] >> 25
            num -= 1
            self.cc_dict[index] = num << 25
        else:
            self.cc_dict[index] = 0
        if self.cc_dict[index] <= 0:  
              self.cc_dict[index] = 0
        msg = m.midi2_0_cc(index, self.cc_dict[index])
        src.send(msg.list_of_words())

    def is_note_on(self, key):
        midiNote = self.keyToNote[key]
        return self.noteOns[midiNote-60]

def main(page: ft.Page):
    k = KeyBoard()
    def on_keyboard(e: ft.KeyboardEvent):
        page.clean()
        if e.key == "Arrow Up":
            k.cc_up(1)
        elif e.key == "Arrow Down":
            k.cc_down(1)
        elif e.key == "Arrow Right":
            k.cc_up(10)
        elif e.key == "Arrow Left":
            k.cc_down(10)
        elif e.key == "'":
            k.cc_up(94)
        elif e.key == ";":
            k.cc_down(94)
        else:
          for letter in k.keyToNote:
              if k.is_note_on(letter):
                k.note_off(letter)
          if e.key in k.keyToNote:
              k.note_on(e.key) 
          else:
              print (e.key)
        page.add(
            ft.Text(
                f"Key: {e.key}"
            )
        )
        page.add(
            ft.Text(
                f"dst: {dst.recv()}"
            )
        )
        page.add(
            ft.Text(
            f"CC Number: {k.cc_dict}"
            )
        )

    page.on_keyboard_event = on_keyboard

    t = ft.Text(value="Welcome the MIDI2.py work please", color="black")
    # page.clean()
    page.add(t)
    

    
    
    

ft.app(target=main)