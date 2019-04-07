import pygame as pg
from threading import Thread
from queue import Queue

NOTE_ON = 144
NOTE_OFF = 128

key_mapping = {
    pg.K_q: 48,
    pg.K_2: 49,
    pg.K_w: 50,
    pg.K_3: 51,
    pg.K_e: 52,
    pg.K_r: 53,
    pg.K_5: 54,
    pg.K_t: 55,
    pg.K_6: 56,
    pg.K_y: 57,
    pg.K_7: 58,
    pg.K_u: 59,
    pg.K_i: 60,
    pg.K_9: 61,
    pg.K_o: 62,
    pg.K_0: 63,
    pg.K_p: 64,
    pg.K_LEFTBRACKET: 65,
    pg.K_EQUALS: 66,
    pg.K_RIGHTBRACKET: 67,
    pg.K_z: 60,
    pg.K_s: 61,
    pg.K_x: 62,
    pg.K_d: 63,
    pg.K_c: 64,
    pg.K_v: 65,
    pg.K_g: 66,
    pg.K_b: 67,
    pg.K_h: 68,
    pg.K_n: 69,
    pg.K_j: 70,
    pg.K_m: 71,
    pg.K_COMMA: 72,
    pg.K_l: 73,
    pg.K_PERIOD: 74,
    pg.K_SEMICOLON: 75,
    pg.K_SLASH: 76
}

class KeyboardInput(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.end = False
        self.note_queue = Queue(maxsize=100)

    def run(self):

        # Wait for display init
        while not pg.display.get_init():
            pg.time.wait(100)

        while not self.end:
            for event in pg.event.get([pg.KEYDOWN, pg.KEYUP]):
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.event.post(pg.event.Event(pg.QUIT))
                    elif event.key in key_mapping:
                        note = [[NOTE_ON, key_mapping[event.key], 127, 0], 0]
                        self.note_queue.put(note)
                elif event.type == pg.KEYUP:
                    if event.key in key_mapping:
                        note = [[NOTE_OFF, key_mapping[event.key], 127, 0], 0]
                        self.note_queue.put(note)

            pg.time.wait(10)

    def poll(self):
        return not self.note_queue.empty()
    
    def read(self, num):
        notes = []
        for _ in range(num):
            if self.poll():
                notes.append(self.note_queue.get())
            else:
                break
        
        return notes

    def close(self):
        self.end = True