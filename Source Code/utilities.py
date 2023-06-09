# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:25:17 2023

@author: sabir
"""


import pyaudio
import wave
import thinkdsp


def record_audio(fileName, recordTime=10, fs=44100):
    """
    record_audio - Record audio from the default system input device and save it as a WAV file.

    Args:
        fileName (str): The name of the WAV file to be saved.
        recordTime (int, optional): The duration of the recording in seconds. Default is 10 seconds.

    Returns:
        None
    """

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * recordTime)+1):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_audio_file(fileName):
    """
    play_audio_file - Play audio from a WAV file using the default system output device.

    Args:
        fileName (str): The name of the WAV file to be played.

    Returns:
        None
    """

    # Set chunk size of 1024 samples per data frame
    chunk = 1024

    # Open the sound file
    wf = wave.open(fileName, 'rb')

    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    p.terminate()


def read_audio_file(fileName):
    """
    read_audio_file - Read audio from a WAV file using the default system output device.

    Args:
        fileName (str): The name of the WAV file to be played.

    Returns:
        time (float): Time of audio signal in seconds.
        dataLength (int): Total length of signal.
        wave (thinkdsp.wave): Wave object for the sound signal
    """

    wave = thinkdsp.read_wave(fileName).segment(0, 10.0)
    dataLength = len(wave.ys)
    time = wave.duration
    return time, dataLength, wave


def make_wave(signal, fs):
    """
    make_wave - make_wave - Make thinkdsp.Wave object from sound signal

    Args:
        signal (np.ndarray): Signal array.
        fs (int): Sampling frequency.

    Returns:
        wave (thinkdsp.wave): Wave object for the sound signal
    """

    wave = thinkdsp.Wave(signal, framerate=fs)
    return wave


def play_audio(wave, chunk_size=1024):
    """
    play_audio - Play audio from a thinkdsp.Wave object in chunks using PyAudio.

    Args:
        wave (thinkdsp.Wave): The Wave object to be played.
        chunk_size (int): The number of samples per chunk. Default is 1024.

    Returns:
        None
    """

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a streaming stream
    stream = p.open(format=8,
                    channels=2,
                    rate=41100,
                    output=True)

    # Start the stream
    stream.start_stream()

    # Play the Wave samples in chunks
    num_chunks = len(wave) // chunk_size
    for i in range(num_chunks + 1):
        chunk_start = i * chunk_size
        chunk_end = (i + 1) * chunk_size
        chunk = wave.ys[chunk_start:chunk_end].tobytes()
        stream.write(chunk)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()


def make_audio_file(wave, fileName):
    """
    make_audio_file - Create audio file from sound signal.

    Args:
        wave (thinkdsp.Wave): The Wave object to be saved.
        fileName (string): Output file name.

    Returns:
        None
    """

    wave.normalize()
    wave.apodize()
    wave.write(fileName)
