from pygame import midi, mixer

def MidiInit():
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
        dev_n = int(input( "Wybierz ilość urządzeń wejściowych (1 lub 2) [1]: " ))
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
            print( '[{}]'.format(it), midi.get_device_info(x)[1].decode('utf-8') )

    # wybieranie urządzeń wejściowych
    input_devs = []
    try:
        dev = int(input( "Wybierz urządzenie 1 [" + str(it) + "]: " ))
    except ValueError:
        dev = it
    if dev not in dev_dic:
        dev = it

    input_devs.append(dev_dic[dev])
    del dev_dic[dev]

    if dev_n == 2 and len(dev_dic) != 0:
        if 1 in dev_dic:
            dev_def = 1
        else :
            dev_def = 2

        try:
            dev = int(input( "Wybierz urządzenie 2 [" +  str(dev_def) + "]: " ))
        except ValueError:
            dev = dev_def
        if dev not in dev_dic:
            dev = dev_def

        input_devs.append(dev_dic[dev])

    # # zapytanie o urządzenie wyjsciowe
    # output_devs = []
    # ans = input( "Czy dodać urządzenie wyjściowe (T/N) [N]: ")
    # if len(ans) > 0 and (ans[0] == 't' or ans[0] == 'T'):

    # # wypisywanie urządzeń wyjściowych
    #     dev_dic.clear()
    #     it = 0
    #     for x in range( midi.get_count() ):
    #         dev_info = midi.get_device_info(x)
    #         if dev_info[3] == 1:
    #             it += 1
    #             dev_dic[it] = x
    #             print( '[{}]'.format(it), midi.get_device_info(x)[1].decode('utf-8') )

    # # wybieranie urządzenia wyjściowego
    #     try:
    #         dev = int(input( "Wybierz urządzenie wyjściowe [" + str(it) + "]: " ))
    #     except ValueError:
    #         dev = it
    #     if not 1 <= dev <= it:
    #         dev = it 

    #     output_devs.append(dev_dic[dev])

    # inicjalizacja urzadzeń 
    inputs = []
    for dev in input_devs:
        inputs.append( midi.Input(dev) )
    # outputs = []
    # for dev in output_devs:
    #     outputs.append( midi.Output(dev, latency = 1000) )

    # określanie pozostałych ustawień
    try:
        sustain = int(input( 'Podaj wartość sustain [200]: ' ))
    except ValueError:
        sustain = 200

    try:
        channels = int(input( 'Podaj ilość kanałów dźwiękowych [16]: ' ))
    except ValueError:
        channels = 16

    mixer.set_num_channels(channels)

    return inputs,sounds,sustain

def MidiQuit():
    midi.quit()
    mixer.quit()