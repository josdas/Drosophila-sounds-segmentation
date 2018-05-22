import numpy as np

WIN_LEN = 1500
PERCENTILE_COUNT = 7


def get_windows(arr):
    l = 0
    while l < len(arr):
        yield arr[l:l + WIN_LEN]
        l += WIN_LEN


def gen_features_way_1(x: np.array):
    x = x / np.abs(x).sum()
    features = [x.mean(), (x ** 2).mean(), x.var()]
    features += [np.percentile(x, p) for p in np.linspace(0, 100, PERCENTILE_COUNT)]
    return features


def gen_all_features(x: np.array):
    features = []
    features += gen_features_way_1(x)
    features += gen_features_way_1(np.abs(x))
    features += gen_features_way_1(np.abs(x[:-1] - x[1:]))
    features += gen_features_way_1(x * np.array(range(len(x))))
    return np.array(features)


def gen_features_name(pref):
    names = [pref + ' - mean', pref + ' - mean of squares', pref + ' - variance']
    names += [pref + ' - {:0.0f}th percentile'.format(p)
              for p in np.linspace(0, 100, PERCENTILE_COUNT)]
    return names


def gen_all_features_name():
    return gen_features_name('x') \
           + gen_features_name('|x|') \
           + gen_features_name('|x`|') \
           + gen_features_name('momentum')
