import pickle
import numpy as np
import wavio
from glob import glob

path = "/Users/seva/biohack/data/soundAnalysis/data/22-03-16-CS-agn-n-AD7/*/*.wav"

files = glob(path)

cutted_wav = []
song_type = []
file_names = []

print "Files = ", len(files)
i = 0

for file in files:
    i += 1
    print i

    fname = file[:-4]
    with open(fname + ".wav") as f:
        rate, sampwidth, wav = wavio.readwav(f)

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

