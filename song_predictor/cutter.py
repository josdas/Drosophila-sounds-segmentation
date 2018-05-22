import pickle
import numpy as np
from scipy.io import wavfile
from glob import glob

path = "../soundAnalysis/data/data/*/*.wav"

files = glob(path)

cutted_wav = []
song_type = []
file_names = []

print ("Files = ", len(files))
i = 0

for file in files:
    i += 1
    print (i)

    fname = file[:-4]
    rate, wav =  wavfile.read(fname + ".wav")

    # get annotation
    with open(fname + ".6") as f:
        annotations = f.readlines()
    annotations = [x.strip() for x in annotations]

    # cut and append to cutted_wav
    for annotation in annotations:
        an_type, an_start, an_end = annotation.split()
        an_start = int(an_start)
        an_end = int(an_end)
        cutted_wav.append(wav[an_start:(an_end+1)])
        song_type.append(an_type)
        file_names.append(file)

to_dump = [(i,j,k) for i,j,k in zip(cutted_wav,song_type,file_names)]
with open( "cutted_wav.pickle", "wb" ) as f:
    pickle.dump(to_dump, f)

