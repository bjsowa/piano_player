import pygame as pg

from pygame import midi
from threading import Thread
from queue import Queue

class Note:
    def __init__(self, note):
        self.type = note[0][0]
        self.pitch = note[0][1]
        self.velocity = note[0][2]
        self.timestamp = note[1]
        if self.type == NOTE_ON and self.velocity == 0:
            self.type = NOTE_OFF


class PianoAI(Thread):
    def __init__(self, output, notes):
        Thread.__init__(self)
        self.output = output
        self.notes = notes
        self.noteList = []
        self.end = False

    def run(self):
        while not self.end:
            try:
                note = self.notes.get(block = False)
            except:
                pg.time.wait(10)
                continue

            self.noteList.append(note)
            #print( note )

    def send_notes(self):
        if len(self.noteList) > 0:
            ticks = pg.time.get_ticks()
            offset = self.noteList[0][1]
            for note in self.noteList:
                note[1] += ticks - offset
            self.output.write(self.noteList)
            self.noteList = []