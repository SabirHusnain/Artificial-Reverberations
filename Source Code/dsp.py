# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:25:17 2023

@author: sabir
"""


import thinkdsp
import thinkplot
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter


def plot_magnitude_spectrum(wave, axis=None, start=0, duration=10, peakFreq=10000):
    """
    Plot magnitude spectrun of thinkdsp.Wave object

    Args:
        wave (thinkdsp.Wave): Input wave
        start (int): Start time in seconds
        duration (int): Duraction time in seconds
        peakFreq (float): Peak Frequency to be shown in plot

    Returns:
        None
    """

    segment = wave.segment(start, duration)
    spectrum = segment.make_spectrum()
    if not axis == None:
        spectrum_magnitude = spectrum.amps
        frequencies = spectrum.fs
        axis.plot(frequencies, spectrum_magnitude)
        axis.set_xlim(0, peakFreq)
    else:
        spectrum.plot(high=peakFreq)
        thinkplot.config(xlabel='Frequency (Hz)')
        thinkplot.show()


def comb_filter(signal, delay, decay=10000, plot=False, time=10):
    """
    comb_filter - Apply a comb filter (Deprecated)

    Args:
        signal (np.ndarray): Signal array.
        delay (float): Delay in seconds.
        decay (float, optional): Decay factor for output signal. Default is 10000.
        plot (bool, optional): Show plots. Default is False.
        time (int, optional): Signal total time in seconds. Default is 10.

    Returns:
        filtered_signal (np.ndarray): Fitlered output signal.
    """

    # Generate a sample signal
    fs = 44100  # Sampling frequency (Hz)
    t = np.linspace(0, time, num=fs*time)  # Time vector

    # Design a comb filter
    num_samples_delay = int(delay * fs)  # Number of samples for delay
    b = np.zeros(num_samples_delay + 1)  # Filter coefficients
    b[0] = 1  # Delay line
    b[num_samples_delay] = decay  # Decay factor

    # Apply the comb filter to the signal
    filtered_signal = lfilter(b, 1, signal)

    filtered_signal = filtered_signal/(decay+1)

    # Plot the original signal and the filtered signal
    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(t, signal, label='Original Signal')
        plt.plot(t, filtered_signal, label='Filtered Signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.title(f'Comb Filter Output with K = {delay}ms')
        plt.show()

    return filtered_signal


def generate_comb_filter_coefficients(delay, gain):
    """
    generate_comb_filter_coefficients - Generate coefficients for a comb filter.

    Args:
        delay (int): Delay length in samples.
        gain (float): Feedback gain.

    Returns:
        b (np.ndarray): Feedforward coefficients.
        a (np.ndarray): Feedback coefficients.
    """

    b = np.zeros(delay)
    b[0] = 1
    a = np.zeros(delay)
    a[0] = 1
    a[delay-1] = -gain
    return b, a

# Function to generate allpass filter coefficients


def generate_allpass_filter_coefficients(delay, gain):
    """
    generate_allpass_filter_coefficients - Generate coefficients for an allpass filter.

    Args:
        delay (int): Delay length in samples.
        gain (float): Feedback gain.

    Returns:
        b (np.ndarray): Feedforward coefficients.
        a (np.ndarray): Feedback coefficients.
    """

    b = np.zeros(delay)
    b[0] = gain
    b[delay-1] = 1
    a = np.zeros(delay)
    a[0] = 1
    a[delay-1] = gain
    return b, a


def apply_comb_filter(x, delay, gain):
    """
    apply_comb_filter - Apply a comb filter to an input signal.

    Args:
        x (np.ndarray): Input signal.
        delay (int): Delay length in samples.
        gain (float): Feedback gain.

    Returns:
        y (np.ndarray): Output signal.
    """

    b, a = generate_comb_filter_coefficients(delay, gain)
    y = np.convolve(x, b)-np.convolve(x, a)
    return y


def apply_allpass_filter(x, delay, gain):
    """
    apply_allpass_filter - Apply an allpass filter to an input signal.

    Args:
        x (np.ndarray): Input signal.
        delay (int): Delay length in samples.
        gain (float): Feedback gain.

    Returns:
        y (np.ndarray): Output signal.
    """

    b, a = generate_allpass_filter_coefficients(delay, gain)
    y = np.convolve(x, b) - np.convolve(x, a)
    return y


def schroeder_reverberator(x, sr, rt60):
    """
    schroeder_reverberator - Apply Schroeder's Reverberator Network to an input signal.

    Args:
        x (np.ndarray): Input signal.
        sr (int): Sample rate in Hz.
        rt60 (float): Reverberation time in seconds.

    Returns:
        y (np.ndarray): Output signal.
    """

    delay_times = [int(sr * t)
                   for t in [0.0297/100, 0.0371/100, 0.0411/100, 0.0437/100]]
    gain_values = [10**(-3 * t / (sr * rt60)) for t in delay_times]

    y = np.copy(x)
    for delay, gain in zip(delay_times, gain_values):
        y = apply_comb_filter(y, delay, gain)
    for delay, gain in zip(delay_times, gain_values):
        y = apply_allpass_filter(y, delay, gain)

    return y
