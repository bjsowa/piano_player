#!/home/blazej/.virtualenv/python3.6/bin/python

import pygame

from midi_input import MidiInput

midi = MidiInput()
pygame.display.init()

size = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode( size, pygame.FULLSCREEN )
pygame.mouse.set_visible( False )

midi.start()

exit = False
clock = pygame.time.Clock()

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True

    clock.tick(60)

midi.end = True
midi.join()
midi.close()
pygame.display.quit()