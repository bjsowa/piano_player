from pygame import midi, mixer

def init():
    # pygame inits
    mixer.pre_init(44100, -16, 2, 256)
    mixer.init()
    midi.init()

    # inicjalizacja plików dźwiękowych
    sounds = {}
    for i in range(20,110):
        path = "piano_samples/" + str(i) + ".wav"
        sounds[i] = mixer.Sound( path )
     
    # wybieranie ilości urządzeń wejściowych
    try:
        dev_n = int(input( "Wybierz ilość urządzeń wejściowych[1-2] (domyślnie 1): " ))
    except ValueError:
        dev_n = 1
    if not 1 <= dev_n <= 2:
        dev_n = 1

    # wypisywanie listy urządzeń wejściowych
    dev_dic = {}
    it = 0
    for x in range( midi.get_count() ):
        dev_info = midi.get_device_info(x)
        if dev_info[2] == 1:
            it += 1
            dev_dic[it] = x
            print( '[{}]'.format(it), midi.get_device_info(x) )

    # wybieranie urządzeń wejściowych
    devs = []
    try:
        dev = int(input( "Wybierz urządzenie 1 (domyślnie " + str(it) + "): " ))
    except ValueError:
        dev = it
    if dev not in dev_dic:
        dev = it

    dev = dev_dic[dev]
    devs.append(dev)

    if dev_n == 2:
        try:
            dev = int(input( "Wybierz urządzenie 1 (domyślnie " + str(it) + "): " ))
        except ValueError:
            dev = it
        if dev not in dev_dic:
            dev = it

        dev = dev_dic[dev]
        devs.append(dev)

    # inicjalizacja urzadzeń wejściowych
    inputs = []
    for dev in devs:
        inputs.append( midi.Input(dev) )

    # określanie pozostałych ustawień
    try:
        sustain = int(input( 'Podaj wartość sustain (domyślnie 200): ' ))
    except ValueError:
        sustain = 200

    try:
        channels = int(input( 'Podaj ilość kanałów dźwiękowych (domyślnie 16): ' ))
    except ValueError:
        channels = 16

    mixer.set_num_channels(channels)

    return inputs,sounds,sustain

def quit():
    midi.quit()
    mixer.quit()