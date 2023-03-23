def b2(input):
    return bin(input)[2:]
"""
message type: indicates the message's general functional area (Utility, MIDI 1.0 Channel Voice Messages, etc)
as well as UMP size and size of status field

group: indicates group of the UMP (out of 16). each group communicates using either MIDI 1.0 or MIDI 2.0
messages such as System Message, Data Messages that do not support MIDI channel field affect all MIDI channels in a group

status: indicates a message within a message type. size of the status depends on the message type


"""
class UniversalMIDIPacket:
    def __init__(self, name, message_type, group, status, index=None, data=None):
        self.name = name
        self.message_type = message_type
        # mt0 = utility msg (32bit)
        # mt1 = system real time and system common messages (32bit)
        # mt2 = MIDI 1.0 Channel Voice Messages (32bit)
        # mt3 = Data Messages (64bit Including System Exclusive)
        # mt4 = MIDI 2.0 Channel Voice Messages (64bit)
        # mt5 = Data Messages (128bit)
        self.group = int(group)
        self.status = int(status) 
        self.index = int(index)
        self.data = int(data)

    def packet_to_binary(self):
        PACKET_SIZE = 32 if (self.message_type == 0 or
                             self.message_type == 1 or
                             self.message_type == 2) else \
                      64 if (self.message_type == 3 or
                             self.message_type == 4) else \
                      128
        STATUS_SIZE = 8 if (self.message_type == 1 or 
                            self.message_type == 2 or 
                            self.message_type == 4) else 4
        DATA_SIZE = 16 if (self.message_type == 0 or 
                           self.message_type == 1 or
                           self.message_type == 2) else \
                    48 if (self.message_type == 3) else \
                    32 if (self.message_type == 4) else \
                   112#if (self.message_type == 5)
        INDEX_SIZE = 16 if (self.message_type == 4) else \
                     8
        packet = 0
        if self.data != None:
            packet |= self.data

        if self.index != None:
          packet |= self.index << DATA_SIZE
          packet |= self.status << (INDEX_SIZE + DATA_SIZE)
          packet |= self.group << (INDEX_SIZE + DATA_SIZE + STATUS_SIZE)
          packet |= self.message_type << (INDEX_SIZE + DATA_SIZE + STATUS_SIZE + 4)
        else:
          packet |= self.status << (DATA_SIZE)
          packet |= self.group << (DATA_SIZE + STATUS_SIZE)
          packet |= self.message_type << (DATA_SIZE + STATUS_SIZE + 4)
        packet_str = bin(packet).replace("0b", "")
        assert len(packet_str) <= PACKET_SIZE,\
            f"expected a packet of length {PACKET_SIZE}, but got {packet_str}: len={len(packet_str)}"
        return packet_str.zfill(PACKET_SIZE)

    def packet_to_hex(self):
        return hex(int(self.packet_to_binary(),2))
    
    def list_of_words(self):
        packet_list = []
        pkt = self.packet_to_binary()
        while len(pkt) > 0:
          packet_list.append(int(pkt[:32],2))
          pkt = pkt[32:]
        return packet_list
        
    def __str__(self):
        return self.name + '\n' + \
            "Message Type: " + str(self.message_type) + '\n' \
            "Group: " + str(self.group) + '\n' + \
            "Data: " + str(self.data)+'\n'+\
            self.packet_to_binary() +'\n'+\
            self.packet_to_hex() + '\n' +\
            str(self.list_of_words())
        

class MIDIMessageCreator:
    def __init__(self):
        pass

    def midi1_0_note_off(note_num:int, vel:int, group=0, channel=0):
        data = note_num << 8 | vel
        status = int("1000", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note Off Message", 2, group, status=status, data=data)

    def midi1_0_note_on(note_num:int, vel:int, group=0, channel=0):
        data = note_num << 8 | vel
        status = int("1001", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note On Message", 2, group, status=status, data=data)

    def midi1_0_poly_pressure(note_num:int, data:int, group=0, channel=0):
        status = int("1010", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Poly Pressure Message", 2, group, status=status, data=note_num << 8 | data)

    def midi1_0_cc(index:int, data:int, group=0, channel=0):
        status = int("1011", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Control Change Message", 2, group, status=status, index=index, data=data)

    def midi1_0_program_change(program, group=0, channel=0):
        data = program << 8
        status = int("1100", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Program Change Message", 2, group, status=status, data=data)

    def midi1_0_channel_pressure(data, group=0, channel=0):
        data = data << 8
        status = int("1101", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Channel Pressure Message", 2, group, status=status, data=data)

    def midi1_0_pitch_bend(lsb_data:int, msb_data:int, group=0, channel=0):
        data = int(lsb_data) << 8 | int(msb_data)
        status = int("1110", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Pitch Bend Message", 2, group, status << 4 | ch, data=data)
        
    def midi2_0_note_off(note_num:int, vel:int, atribute_type=0, atribute_data=0, group=0, channel=0):
        status = int('1000', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(atribute_type)
        data = int(vel) << 16 | int(atribute_data) 
        return UniversalMIDIPacket("MIDI 2.0 Note Off Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_note_on(note_num: int, vel:int, atribute_type=0, atribute_data=0, group=0, channel=0):
        status = int('1001', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(atribute_type)
        data = int(vel) << 16 | int(atribute_data)
        return UniversalMIDIPacket("MIDI 2.0 Note On Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_poly_pressure(note_num, data, group=0, channel=0):
        status = int('1010', 2) << 4 | int(channel)
        index = int(note_num) << 8
        return UniversalMIDIPacket("MIDI 2.0 Poly Pressure Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_reg_per_note(note_num, index, data, group=0, channel=0):
        status = int('0000', 2) << 4 | int(channel)
        index = int(note_num) << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Registered Per-Note Controller Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_asn_per_note(note_num, index, data, group=0, channel=0):
        status = int('0001', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(index)
        return UniversalMIDIPacket("MIDI 2.0 Assignable Per-Note Controller Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_per_note_management(note_num, d, s, group=0, channel=0):
        status = int('1111', 2) << 4 | int(channel)
        index = int(note_num) << 8 | d << 1 | s
        return UniversalMIDIPacket("MIDI 2.0 Per-Note Management Message", 4, group, status=status, index=index, data=0)

    def midi2_0_cc(index, data, group=0, channel=0):
        status = int("1011", 2) << 4 | int(channel)
        index = index << 8
        return UniversalMIDIPacket("MIDI 2.0 Control Change Message", 4, group, status=status, index=index, data=data)

    def midi2_0_reg_controller(bank, index, data, group=0, channel=0):
        status = int("0010", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Registered Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_asn_controller(bank, index, data, group=0, channel=0):
        status = int("0011", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Assignable Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_rel_reg_controller(bank, index, data, group=0, channel=0):
        status = int("0100", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Relative Registered Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_rel_asn_controller(bank, index, data, group=0, channel=0):
        status = int("0101", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Relative Assignable Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_program_change(b, program, bank_msb, bank_lsb, group=0, channel=0):
        """
        MIDI 2.0 Program Change Message

        Option Flags:
        b - if set to 0, the receiever performs only the Program Change without
            selecting a new bank
            if set to 1, the receiever performs the bank selection, then the
            Program Change 
        """
        status = int("1100", 2) << 4 | int(channel)
        index = b
        data = program << 24 | bank_msb << 8 | bank_lsb
        return UniversalMIDIPacket("MIDI 2.0 Program Change Message", 4, group, status=status, index=index, data=data)
    
    def midi2_0_channel_pressure(data, group=0, channel=0):
        status = int("1101", 2) << 4 | int(channel)
        index = 0
        return UniversalMIDIPacket("MIDI 2.0 Channel Pressure Message", 4, group, status=status, index=index, data=data)
    
    def midi2_0_pitch_bend(data, group=0, channel=0):
        status = int("1110", 2) << 4 | int(channel)
        index = 0
        return UniversalMIDIPacket("MIDI 2.0 Pitch Bend Message", 4, group, status=status, index=index, data=data)

    def midi2_0_per_note_pitch_bend(note_num, data, group=0, channel=0):
        status = int("0110", 2) << 4 | int(channel)
        index = int(note_num) << 8
        return UniversalMIDIPacket("MIDI 2.0 Per-Note Pitch Bend Message", 4, group, status=status, index=index, data=data)