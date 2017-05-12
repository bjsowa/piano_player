import pygame as pg

from pygame import Surface

class Keypad(Surface):
    # offset, min_pitch, max_pitch, keypad_surface
    def __init__(self, path, screen_width, min_pitch: int):
        min_pitch //= 12
        min_pitch *= 12
        self.min_pitch = min_pitch

        keypad_octave = pg.image.load(path)
        octave_width, octave_heigh = keypad_octave.get_width(), keypad_octave.get_height()
        octaves = int(screen_width / octave_width)
        self.offset = int( (screen_width - (octave_width*octaves))/2 )
        
        if self.offset > 0:
            octaves += 2
            self.offset -= octave_width
            self.min_pitch -= 12

        self.max_pitch = self.min_pitch + octaves*12 - 1

        self.keypad_surface = Surface(  (octaves*octave_width,octave_heigh) )
        Surface.__init__(self, (octaves*octave_width,octave_heigh) )

        for i in range(octaves):
            self.keypad_surface.blit( keypad_octave, (i*octave_width,0) )
        self.blit( self.keypad_surface, (0,0) )

    def NoteOn(self, pitch):
        pass

    def NoteOff(self, pitch):
        pass

    def NextFrame(self):
        self.blit( self.keypad_surface, (0,0) )