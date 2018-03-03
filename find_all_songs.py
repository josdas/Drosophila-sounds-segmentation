"""
Набор из некоторого числа коротких импульсов (щелчков).
Если интервал между импульсами меньше min_distance мс, то считается, что импульсы принадлежат одному периоду песни.
При интервале более min_distance мс импульсы трактуются как конец одного и начало нового периода песни.
"""


def find_all_songs(pulses, rate=44100, min_distance=80):
    # pulses - list(tuple)
    num_pulses = len(pulses)
    inter_puls = pulses[0]
    i = 0
    inter_res_songs = []
    song = []
    while i < num_pulses:
        # формируем массив с песней
        if pulses[i][0] - inter_puls[1] <= min_distance * rate:
            inter_res_songs.append(pulses[i])
        # если длина между > 80, делаем запись в Songs
        elif pulses[i] - inter_puls > min_distance * rate:
            song.append(list(inter_res_songs))
            arrInterLen = len(inter_res_songs)
            # очищаем массив от элементов
            del inter_res_songs[:arrInterLen]
            inter_res_songs.append(pulses[i])
        # обработка последнего списка
        if i == num_pulses - 1:
            song.append(list(inter_res_songs))
        inter_puls = pulses[i]
        i = i + 1
    return song
