# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:25:17 2023

@author: sabir
"""


import numpy as np
import utilities as utils
import dsp
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # utils.record_audio(fileName='output.wav')
    # utils.play_audio_file(fileName='output.wav')
    # dsp.plot_magnitude_spectrum(wave=wave,peakFreq=8000)
    time, dataLength, wave = utils.read_audio_file('data/Record_1.wav')

    '''
    delays=[31.25E-3, 62.50E-3, 93.75E-3, 125.0E-3, 156.25E-3, 187.50E-3]
    delays = [1.0E-3, 2.0E-3, 3.0E-3, 4.0E-3, 5.0E-3]
    sig = np.zeros((dataLength, len(delays)+1))
    for i, j in enumerate(delays):
        sig[:, i] = dsp.comb_filter(signal=wave.ys, delay=j, plot=False)
    sig[:, -1] = np.sum(sig, axis=1)
    '''

    output = dsp.schroeder_reverberator(wave.ys, dataLength/time, 0.1)

    newWave = utils.make_wave(signal=output, fs=dataLength/time)

    fig = plt.figure(figsize=(8, 6), dpi=80)

    dsp.plot_magnitude_spectrum(wave=wave, fig=fig, peakFreq=8000)
    dsp.plot_magnitude_spectrum(wave=newWave, peakFreq=8000)

    # utils.make_audio_file(newWave, 'output2.wav')

    print('EOF')
