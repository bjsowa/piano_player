#!/home/blazej/.virtualenv/python3.6/bin/python

import sys
import pygame
from pygame import midi, mixer
 
pygame.mixer.pre_init(44100, -16, 2, 256)
mixer.init()
midi.init()
 
for x in range( midi.get_count() ):
	print( '[{}]'.format(x), midi.get_device_info(x) )



try:
	dev = int(input( "Wybierz urządzenie (domyślnie " + str(midi.get_count()-1) + "): " ))
except ValueError:
	dev = midi.get_count()-1

try:
	sustain = int(input( 'Podaj wartość sustain (domyślnie 200): ' ))
except ValueError:
	sustain = 200

try:
	channels = int(input( 'Podaj ilość kanałów dźwiękowych (domyślnie 16): ' ))
except ValueError:
	channels = 16

inp = midi.Input(dev)
mixer.set_num_channels(channels)

sound = {}
for i in range(20,110):
	path = "piano_samples/" + str(i) + ".wav"
	sound[i] = mixer.Sound( path )

while True:
	try:
		pygame.time.wait(10)
		if inp.poll():
			notes = inp.read(10)
			for note in notes:
				try:
					if note[0][0] == 144: # note on
						sound[note[0][1]].set_volume( float(note[0][2]) / 127.0 )
						sound[note[0][1]].play()
					elif note[0][0] == 128: # note off
						sound[note[0][1]].fadeout(sustain)
				except KeyError:
					continue
			print( notes )
	except KeyboardInterrupt:
		break

del inp
midi.quit()
mixer.quit()