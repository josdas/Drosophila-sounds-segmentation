import argparse

from scipy.io import wavfile
from sound_processing.model.model import load_model, predict
from sound_processing.file_handler import load_pickle_file, save
from sound_processing.processing.muha import information_about_pulse_song, information_about_sine_song
from sound_processing.processing.find_all_songs import find_all_songs
from frontend.server import start_server


def process_file(model, file_name, length=None):
    sample_rate, samples = wavfile.read(file_name)
    print('Wav loaded')

    if length:
        samples = samples[:length]
        print('Cut')

    segments_sin, segments_pulse = predict(model, samples)
    print('Segments predicted')

    song_p = find_all_songs(segments_pulse)
    print('All songs found')

    info_sin = [information_about_sine_song(segment_sin, samples, sample_rate)
                for segment_sin in segments_sin]
    print('Info about sin songs calculated')

    info_pulse = [information_about_pulse_song(song, samples, sample_rate)
                  for song in song_p]
    print('Info about pulse songs calculated')

    return {
        'samples': samples,
        'info_sin': info_sin,
        'info_pulse': info_pulse,
        'rate': sample_rate,
        'segments_sin': segments_sin,
        'segments_pulse': segments_pulse,
        'file_name': file_name
    }


def main():
    parser = argparse.ArgumentParser(description='File name')

    parser.add_argument('-input',
                        help='Path to *.wav file with recorder of songs')

    parser.add_argument("--server_off", action="store_true",
                        help='Flag to cancel server running\n'
                             'Set up if you do not want to run server')

    parser.add_argument("--bin_load", action="store_true",
                        help='Set up if you want to load result from binary file')

    parser.add_argument("--bin_save", action="store_true",
                        help='Set up if you want to save result as binary file')

    parser.add_argument("--lab_save", action="store_true",
                        help='Set up if you want to save result in laboratory format')

    parser.add_argument("-len", default=None, type=int,
                        help='Run program for prefix of file with length of "len"\n'
                             'This is special option for testing')

    parser.add_argument('-output', default=None,
                        help='Path to output')

    args = parser.parse_args()
    if args.bin_load:
        data = load_pickle_file(args.input)
    else:
        model = load_model('model.pickle')
        data = process_file(model, args.input, args.len)

    print('Loaded {} chunks'.format(len(data['samples'])))

    if args.bin_save:
        output_name = args.output | args.input + '.pickle'
        save(data, output_name, format='bin')
        print('Saved pickled file in', output_name)

    if args.lab_save:
        output_name = args.output | args.input + '.6'
        save(data, output_name, format='lab')
        print('Saved lab file in', output_name)

    if not args.server_off:
        print('Starting server')
        start_server(data)


if __name__ == '__main__':
    main()
