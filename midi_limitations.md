# Limitations of MIDI 1.0 and MPE

Since 1983, the Musicial Instrument Digital Interface (MIDI) protocol has enabled musical devices to communicate with each other and has allowed for creative possibilities such as sequencing and home recording in a quick and efficient way. However, due to the desire for simplicity in the specification as well as the technical limitations of the time, MIDI has its limitations.

One of the major limitations of MIDI is the lack of emotion and expressivity that comes from the lack of per note modulation since all notes in a channel are affected by pitch bend and CC changes. This is addressed with MIDI Polyphonic Expression (MPE) which enables per note pitch bend (up to 16 note polyphony) and multidimensional controllers to control multiple parameters of each note.

Another limiation of MIDI comes from the data format. Most MIDI messages are sent in two or three bytes where the first bit of the bytes containing data are locked only allowing a device to send 7 bits of information. These 7 bits can encode 128 different values which may be enough for convey different notes, works but might be lacking for convey all volume from pianissimo to fortissimo, and would not work for encoding a filter sweep from 100 Hz to 20,000 Hz.

With the 128 different values for pitch, MIDI was built for the 12-tone equal temperament scale which makes MIDI a difficult format to use for other scales or microtonal music.

In general, MIDI was built for keyboard like controllers and is difficult to implement on wind instruments, guitars, and other instruments (some of this is made easier with MPE).