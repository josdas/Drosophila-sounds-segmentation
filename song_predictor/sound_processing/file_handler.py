import pickle


def parse_segments(file_name):
    with open(file_name, 'r') as fl:
        return [(int(data[1]), int(data[2]), data[0])
                for data in map(lambda s: s.strip().split(), fl)]


def save(data, file_name, out_file=None, format='bin'):
    if format == 'bin':
        if not out_file:
            out_file = file_name + '.pickle'
        with open(out_file, 'wb') as fl:
            pickle.dump(data, fl)
        return out_file
    elif format == 'lab':
        if not out_file:
            out_file = file_name + '.6'
        with open(out_file, 'w') as fl:
            all_segments = [('S', segment[0], segment[1]) for segment in data['segments_sin']] + \
                           [('P', segment[0], segment[1]) for segment in data['segments_pulse']]
            for segment in all_segments:
                fl.write('{} {} {}\n'.format(*segment))
        return out_file
    else:
        raise ValueError("Unknown format")


def save_in_pickle_file(data, file_name, out_file=None):
    return out_file


def save_in_lab_file(data, file_name, out_file=None):
    return out_file


def load_pickle_file(file_name):
    with open(file_name, 'rb') as fl:
        return pickle.load(fl)
