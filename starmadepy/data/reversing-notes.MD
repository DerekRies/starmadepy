# Reversing Notes

Just some general notes I take as I go through the file types. Much of the file was already completed thanks to der_scheme on the starmade-dock forums.
[http://starmadedock.net/threads/the-starmade-template-file-format-smtpl.2994/](http://starmadedock.net/threads/the-starmade-template-file-format-smtpl.2994/)

also found this wiki page with some good info that would have been nice to find before I spent anytime trying to find this stuff out. [http://starmadepedia.net/wiki/Blueprint_File_Formats](http://starmadepedia.net/wiki/Blueprint_File_Formats)

Each block has:
 - 32bit int for x position
 - 32bit int for y position
 - 32bit int for z position
 - Orientation/Active Byte (4 bits orientation / 4 bits on-off)
 - 2 Bytes for Block ID (first byte last 2 bits is an offset)

## Orientation & active/inactive state bytes


grey wedge 01 -> 0x03
           02 -> 0x13
           03 -> 0x23
           04 -> 0x33
           05 -> 0x43
           06 -> 0x53
           07 -> 0x63
           08 -> 0x73
           09 -> 0x83
           10 -> 0x93
           11 -> 0xA3
           12 -> 0xB3

activation module off -> 0x08
                   on -> 0x00

white light off -> 0x08
             on -> 0x00

plex door open -> 0x09
        closed -> 0x01

plex door wedge 01 open -> 0x09
                 closed -> 0x01

plex door wedge 02 open -> 0x19
                 closed -> 0x11

plex door wedge 03 open -> 0x29
                 closed -> 0x21


First four bits seem to govern the rotation of the block while the last four
handle the active/inactive state.

Last Four Bits
Off = 8
On = 0
Open = 9
Closed = 1
Open = off + 1
Closed = on + 1

Rotation increments the first four bits by 1 each time, to a maximum of
12 (B in hex)

Now why is the last four bits equal to 3 in the grey wedge rotating case.
After some testing, everything still worked after changing the 3 to
different values. I guess it's disregarded for blocks that don't have an
on/off state.

Some cube shaped blocks, like thrusters, have orientations, and also an on/off state. (I don't think they, thrusters in this case, can be saved with an on state however. ex: 0x08 thuster block 01)

Blocks without orientation are technically still rotated in the engine, and stored as rotations. They just aren't rendered and give a message stating they have no orientation in the advanced build tool