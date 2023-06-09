# DSP: Artificial Reverberations

DSP: Artificial Reverberations is a Python application that allows you to record audio, apply artificial reverberation processing, and play the processed audio. It provides a graphical user interface (GUI) built with PyQt5 and utilizes various digital signal processing (DSP) techniques.


## Features

- Open and play audio files (WAV format).
- Record audio with customizable recording time and sampling frequency.
- Apply artificial reverberation processing to audio files using the Schroeder reverberator algorithm.
- Adjust the delay time and decay factor of the reverberation effect.
- Visualize the magnitude spectrum of the original and processed audio signals.
- Save the processed audio as a WAV file.
- Play the original and processed audio files.


## Prerequisites

- Python 3.6 or above
- PyQt5
- NumPy
- SciPy
- Matplotlib


## Installation

1. Clone the repository:
   git clone https://github.com/sabirhusnain577/Artificial-Reverberations.git
   
2. Install the required dependencies using pip:
   pip install pyqt5 numpy scipy matplotlib


## Usage

1. Run the 'main.py' file to start the application
2. Use the menu bar to open an audio file or record a new audio file.
3. Once an audio file is loaded or recorded, you can adjust the delay time and decay factor parameters.
4. Click the "Process Audio" button to apply the artificial reverberation effect to the audio.
5. The processed audio will be displayed in the right panel, and you can play it by clicking the "Play Processed Audio" button.