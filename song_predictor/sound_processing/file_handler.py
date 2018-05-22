import pickle


def save(data, output_file=None, format='bin'):
    if format == 'bin':
        with open(output_file, 'wb') as fl:
            pickle.dump(data, fl)
    elif format == 'lab':
        segments = [('S', segment[0], segment[1])
                    for segment in data['segments_sin']]
        segments += [('P', segment[0], segment[1])
                     for segment in data['segments_pulse']]
        with open(output_file, 'w') as fl:
            for segment in segments:
                fl.write('{} {} {}\n'.format(*segment))
    else:
        raise ValueError("Unknown format")


def load_pickle_file(file_name):
    with open(file_name, 'rb') as fl:
        return pickle.load(fl)
