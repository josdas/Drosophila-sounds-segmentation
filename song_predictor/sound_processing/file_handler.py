import pickle


def save(data, output_file=None, format='bin'):
    if format == 'bin':
        with open(output_file, 'wb') as fl:
            pickle.dump(data, fl)
        return output_file
    elif format == 'lab':
        all_segments = [('S', segment[0], segment[1]) for segment in data['segments_sin']]
        all_segments += [('P', segment[0], segment[1]) for segment in data['segments_pulse']]
        with open(output_file, 'w') as fl:
            for segment in all_segments:
                fl.write('{} {} {}\n'.format(*segment))
        return output_file
    else:
        raise ValueError("Unknown format")


def load_pickle_file(file_name):
    with open(file_name, 'rb') as fl:
        return pickle.load(fl)
