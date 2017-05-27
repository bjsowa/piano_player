from os import listdir, path
from pygame import midi, mixer

def MidiInit():
    # pygame inits
    mixer.pre_init(44100, -16, 2, 256)
    mixer.init()
    midi.init()

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
    try:
        dev = int(input( "Wybierz urządzenie wejściowe [" + str(it) + "]: " ))
    except ValueError:
        dev = it
    if dev not in dev_dic:
        dev = it

    # inicjalizacja urzadzeia 
    input_dev = midi.Input(dev_dic[dev])

    # wypisywanie dostępnych sampli
    dirlist = listdir('./samples')
    dir_dic = {}
    it = 0
    for dirname in dirlist:
        if path.isdir('./samples/' + dirname):
            it += 1
            dir_dic[it] = dirname
            print( '[{}]'.format(it), dirname )

    # wybieranie sampli
    try:
        samp = input( "Wybierz sample dźwiękowe [" + str(it) + "]: " )
    except ValueError:
        samp = it
    if samp not in dir_dic:
        samp = it

    samp_path = './samples/' + dir_dic[samp]

    # inicjalizacja plików dźwiękowych
    sounds = [{},{}]
    for samp_name in listdir(samp_path):
        name, ext = path.splitext(samp_name)
        if ext == '.wav':
            try:
                it = int(name)
            except:
                continue
            sounds[0][it] = mixer.Sound( samp_path + '/' + samp_name )
            sounds[1][it] = mixer.Sound( sounds[0][it] )

    # określanie pozostałych ustawień
    try:
        sustain = int(input( 'Podaj wartość sustain [200]: ' ))
    except ValueError:
        sustain = 200

    try:
        channels = int(input( 'Podaj ilość kanałów dźwiękowych [' + str(32) + ']: ' ))
    except ValueError:
        channels = 32

    mixer.set_num_channels(channels)

    return input_dev,sounds,sustain

def MidiQuit():
    midi.quit()
    mixer.quit()