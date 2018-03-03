import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal

def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def information_about_pulse_song(song, data, rate=44100):
    # song - [(l1,r1), (l2,r2), ...]
    # filename - path
    # TODO: classify peak by lineshape using correlation score

    # rate, data = wavfile.read(filename)
    
    number_of_pulses = len(song)
    l1, r1 = song[0]
    ll, rr = song[-1]
    song_duration = float(rr - l1) / rate

    distances = np.zeros(number_of_pulses - 1)
    energies = np.zeros(number_of_pulses)
    max_amps = np.zeros(number_of_pulses)
    for i in range(number_of_pulses):
        l1, r1 = song[i]
        l2, r2 = song[i+1]
        energies[i] = np.sum(data[l1:r1])
        max_amps[i] = np.max(np.absolute(data[l1:r1]))
        if i<number_of_pulses:
            distances[i] = (l2 - l1) * rate
    # distance_mean = np.mean(distances)
    # distance_std = np.std(distances)
    # energy_mean = np.mean(energies)
    # energy_std = np.std(energies)
    # max_amps_mean = np.mean(max_amps)
    # max_amps_std = np.std(max_amps)
    # return (number_of_pulses, song_duration, distances, energies, max_amps)
    return {    'number_of_pulses'  :number_of_pulses,
                'song_duration'     :song_duration,
                'distances'         :distances,
                'energies'          :energies,
                'max_amps'          :max_amps}

def information_about_sine_song(song, data, rate=44100):
    # song - [(l1,r1)]
    # filename - path
    # 1. Frequency
    # 2. Duration
    # 3. Amplitude modulation (period)

    # rate, data = wavfile.read(filename)
    l, r = song[0]

    song_duration = float(r - l) / rate

    N = r - l
    data_wf = data[l:r] * np.sin( np.pi * np.arange(0,N) / (N-1) )
    # np.savetxt('data.txt',data[l:r])
    # np.savetxt('data_wf.txt',data_wf)
    sp = np.fft.fft(data_wf,2**15)
    freqs = np.linspace(0,rate,len(sp))
    mag = np.sqrt(np.real(sp)**2+np.imag(sp)**2)

    i_100 = np.argmin(np.absolute(freqs - 100))
    i_250 = np.argmin(np.absolute(freqs - 250))

    mag_100_250 = mag[i_100:i_250]

    sine_freq = freqs[i_100 + np.argmax(mag_100_250)]
    period = 1/sine_freq

    n_periods = int(np.floor(song_duration/period))
    # print sine_freq, period, song_duration, n_periods
    am_time = np.linspace(0, period * n_periods, n_periods)
    am_amplitude = np.zeros(n_periods)
    for i in range(n_periods):
        am_amplitude[i] = np.sum(np.absolute(data[l+int(i*period*rate):l+int((i+1)*period*rate)]))
    # print am_time
    # print am_amplitude
    # np.savetxt('sp.txt',np.column_stack((freqs,mag)))
    return {    'song_duration' :song_duration,
                'sine_freq'     :sine_freq,
                'n_periods'     :n_periods,
                'am_time'       :am_time,
                'am_amplitude'  :am_amplitude}


