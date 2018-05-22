import pickle
import numpy as np

from sound_processing.model.features import gen_all_features, get_windows, WIN_LEN


def load_model(file_name):
    with open(file_name, 'rb') as fl:
        return pickle.load(fl)


def predict(model, data):
    windows = get_windows(data)

    segments_s, segments_p = [], []

    ls = -np.inf

    probs = model.predict_proba([gen_all_features(win) for win in windows])

    i = 0
    left = None
    last_prediction = None

    for prob in probs:
        prob = dict(zip(model.classes_, prob))

        if prob['N'] > 0.15:
            prediction = 'N'
        else:
            prediction = 'S' if prob['S'] > prob['P'] else 'P'

        if prediction == 'S':
            ls = i
        if i - ls < 10000 and prob['S'] > 0.3:
            prediction = 'S'

        if prediction != 'N' and last_prediction != prediction:
            left = i
            last_prediction = prediction
        if prediction == 'N' and last_prediction:
            segment = (left, i)
            if last_prediction == 'S':
                segments_s.append(segment)
            else:
                segments_p.append(segment)
            last_prediction = None
        i += WIN_LEN

    return segments_s, segments_p
