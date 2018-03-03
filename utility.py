import argparse
from scipy.io import wavfile
from model import load_model, predict
from muha import information_about_pulse_song, information_about_sine_song
from find_all_songs import find_all_songs
import pickle


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


def create_base_file(data, file_name, out_file=None):
    if not out_file:
        out_file = file_name + '.6'
    with open(out_file, 'w') as fl:
        all_segments = [('S', segment[0], segment[1]) for segment in data['segments_sin']] + \
                       [('P', segment[0], segment[1]) for segment in data['segments_pulse']]
        for segment in all_segments:
            fl.write('{} {} {}\n'.format(*segment))


def load_pickle_data(file_name):
    


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


if __name__ == '__main__':
    main()
