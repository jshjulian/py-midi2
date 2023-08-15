# A (hopefully) Simple Explanation of MIDI 2.0 and MPE

Since 1983, the Musicial Instrument Digital Interface (MIDI) protocol has enabled musical devices to communicate with each other and has allowed for creative possibilities such as sequencing and home recording in a quick and efficient way. Due to the desire for simplicity in the specification as well as the technical limitations of the time, MIDI has some limitations.

A major limitation MIDI controller manufacturers have run into is the limited amount of information that can be sent through MIDI (in an easy and efficient way). Limited ways to send information over MIDI leads to limited amount of sound that can be created from an instrument. For example if you create a MIDI controller that utilizes the pressure of a button press, the vertical position on the button when pressed, and the horizontal position, how can we send all of this information to be proccessed by MIDI to create interesting and expressive music.

For years, MIDI controllers such as Continuum from Hakan Audio, the EigenHarp from John Lambert, and the Linstrument from Roger Lin all use MIDI (and some other protocols) to make their controllers more expressive, but there was no standardized way to add dimensionality and expressivity to MIDI controllers.

In 2016 at NAMM, Roli taked about a standard which would allow for multi-dimensional polyphonic expression in MIDI controllers using what already exists in the MIDI specification and what has already been done in some MIDI controllers. The idea is to put different notes on different channels so that channel wide MIDI messages would affect each note as if it were a different instrument, allowing for features such as per note pitch bend or per note timbre modulation. And so, ratified in 2018, MPE (MIDI Polyphonic Expression) was added to the MIDI specification. When enabled, this allows for up to 16 note polyphony.

The introduction of MIDI 2.0 does not directly affect MPE. Since MIDI 2.0 is backwards compatible with MIDI 1.0, a device running MIDI MPE can send messages to a MIDI 2.0 device and those messages will be understood and processed just as they would if they were sent to a MIDI 1.0 device.

Devices running MPE could be updated to instead send MIDI 2.0 messages that accomplish the same thing that MPE accomplish, but without the 16 note polyphony limit. MIDI 2.0 has a message that allows for per note pitch bend (Status `0110`). An implementation of MPE in MIDI 2.0 could be created that would increase the polyphony limit to 256 due to the added Group field in MIDI 2.0 messages. This would require an updated MPE standard I believe.

Otherwise, a question is what UMP messages can be used to send multidimensional information over MIDI. The answer. 

**Attributes**


