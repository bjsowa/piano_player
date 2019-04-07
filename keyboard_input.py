import pygame as pg
from threading import Thread

class KeyboardInput(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.end = False

    def run(self):
        while not self.end:
            pg.time.wait(10)

    def poll(self):
        return False
    
    def read(self, num):
        pass

    def close(self):
        self.end = True