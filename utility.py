import argparse
from scipy.io import wavfile
from model import load_model, predict
from muha import information_about_pulse_song, information_about_sine_song
from find_all_songs import find_all_songs
import pickle
from server import start_server


def make_prediction(samples):
    model = load_model('model.pickle')
    prediction = predict(model, samples)
    return prediction


def process_file(file_name):
    sample_rate, samples = wavfile.read(file_name)
    segments_sin, segments_pulse = make_prediction(samples)
    song_p = find_all_songs(segments_pulse)
    info_sin = information_about_sine_song(segments_sin, samples, sample_rate)
    info_pulse = information_about_pulse_song(song_p, samples, sample_rate)
    return {
        'samples': samples,
        'info_sin': info_sin,
        'info_pulse': info_pulse,
        'rate': sample_rate,
        'segments_sin': segments_sin,
        'segments_pulse': segments_pulse,
        'file_name': file_name
    }


def create_pickle_file(data, file_name, out_file=None):
    if not out_file:
        out_file = file_name + '.pickle'
    with open(out_file, 'wb') as fl:
        pickle.dump(data, fl)
    return out_file


def create_base_file(data, file_name, out_file=None):
    if not out_file:
        out_file = file_name + '.6'
    with open(out_file, 'w') as fl:
        all_segments = [('S', segment[0], segment[1]) for segment in data['segments_sin']] + \
                       [('P', segment[0], segment[1]) for segment in data['segments_pulse']]
        for segment in all_segments:
            fl.write('{} {} {}\n'.format(*segment))
    return out_file


def load_pickle_data(file_name):
    with open(file_name, 'rb') as fl:
        return pickle.load(fl)


def main():
    parser = argparse.ArgumentParser(description='File name')

    parser.add_argument('-inp')
    parser.add_argument("--pickle_load", action="store_true")
    parser.add_argument("--pickle_save", action="store_true")
    parser.add_argument("--base_save", action="store_true")
    parser.add_argument("--server_off", action="store_true")
    parser.add_argument('-out', default=None)

    args = parser.parse_args()

    if args.pickle_load:
        data = load_pickle_data(args.inp)
    else:
        data = process_file(args.inp)

    print('Loaded {} chunks'.format(len(data['samples'])))

    if args.pickle_save:
        out = create_pickle_file(data, args.inp, args.out)
        print('Saved pickle file in', out)

    if args.base_save:
        out = create_base_file(data, args.inp, args.out)
        print('Saved base file in', out)

    if not args.server_off:
        print('Starting server')
        start_server(data)


if __name__ == '__main__':
    main()
