import pygame as pg

from pygame import Surface
from os import path
from ast import literal_eval

FADE_PERIOD = 5

def blit_alpha(target, source, location, opacity):
        x,y = location
        temp = Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class Key():
    def __init__(self, pitch, alpha, fadein: bool, fadeout: bool):
        self.pitch = pitch
        self.alpha = alpha
        self.fadein = fadein
        self.fadeout = fadeout

class Keypad(Surface):
    # offset, min_pitch, max_pitch, octave_width
    # keypad_surface, key_surfaces, key_pressed
    # key_info, rects
    def __init__(self, piano_path, keys_path, screen_width, min_pitch: int):
        min_pitch //= 12
        min_pitch *= 12
        self.min_pitch = min_pitch

        keypad_octave = pg.image.load(piano_path)
        octave_width, octave_heigh = keypad_octave.get_width(), keypad_octave.get_height()
        self.octave_width = octave_width
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

        self.key_surfaces = []
        self.key_info = []
        inf = open(path.join(keys_path, 'key_info'), 'r')
        for i in range(12):
            self.key_surfaces.append( pg.image.load( path.join(keys_path, str(i)+'.png')) )
            line = inf.readline()
            key_info.append( literal_eval(line) )

        self.Rects = []
        self.key_pressed = {}


    def NoteOn(self, pitch):
        if self.min_pitch <= pitch <= self.max_pitch:
            if pitch in self.key_pressed:
                self.key_pressed[pitch].fadein = True
                self.key_pressed[pitch].fadeout = False
            else:
                new_key = Key( pitch, 0, True, False )
                self.key_pressed[pitch] = new_key
            

    def NoteOff(self, pitch):
        if self.min_pitch <= pitch <= self.max_pitch:
            if pitch in self.key_pressed:
                self.key_pressed[pitch].fadein = False
                self.key_pressed[pitch].fadeout = True


    def NextFrame(self):
        to_delete = []
        self.blit( self.keypad_surface, (0,0) )
        for pitch, key in self.key_pressed.items():
            if key.fadein:
                if key.alpha < FADE_PERIOD:
                    key.alpha += 1
                if key.alpha == FADE_PERIOD:
                    key.fadein = False
            elif key.fadeout:
                key.alpha -= 1
                if key.alpha <= 0:
                    key.fadeout = False
                    to_delete.append(pitch)
                    continue
            octave_offset = ((pitch - self.min_pitch) // 12) * self.octave_width
            key_nr = pitch % 12
            alpha = int((255/FADE_PERIOD)*key.alpha)
            blit_alpha( self, self.key_surfaces[key_nr], (octave_offset,0), alpha )
            
        for p in to_delete:
            self.key_pressed.pop(p)
