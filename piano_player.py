import pygame as pg
import traceback

from midi_input import MidiInput
from keypad import Keypad

diatonic_color = (66,128,231)
chromatic_color = (59,101,151)

exit = False
clock = pg.time.Clock()

# inicjalizacja midi i ekranu
midi = MidiInput()
pg.display.init()

width = pg.display.Info().current_w
height = pg.display.Info().current_h
size = width, height

screen = pg.display.set_mode( size, pg.FULLSCREEN )
pg.mouse.set_visible( False )
background = (12,12,12)
screen.fill(background)
pg.display.update()

# inicjalizacja klawiatury
try:
    keypad = Keypad( 'img/piano.png', 'img/keys/', width, 24 )
except:
    traceback.print_exc()
    exit = True

screen.blit( keypad, (keypad.offset,height - keypad.get_height()) )
pg.display.update()

# rozpoczęcie działania
midi.start()

while not exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit = True
        elif event.type == pg.USEREVENT:
            try:
                if event.NoteOn:
                    keypad.NoteOn(event.Pitch, event.Player)
                elif event.NoteOff:
                    keypad.NoteOff(event.Pitch, event.Player)
            except:
                traceback.print_exc()
                exit = True

    try:
        keypad.NextFrame()
    except:
        traceback.print_exc()
        exit = True

    screen.fill( background )
    screen.blit( keypad, (keypad.offset, height - keypad.get_height()) )

    for rect in keypad.rects:
        if rect[1]:
            my_rect = rect[0].copy()
            my_rect.left += keypad.offset
            my_rect.top += height - keypad.get_height()
            pg.draw.rect( screen, rect[2], my_rect )
        
    for rect in keypad.rects:
        if not rect[1]:
            my_rect = rect[0].copy()
            my_rect.left += keypad.offset
            my_rect.top += height - keypad.get_height()
            pg.draw.rect( screen, rect[2], my_rect )

    pg.display.update()

    clock.tick(60)


# zakończenie działania
midi.end = True
midi.join()
midi.close()
pg.display.quit()