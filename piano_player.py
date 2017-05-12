#!/home/blazej/.virtualenv/python3.6/bin/python

import pygame as pg

from midi_input import MidiInput
from keypad import Keypad

# inicjalizacja midi i ekranu
midi = MidiInput()
pg.display.init()

width = pg.display.Info().current_w
height = pg.display.Info().current_h
size = width, height

screen = pg.display.set_mode( size )
pg.mouse.set_visible( False )

# inicjalizacja klawiatury
keypad = Keypad( 'img/piano.png', width, 24 )

screen.blit( keypad, (keypad.offset,height - keypad.get_height()) )
pg.display.update()


# rozpoczęcie działania
midi.start()

exit = False
clock = pg.time.Clock()

while not exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit = True
        elif event.type == pg.USEREVENT:
            if event.NoteOn:
                keypad.NoteOn(event.Pitch)
            elif event.NoteOff:
                keypad.NoteOff(event.Pitch)

    screen.fill( (0,0,0) )
    keypad.NextFrame()
    screen.blit( keypad, (keypad.offset,height - keypad.get_height()) )
    pg.display.update()

    clock.tick(60)


# zakończenie działania
midi.end = True
midi.join()
midi.close()
pg.display.quit()