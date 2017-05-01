#!/home/blazej/.virtualenv/python3.6/bin/python

import sys
import pygame
from pygame import midi, mixer

from init import init,quit

inputs, sounds, sustain = init()

while True:
    try:
        pygame.time.wait(10)
        for inp in inputs:
            if inp.poll():
                notes = inp.read(10)
                for note in notes:
                    try:
                        if note[0][0] == 144: # note on
                            sounds[note[0][1]].set_volume( float(note[0][2]) / 127.0 )
                            sounds[note[0][1]].play()
                        elif note[0][0] == 128: # note off
                            sounds[note[0][1]].fadeout(sustain)
                    except KeyError:
                        continue
                print( notes )
    except KeyboardInterrupt:
        break

del inputs, sounds, sustain
quit()