from os import listdir, path
from pygame import midi, mixer
from keyboard_input import KeyboardInput

def MidiInit():
    # pygame inits
    mixer.pre_init(44100, -16, 2, 256)
    mixer.init()
    midi.init()

    # wypisywanie listy urządzeń wejściowych
    input_devices = [-1]
    print( '[0] Klawiatura' )
    for x in range( midi.get_count() ):
        dev_info = midi.get_device_info(x)
        if dev_info[2] == 1:
            input_devices.append(x)
            print( '[{}]'.format(len(input_devices)-1), dev_info[1].decode('utf-8') )

    default_device = len(input_devices)-1

    # wybieranie urządzenia wejściowego
    try:
        dev = int(input( "Wybierz urządzenie wejściowe [" + str(default_device) + "]: " ))
    except ValueError:
        dev = default_device
    if dev >= len(input_devices) or dev < 0:
        print( 'Nieprawidłowy numer urządzenia! Wybrano domyślne.' )
        dev = default_device

    # inicjalizacja urzadzenia
    inputs = []
    dev_nr = input_devices[dev]
    if dev_nr == -1:
        inputs.append(KeyboardInput())
        inputs[0].start()
    else:
        inputs.append(midi.Input(dev_nr))

    # wypisywanie dostępnych sampli
    dirlist = listdir('./samples')
    samples = []
    for dirname in dirlist:
        if path.isdir('./samples/' + dirname):
            samples.append(dirname)
            print( '[{}]'.format(len(samples)-1), dirname )
    
    default_samples = len(samples)-1

    # wybieranie sampli
    try:
        samples_nr = int(input( "Wybierz sample dźwiękowe [" + str(default_samples) + "]: " ))
    except ValueError:
        samples_nr = default_samples
    if samples_nr >= len(samples) or samples_nr < 0:
        samples_nr = default_samples

    samples_path = './samples/' + samples[samples_nr]

    # inicjalizacja plików dźwiękowych
    sounds = [{},{}]
    for sample_name in listdir(samples_path):
        name, ext = path.splitext(sample_name)
        if ext == '.wav':
            try:
                it = int(name)
            except:
                continue
            sounds[0][it] = mixer.Sound( samples_path + '/' + sample_name )
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

    return inputs,sounds,sustain

def MidiQuit():
    midi.quit()
    mixer.quit()