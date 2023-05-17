from coremidi.core import *
from ump import MIDIMessageCreator as m
import random

class MIDI2:
  def __init__(self, name="Python MIDI 2.0"):
    self.name = name
    self.src = MIDISource(name + " src")
    self.dst = MIDIDestination(name + " dst")
    self.muid = random.getrandbits(32)
    self.muid_bytes = [
      self.muid     & int("ff", 16), 
      self.muid>>8  & int("ff", 16),
      self.muid>>16 & int("ff", 16),
      self.muid>>24 & int("ff", 16)
    ]

  def recv(self):
    data = self.dst.recv()
    new_data = []
    for x in data:
      new_data.append(hex(x))
    return new_data
  
  def note_on(self, note_num, vel, atr_type=0, atr_data=0, group=0, channel=0):
    msg = m.midi2_0_note_on(note_num, vel, atribute_type=atr_type, atribute_data=atr_data, group=group, channel=channel)
    self.src.send(msg())

  def note_off(self, note_num, vel, atr_type=0, atr_data=0, group=0, channel=0):
    msg = m.midi2_0_note_off(note_num, vel, atribute_type=atr_type, atribute_data=atr_data, group=group, channel=channel)
    self.src.send(msg())

  def note_on_pitch_7_9(self, note_idx, vel, pitch, frac_of_semitone, group=0, channel=0):
    semitones = int (frac_of_semitone * (2**9-1))
    data = pitch << 9 | semitones
    msg = m.midi2_0_note_on(note_idx, vel, 3, data, group, channel)
    self.src.send(msg())

  def note_off_pitch_7_9(self, note_idx, vel, pitch, frac_of_semitone, group=0, channel=0):
    semitones = int (frac_of_semitone * (2**9-1))
    data = pitch << 9 | semitones
    msg = m.midi2_0_note_off(note_idx, vel, 3, data, group, channel)
    self.src.send(msg())

  def rpnc(self, note_idx, num, data, group=0, channel=0):
    msg = m.midi2_0_reg_per_note(note_idx, num, data, group, channel)
    self.src.send(msg())

  def rpnc_modulation(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 1, data, group, channel)

  def rpnc_breath(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 2, data, group, channel)

  def rpnc_pitch_7_25(self, note_idx, pitch, frac_of_semitone, group=0, channel=0):
    semitones = int(frac_of_semitone * (2**25-1))
    data = pitch << 25 | semitones
    self.rpnc(note_idx, 3, data, group, channel)

  def rpnc_volume(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 7, data, group, channel)

  def rpnc_balance(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 8, data, group, channel)

  def rpnc_pan(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 10, data, group, channel)

  def rpnc_expression(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 11, data, group, channel)

  def rpnc_reverb(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 91, data, group, channel)

  def rpnc_chorus(self, note_idx, data, group=0, channel=0):
    self.rpnc(note_idx, 93, group, channel)

  def cc(self, num, data, group=0, channel=0):
    msg = m.midi2_0_cc(num, data, group, channel)
    self.src.send(msg())

  def cc_modulation(self, data, group=0, channel=0):
    self.cc(1, data, group, channel)

  def cc_foot_pedal(self, data, group=0, channel=0):
    self.cc(4, data, group, channel)

  def cc_volume(self, data, group=0, channel=0):
    self.cc(7, data, group, channel)

  def cc_pan(self, data, group=0, channel=0):
    self.cc(10, data, group, channel)

  def cc_expression(self, data, group=0, channel=0):
    self.cc(11, data, group, channel)

  def cc_damper_pedal(self, is_on, group=0, channel=0):
    if is_on:
      self.cc(64, 127, group, group)
    else:
      self.cc(64, 0, group, channel)

  def cc_portamento(self, is_on, group=0, channel=0):
    if is_on:
      self.cc(65, 127, group, channel)
    else:
      self.cc(65, 0, group, channel)

  def cc_sostenuto(self, is_on, group=0, channel=0):
    if is_on:
      self.cc(66, 127, group, channel)
    else:
      self.cc(66, 0, group, channel)

  def cc_soft_pedal(self, is_on, group=0, channel=0):
    if is_on:
      self.cc(67, 127, group, channel)
    else:
      self.cc(67, 0, group, channel)
  
  def cc_resonance(self, data, group=0, channel=0):
    self.cc(71, data, group, channel)

  def cc_cutoff_freq(self, data, group=0, channel=0):
    self.cc(74, data, group, channel)

  def cc_portamento_control(self, data, group=0, channel=0):
    self.cc(84, data, group, channel)

  def cc_reverb(self, data, group=0, channel=0):
    self.cc(91, data, group, channel)

  def cc_chorus(self, data, group=0, channel=0):
    self.cc(93, data, group, channel)

  def cc_all_sound_off(self, group=0):
    self.cc(120, 0, group)

  def cc_reset_all_controllers(self, group=0):
    self.cc(121, 0, group)

  def cc_local_control(self, is_on, group=0):
    if is_on:
      self.cc(122, 127, group)
    else:
      self.cc(122, 0, group)

  def cc_all_notes_off(self, group=0):
    self.cc(123, 0, group)

  def cc_omni_mode_off(self, group=0):
    self.cc(124, 0, group)

  def cc_omni_mode_on(self, group=0):
    self.cc(125, 0, group)

  def cc_mono_mode(self, group=0):
    self.cc(126, 0, group)

  def cc_poly_mode(self, group=0):
    self.cc(127, 0, group)

  def discovery_inquiry(self, group=0): 
    data_list_1 = [
      int("7e", 16),
      int("7f", 16),
      int("0d", 16),
      int("70", 16),
      int("01", 16),
      self.muid_bytes[0],
      self.muid_bytes[1],
      self.muid_bytes[2],
      self.muid_bytes[3],
      int("7f", 16),
      int("7f", 16),
      int("7f", 16),
      int("7f", 16)
    ]
    data_list_2 = [
      int("7d", 16),
      int("00", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("00", 16),
      int("00", 16),
      int("00001110", 2),
    ]
    data_list_3 = [
      int("00", 16),
      int("02", 16),
      int("00", 16),
      int("00", 16),
    ]
    msg = m.system_exclusive_8bit(1, 14, data_list_1)
    self.src.send(msg())
    msg = m.system_exclusive_8bit(2, 13, data_list_2)
    self.src.send(msg())
    msg = m.system_exclusive_8bit(3, 5, data_list_3)
    self.src.send(msg())

  def reply_to_discovery_inquiry(self, dest_bytes, group=0): 
    data_list_1 = [
      int("7e", 16),
      int("7f", 16),
      int("0d", 16),
      int("71", 16),
      int("01", 16),
      self.muid_bytes[0],
      self.muid_bytes[1],
      self.muid_bytes[2],
      self.muid_bytes[3],
      int(dest_bytes[0], 16),
      int(dest_bytes[1], 16),
      int(dest_bytes[2], 16),
      int(dest_bytes[3], 16)
    ]
    data_list_2 = [
      int("7d", 16),
      int("00", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("01", 16),
      int("00", 16),
      int("00", 16),
      int("00", 16),
      int("00001110", 2),
    ]
    data_list_3 = [
      int("00", 16),
      int("02", 16),
      int("00", 16),
      int("00", 16),
    ]
    msg = m.system_exclusive_8bit(1, 14, data_list_1, group=group)
    self.src.send(msg())
    msg = m.system_exclusive_8bit(2, 13, data_list_2, group=group)
    self.src.send(msg())
    msg = m.system_exclusive_8bit(3, 5, data_list_3, group=group)
    self.src.send(msg())
