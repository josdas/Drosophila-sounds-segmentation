import argparse
from scipy.io import wavfile
from features import gen_all_features, get_windows, WIN_LEN
from model import load_model, predict
from muha import information_about_pulse_song, information_about_sine_song
from find_all_songs import find_all_songs


def make_prediction(samples):
    model = load_model('model.pickle')
    prediction = predict(model, samples)
    return prediction


def process_file(file_name):
    sample_rate, samples = wavfile.read(file_name)
    segments_s, segments_p = make_prediction(samples)
    song_p = find_all_songs(segments_p)
    inf_s = information_about_sine_song(segments_s, samples, sample_rate)
    inf_p = information_about_pulse_song(song_p, samples, sample_rate)


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
