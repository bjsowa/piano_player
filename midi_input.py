import pygame as pg

from pygame import midi, mixer
from threading import Thread

from midi_init import MidiInit, MidiQuit

NOTE_ON = 144
NOTE_OFF = 128

class Note:
    def __init__(self, note):
        self.type = note[0][0]
        self.pitch = note[0][1]
        self.velocity = note[0][2]
        self.timestamp = note[1]
        if self.type == NOTE_ON and self.velocity == 0:
            self.type = NOTE_OFF

class MidiInput(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.inputs, self.sounds, self.sustain = MidiInit()
        self.end = False

    def run(self):
        # wywalenie śmieci
        for inp in self.inputs:
            if inp.poll():
                notes = inp.read(50)

        while not self.end:
            for player, inp in enumerate(self.inputs):
                if inp.poll():
                    notes = inp.read(10)
                    for x in notes:
                        note = Note(x)
                        if note.type == NOTE_ON:
                            event = pg.event.Event( pg.USEREVENT, 
                                { 'NoteOn': True, 'NoteOff': False, 'Pitch': note.pitch, 'Player': player } )
                            pg.event.post(event)
                            if note.pitch in self.sounds:
                                self.sounds[note.pitch].set_volume( float(note.velocity) / 127.0 )
                                self.sounds[note.pitch].play()
                        elif note.type == NOTE_OFF:
                            event = pg.event.Event( pg.USEREVENT, 
                                { 'NoteOn': False, 'NoteOff': True, 'Pitch': note.pitch, 'Player': player } )
                            pg.event.post(event)
                            if note.pitch in self.sounds:
                                self.sounds[note.pitch].fadeout(self.sustain)
                    #print( notes)
            pg.time.wait(10)

    def close(self):
        for inp in self.inputs:
            inp.close()
        del self.sounds, self.sustain
        MidiQuit()
