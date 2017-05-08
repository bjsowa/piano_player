#!/home/blazej/.virtualenv/python3.6/bin/python

import pygame

from midi_input import MidiInput

midi = MidiInput()
midi.start()

while True:
    try:
        print("CHUJ")
        pygame.time.wait(600)
    except KeyboardInterrupt:
        break

midi.end = True
midi.join()
midi.close()