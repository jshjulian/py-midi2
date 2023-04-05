# Limitations of MIDI 1.0 and MPE

Since 1983, the Musicial Instrument Digital Interface (MIDI) protocol has enabled musical devices to communicate with each other and has allowed for creative possibilities such as sequencing and home recording in a quick and efficient way. However, due to the desire for simplicity in the specification as well as the technical limitations of the time, MIDI has its limitations.

- **Per Note Pitch Bend**
    
    Addressed by MIDI Polyphonic Expression (MPE) in 2018, the original MIDI specification does not support single note pitch bend, only pitch bends across an entire channel. This was remedied with MPE by putting different notes on different channels allowing up to 16 note polyphony which enables multidimensional controllers to control multiple parameters of each note. This allows for standard implementations of non-keyboard controllers such as MIDI guitars.

- **Keyboard Bias**

    MIDI was created to emulate sending piano information over a cable. While this is and has been the largest use case of MIDI, music that relies on notes outside of the western 12-tone equal temperament standard, music on stringed instruments, and any music made for non keyboard instruments are not well represented in the MIDI format. While non-keyboard MIDI controllers have been created, they are generally difficult to implement.

- **Controller Value Resolution**

    MIDI messages are sent in one, two, or three bytes. In these bytes, general the second and/or third byte encode data information about the message. The most significant bit for these bytes are set to 1, so for sending controller values, MIDI allows 7 bits of information (128 different values). While this is enough for encoding note numbers in the 12-tone standard and works for encoding volume information, when trying to encode something like a filter sweep from 100Hz to 10kHz, 128 values is just not enough.

- **Unidirectional Communication**

    MIDI is a one way communication protocol. This means that a MIDI controller has no information about the device that it is sending information to. Two way communication requires two MIDI cables and there is no standard for how two way communication would work in MIDI.

MIDI has been extended since it was intially proposed. General MIDI was established in 1991 to provide a standardized sound bank of 128 sounds including percussion instruments which are placed on channel 10 and standard note mapping which sets note number 60 to Middle C. General MIDI requires 24 note polyphony.

General MIDI 2 was developed in 1999. It increases polyphony to 32 notes, incorporates the MIDI Tuning Standard which allows for user-defined scales other than 12-tone equal temperament, and expands the set of additional sounds that General MIDI provided. General MIDI 2 also standardizes several CC numbers and RPNs such as sostenuto and soft pedal.

As mentioned previously, MIDI MPE was ratified in 2018 to enable per note expressive controls for pitch bend, velocity, and other dimensions of control for up to 16 notes across the 16 channels.

