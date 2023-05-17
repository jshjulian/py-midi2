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
    """
    A class to desciribe the Universal MIDI Packet (UMP)

    Attributes
    ----------
    name : str
      a string for the name of the UMP
    message_type : int
      a number representing the message type of the UMP
      0 = Utility Messsage
      1 = System Real Time and System Common Messages
      2 = MIDI 1.0 Channel Voice Message
      3 = 64 bit Data Message (including System Exclusive)
      4 = MIDI 2.0 Channel Voice Message
      5 = 128 bit Data Message
    group : int
      number representing the group of the UMP
    status : int
      number representing the status of the UMP
    index : int, optional
      number representing the index of the UMP
      not required for all UMP messages
    data : int, optional
      number representing the data of the UMP
      not required for all UMP messages

    Methods
    -------
    packet_to_binary()
      returns string of binary representation of UMP
    packet_to_hex()
      returns string of hexadecimal representation of UMP
    list_of_words()
      returns list of 32 bit integers representing the representation of UMP
    """
    def __init__(self, name:str, message_type:int, group:int, status:int, index:int=None, data:int=None):
        self.name = name
        self.message_type = int(message_type)
        self.group = int(group)
        self.status = int(status) 
        if index:
          self.index = int(index)
        else:
          self.index = None
        if data:
          self.data = int(data)
        else:
          self.data = None
        self.packet = self.list_of_words()

    def packet_to_binary(self)->str:
        """
        Returns String of Binary Representation of UMP
        """
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
                   112 if (self.message_type == 5) else \
                   0
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

        # check to make sure packet is correct size
        assert len(packet_str) <= PACKET_SIZE,\
            f"expected a packet of length {PACKET_SIZE}, but got {packet_str}: len={len(packet_str)}"
        return packet_str.zfill(PACKET_SIZE)

    def packet_to_hex(self):
        """
        Returns String of Hexadecimal representation of UMP
        """
        return hex(int(self.packet_to_binary(),2))
    
    def list_of_words(self):
        """
        Returns list of 32 bit words representing the UMP
        """
        packet_list = []
        pkt = self.packet_to_binary()
        while len(pkt) > 0:
          packet_list.append(int(pkt[:32],2))
          pkt = pkt[32:]
        return packet_list
        
    def __call__(self) -> list:
        return self.packet
    
    def __str__(self):
        return self.name + '\n' + \
            "Message Type: " + str(self.message_type) + '\n' \
            "Group: " + str(self.group) + '\n' + \
            "Data: " + str(self.data)+'\n'+\
            self.packet_to_binary() +'\n'+\
            self.packet_to_hex() + '\n' +\
            str(self.list_of_words())
        

class MIDIMessageCreator:
    """
    A class for creating UMPs
    """
    def __init__(self):
        pass

    def midi1_0_note_off(note_num:int, vel:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Note Off Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        vel : int
          Velocity (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        data = note_num << 8 | vel
        status = int("1000", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note Off Message", 2, group, status=status, data=data)

    def midi1_0_note_on(note_num:int, vel:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Note On Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        vel : int
          Velocity (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        data = note_num << 8 | vel
        status = int("1001", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Note On Message", 2, group, status=status, data=data)

    def midi1_0_poly_pressure(note_num:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Poly Pressure Message (Polyphonic Aftertouch)

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        data : int
          Poly Pressure Data (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1010", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Poly Pressure Message", 2, group, status=status, data=note_num << 8 | data)

    def midi1_0_cc(index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Control Change Message

        Parameters
        ----------
        index : int
          Control Change Number Index (7 bits)
        data : int
          Control Change Data (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1011", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Control Change Message", 2, group, status=status, index=index, data=data)

    def midi1_0_program_change(program:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Program Change Message

        Parameters
        ----------
        program : int
          Program Number (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        data = program << 8
        status = int("1100", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Program Change Message", 2, group, status=status, data=data)

    def midi1_0_channel_pressure(data:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Channel Pressure Message (Channel Aftertouch)

        Parameters
        ----------
        data : int
          Channel Pressure Data (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        data = data << 8
        status = int("1101", 2) << 4 | int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Channel Pressure Message", 2, group, status=status, data=data)

    def midi1_0_pitch_bend(lsb_data:int, msb_data:int, group:int=0, channel:int=0):
        """
        MIDI 1.0 Pitch Bend Message

        Parameters
        ----------
        lsb_data : int
          Least Significant Byte of Pitch Bend Data (7 bits)
        msb_data : int
          Most Significant Byte of Pitch Bend Data  (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        data = int(lsb_data) << 8 | int(msb_data)
        status = int("1110", 2)
        ch = int(channel)
        return UniversalMIDIPacket("MIDI 1.0 Pitch Bend Message", 2, group, status << 4 | ch, data=data)
        
    def midi2_0_note_off(note_num:int, vel:int, atribute_type:int=0, atribute_data:int=0, group:int=0, channel:int=0):
        """
        MIDI 2.0 Note Off Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        vel : int
          Note Velocity (16 bits)
        attribute_type : int, optional
          Atribute Type (8 bits), Default: 0 for no Attribute Type
        attribute_data : int, optional
          Attribute Data (16 bits), Default: 0 for no Attribute Data
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('1000', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(atribute_type)
        data = int(vel) << 16 | int(atribute_data) 
        return UniversalMIDIPacket("MIDI 2.0 Note Off Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_note_on(note_num: int, vel:int, atribute_type:int=0, atribute_data:int=0, group:int=0, channel:int=0):
        """
        MIDI 2.0 Note On Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        vel : int
          Note Velocity (16 bits)
        attribute_type : int, optional
          Atribute Type (8 bits), Default: 0 for no Attribute Type
        attribute_data : int, optional
          Attribute Data (16 bits), Default: 0 for no Attribute Data
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('1001', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(atribute_type)
        data = int(vel) << 16 | int(atribute_data)
        return UniversalMIDIPacket("MIDI 2.0 Note On Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_poly_pressure(note_num:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Poly Pressure Message (Polyphonic Aftertouch)

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        data : int
          Poly Pressure Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('1010', 2) << 4 | int(channel)
        index = int(note_num) << 8
        return UniversalMIDIPacket("MIDI 2.0 Poly Pressure Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_reg_per_note(note_num:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Registered Per-Note Controller Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        index : int
          RPNC Index (8 bits)
        data : int
          RPNC Message Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('0000', 2) << 4 | int(channel)
        index = int(note_num) << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Registered Per-Note Controller Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_asn_per_note(note_num:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Assignable Per-Note Controller Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        index : int
          APNC Index (8 bits)
        data : int
          APNC Message Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('0001', 2) << 4 | int(channel)
        index = int(note_num) << 8 | int(index)
        return UniversalMIDIPacket("MIDI 2.0 Assignable Per-Note Controller Message", 4, group, status=status, index=index, 
                                    data=data)

    def midi2_0_per_note_management(note_num:int, d:int, s:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Per-Note Management Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        d : int
          Detach (1 bit)
          When set, all currently playing notes and previous notes on 
          Note Number no longer respond to Per-Note Controllers.
          Currently playing notes mantain current value of Per-Note Controllers.
        s : int
          reSet (1 bit)
          When set, all per-note controllers on Note Number are reset to 
          their default values
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int('1111', 2) << 4 | int(channel)
        index = int(note_num) << 8 | d << 1 | s
        return UniversalMIDIPacket("MIDI 2.0 Per-Note Management Message", 4, group, status=status, index=index, data=0)

    def midi2_0_cc(index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Control Change Message

        Parameters
        ----------
        index : int
          Control Change Number Index (7 bits)
        data : int
          Control Change Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1011", 2) << 4 | int(channel)
        index = index << 8
        return UniversalMIDIPacket("MIDI 2.0 Control Change Message", 4, group, status=status, index=index, data=data)

    def midi2_0_reg_controller(bank:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Registered Controller Message (RPN)

        Parameters
        ----------
        bank : int
          Bank or RPN Most Significant Byte (7 bits)
        index : int
          Index or RPN Least Significat Byte (7 bits)
        data : int
          RPN Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("0010", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Registered Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_asn_controller(bank:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Assignable Controller Message (NRPN)

        Parameters
        ----------
        bank : int
          Bank or NRPN Most Significant Byte (7 bits)
        index : int
          Index or NRPN Least Significat Byte (7 bits)
        data : int
          RPN Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("0011", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Assignable Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_rel_reg_controller(bank:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Relative Registered Controller Message (RPN)

        Parameters
        ----------
        bank : int
          Bank or RPN Most Significant Byte (7 bits)
        index : int
          Index or RPN Least Significat Byte (7 bits)
        data : int
          RPN Data (32 bits)
          Two's compliment to provide positive and negative control of the destination value
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("0100", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Relative Registered Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_rel_asn_controller(bank:int, index:int, data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Relative Assignable Controller Message (NRPN)

        Parameters
        ----------
        bank : int
          Bank or NRPN Most Significant Byte (7 bits)
        index : int
          Index or NRPN Least Significat Byte (7 bits)
        data : int
          NRPN Data (32 bits)
          Two's compliment to provide positive and negative control of the destination value
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("0101", 2) << 4 | int(channel)
        index = bank << 8 | index
        return UniversalMIDIPacket("MIDI 2.0 Relative Assignable Controller Message", 4, group, status=status, index=index, data=data)

    def midi2_0_program_change(program:int, b:int=0, bank_msb:int=0, bank_lsb:int=0, group:int=0, channel:int=0):
        """
        MIDI 2.0 Program Change Message

        Parameters
        ----------
        program : int
          Program Number (7 bits)
        b : int
          Bank Valid Bit (1 bit)
          When set, Bank Select operation is perfomed first, then Program Change
        bank_msb : int
          Most Significant Byte Bank Select Data (7 bits)
        bank_lsb : int
          Least Significant Byte Bank Select Data (7 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1100", 2) << 4 | int(channel)
        index = b
        data = program << 24 | bank_msb << 8 | bank_lsb
        return UniversalMIDIPacket("MIDI 2.0 Program Change Message", 4, group, status=status, index=index, data=data)
    
    def midi2_0_channel_pressure(data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Channel Pressure Message

        Parameters
        ----------
        data : int
          Channel Pressure Data (32 bits)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1101", 2) << 4 | int(channel)
        index = 0
        return UniversalMIDIPacket("MIDI 2.0 Channel Pressure Message", 4, group, status=status, index=index, data=data)
    
    def midi2_0_pitch_bend(data:int, group:int=0, channel:int=0):
        """
        MIDI 2.0 Pitch Bend Message

        Parameters
        ----------
        data : int
          Pitch Bend Data (32 bits)
          centered at 0x80000000 (2147483648)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("1110", 2) << 4 | int(channel)
        index = 0
        return UniversalMIDIPacket("MIDI 2.0 Pitch Bend Message", 4, group, status=status, index=index, data=data)

    def midi2_0_per_note_pitch_bend(note_num:int, data:int, group=0, channel=0):
        """
        MIDI 2.0 Per-Note Pitch Bend Message

        Parameters
        ----------
        note_num : int
          Note Number (7 bits)
        data : int
          Pitch Bend Data (32 bits)
          centered at 0x80000000 (2147483648)
        group : int, optional
          Group (4 bits) default: group 1
        channel : int, optional
          Channel (4 bits) default: channel 1
        """
        status = int("0110", 2) << 4 | int(channel)
        index = int(note_num) << 8
        return UniversalMIDIPacket("MIDI 2.0 Per-Note Pitch Bend Message", 4, group, status=status, index=index, data=data)
    
    def system_exclusive_7bit(status:int, num_bytes:int, data_list:list, group:int=0):
        """
        System Exclusive (7 bit) Message

        Parameters
        ----------
        status: int
          Determines the role of the UMP in the System Exclusive Message
          0: Complete System Exclusive Message in one UMP
          1: System Exclusive Start UMP
          2: System Exclusive Continue UMP
          3: System Exclusive End UMP

        num_bytes: int
          Number of bytes through the end of the current UMP
          (integer between 0 and 6)

        data_list: list
          List of data bytes (7bits per byte)

        group: int, optional
          Group (4bits), default: group 1
        """
        data = 0
        shift = 0
        for b in data_list:
            data = int(b) << shift | data
            shift += 8
        data = data << (48-shift)
        return UniversalMIDIPacket("System Exclusive (7-Bit) Message", 3, group, status<<4|num_bytes, data=data)
    
    def system_exclusive_8bit(status:int, num_bytes:int, data_list:list, stream_id:int=0, group:int=0):
        """
        System Exclusive 8 (8 bit) Message

        Parameters
        ----------
        status: int
          Determines the role of the UMP in the System Exclusive Message
          0: Complete System Exclusive 8 Message in one UMP
          1: System Exclusive 8 Start UMP
          2: System Exclusive 8 Continue UMP
          3: System Exclusive 8 End UMP

        num_bytes: int
          Number of bytes through the end of the current UMP
          includes the stream_id byte
          (integer between 1 and 14)

        data_list: list
          List of data bytes (8bits per byte)

        stream_id: int, optional
          if the device supports multiple simultaneous System Exclusive 8 messages
          stream_id denotes the specific stream that this messages is sent and received by

        group: int, optional
          Group (4bits), default: group 1
        """
        data = 0
        shift = 0
        for b in data_list:
            data = int(b) << shift | data
            shift += 8
        data = data << ((13*8)-shift)
        return UniversalMIDIPacket("System Exclusive 8 (8-bit)", 5, group, status<<4|num_bytes, data=stream_id << 104 | data)