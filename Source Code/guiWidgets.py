# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:25:17 2023

@author: sabir
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
import webbrowser
import threading

import utilities as utils
import dsp


base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.stderr = open(os.path.join(base_path, 'stderr_log.txt'), 'w')
sys.stdout = open(os.path.join(base_path, 'stdout.txt'), 'w')


class Signal(QtCore.QObject):
    message_signal = QtCore.pyqtSignal(str)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.audio_file_loc = ''

        super(MainWindow, self).__init__()

        self.defUI()

        self.show()

        self.check_resources()

        self.signal = Signal()

        self.signal.message_signal.connect(self.show_message_box)

    def defUI(self):
        self.setGeometry(0, 0, 720, 480)  # Set the GUI size
        # self.setFixedSize(720, 480)
        # Set the GUI title
        self.setWindowTitle('DSP: Artificial Reverberations')
        icon = QtGui.QIcon(f'{base_path}/etc/artwork/dsp_icon.png')
        self.setWindowIcon(icon)
        QtWidgets.QApplication.setStyle(
            QtWidgets.QStyleFactory.create('Fusion'))  # Set the GUI look style
        self.add_menubar()
        self.add_sections()

    def add_menubar(self):
        """Add a menubar to the main UI. This controls all the buttons in the menubar"""

        # New participant button
        self.openFileAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(
                base_path, 'etc\\artwork', 'add_new_file_icon.png')), '&Open File', self)
        self.openFileAction.setStatusTip('Open Audio File')
        self.openFileAction.triggered.connect(self.getLoc_event)

        # drop down menu
        self.exitAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            base_path, 'etc\\artwork', 'close_icon.png')), '&Exit', self)
        self.exitAction.setStatusTip('Exit App')
        self.exitAction.triggered.connect(self.exit_event)

        # Choose storage location
        self.openDocsAction = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(
                base_path, 'etc\\artwork', 'documentation_icon.png')), '&Documentation', self)
        self.openDocsAction.setStatusTip('Open Documentation File')
        self.openDocsAction.triggered.connect(self.openDocs_Event)

        # Choose storage location
        self.openCodeAction = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(
                base_path, 'etc\\artwork', 'code_icon.png')), '&Code', self)
        self.openCodeAction.setStatusTip('Open Code Files')
        self.openCodeAction.triggered.connect(self.openCode_Event)

        # Choose storage location
        self.openAboutAction = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(
                base_path, 'etc\\artwork', 'about_me_icon.png')), '&About Me', self)
        self.openAboutAction.setStatusTip('About Author')
        self.openAboutAction.triggered.connect(self.openAbout_Event)

        # Add the menubar and the menu buttons
        menubar = self.menuBar()

        #        menubar.setFixedHeight(25)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openFileAction)
        fileMenu.addAction(self.exitAction)

        participantMenu = menubar.addMenu('&Help')
        participantMenu.addAction(self.openCodeAction)
        participantMenu.addAction(self.openDocsAction)
        participantMenu.addAction(self.openAboutAction)

        self.label = QtWidgets.QLabel("No File Opened!")
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.label.setMargin(5)
        self.label.setFixedWidth(600)
        menubar.setCornerWidget(self.label)

    def add_sections(self):
        # Create the vertical layout for the three sections
        layout = QtWidgets.QVBoxLayout()

        upper_section = QtWidgets.QWidget()
        upper_section_layout = QtWidgets.QHBoxLayout()
        upper_section.setLayout(upper_section_layout)

        lower_section = QtWidgets.QWidget()
        lower_section_layout = QtWidgets.QHBoxLayout()
        lower_section.setLayout(lower_section_layout)

        # Third section
        first_section = QtWidgets.QWidget()
        first_section_layout = QtWidgets.QVBoxLayout()
        first_section.setLayout(first_section_layout)

        open_file_button = QtWidgets.QPushButton("Open File")
        open_file_button.clicked.connect(self.getLoc_event)

        self.play_file_button = QtWidgets.QPushButton("Play File")
        self.play_file_button.clicked.connect(self.playFile_event)

        clear_all_button = QtWidgets.QPushButton("Clear All")
        clear_all_button.clicked.connect(self.clear_all_event)

        exit_button = QtWidgets.QPushButton("Exit")
        exit_button.clicked.connect(self.exit_event)

        first_section_layout.addWidget(open_file_button)
        first_section_layout.addWidget(self.play_file_button)
        first_section_layout.addWidget(clear_all_button)
        first_section_layout.addWidget(exit_button)

        # second section
        second_section = QtWidgets.QWidget()
        second_section_layout = QtWidgets.QVBoxLayout()
        second_section.setLayout(second_section_layout)

        self.recording_name_edit = QtWidgets.QLineEdit()
        self.recording_name_edit.setObjectName('Recording Name Text')
        self.recording_name_edit.setPlaceholderText('Enter Recording Name')

        self.recording_time_edit = QtWidgets.QLineEdit()
        self.recording_time_edit.setObjectName('Recording Time Text')
        self.recording_time_edit.setPlaceholderText(
            'Enter Recording Time (s, default = 10)')

        self.sampling_frequency_edit = QtWidgets.QLineEdit()
        self.sampling_frequency_edit.setObjectName('Sampling Frequency Text')
        self.sampling_frequency_edit.setPlaceholderText(
            'Enter Sampling Frequency (Hz, default = 44100)')

        self.record_button = QtWidgets.QPushButton("Record Audio")
        self.record_button.clicked.connect(self.record_audio_event)

        second_section_layout.addWidget(self.recording_name_edit)
        second_section_layout.addWidget(self.recording_time_edit)
        second_section_layout.addWidget(self.sampling_frequency_edit)
        second_section_layout.addWidget(self.record_button)

        # third section
        third_section = QtWidgets.QWidget()
        third_section_layout = QtWidgets.QVBoxLayout()
        third_section.setLayout(third_section_layout)

        self.delay_time_edit = QtWidgets.QLineEdit()
        self.delay_time_edit.setObjectName('Delay Time Text')
        self.delay_time_edit.setPlaceholderText('Enter Delay (s)')

        self.decay_factor_edit = QtWidgets.QLineEdit()
        self.decay_factor_edit.setObjectName('Decay Factor Text')
        self.decay_factor_edit.setPlaceholderText(
            'Enter Decay Factor (optional)')

        self.process_button = QtWidgets.QPushButton("Process Audio")
        self.process_button.clicked.connect(self.process_audio_event)

        self.play_processed_button = QtWidgets.QPushButton(
            "Play Processed Audio")
        self.play_processed_button.clicked.connect(self.play_processed_event)

        third_section_layout.addWidget(self.delay_time_edit)
        third_section_layout.addWidget(self.decay_factor_edit)
        third_section_layout.addWidget(self.process_button)
        third_section_layout.addWidget(self.play_processed_button)

        upper_section_layout.addWidget(first_section)
        upper_section_layout.addWidget(second_section)
        upper_section_layout.addWidget(third_section)

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.fig.subplots_adjust(left=0.075, right=0.95, bottom=0.15, top=0.9)
        self.defineSpectrums()

        lower_section_layout.addWidget(self.canvas)

        upper_section.setFixedHeight(140)

        layout.addWidget(upper_section)
        layout.addWidget(lower_section)

        # Set the central widget to be the vertical layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def exit_event(self):
        close_msg = 'Exit to Desktop?'
        reply2 = QtWidgets.QMessageBox.question(
            self, "Exit", close_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply2 == QtWidgets.QMessageBox.Yes:
            self.close()  # Quit Application.

    def getLoc_event(self):
        self.audio_file_loc, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', os.path.join(base_path, 'data'), '*.wav')
        self.label.setText(self.audio_file_loc)

    def openDocs_Event(self):
        try:
            webbrowser.open(os.path.join(
                base_path, 'etc\\docs\\documentation.pdf'))
        except:
            QtWidgets.QMessageBox.information(
                self, "Error", "Can't Open Documentation Files", QtWidgets.QMessageBox.Ok)

    def openCode_Event(self):
        try:
            webbrowser.open(os.path.join(
                base_path, 'etc\\docs\\code.pdf'))
        except:
            QtWidgets.QMessageBox.information(
                self, "Error", "Can't Open Documentation Files", QtWidgets.QMessageBox.Ok)

    def openAbout_Event(self):
        try:
            webbrowser.open(os.path.join(
                base_path, 'etc\\docs\\aboutme.pdf'))
        except:
            QtWidgets.QMessageBox.information(
                self, "Error", "Can't Open Documentation Files", QtWidgets.QMessageBox.Ok)

    def clear_all_event(self):
        self.clear('all')

    def record_audio_event(self):
        self.record_button.setEnabled(False)
        thread = threading.Thread(target=self.recordAudio)
        thread.start()

    def recordAudio(self):
        self.clear('prev_proc')
        startRecording = True

        if (self.recording_name_edit.text() == ''):
            self.signal.message_signal.emit('Error:Enter Valid File Name')
            startRecording = False
        else:
            self.audio_file_loc = os.path.join(
                base_path, f'data\\{self.recording_name_edit.text()}.wav')

        if (not self.recording_time_edit.text() == ''):
            if (not self.recording_time_edit.text().isnumeric()):
                self.signal.message_signal.emit(
                    'Error:Enter Valid Record Time')
                startRecording = False
            else:
                self.recordingTime = float(self.recording_time_edit.text())
        else:
            self.recordingTime = 10

        if (not self.sampling_frequency_edit.text() == ''):
            if (not self.sampling_frequency_edit.text().isnumeric()):
                self.signal.message_signal.emit(
                    'Error:Enter Valid Sampling Frequency')
                startRecording = False
            else:
                self.samplingFreq = float(self.sampling_frequency_edit.text())
        else:
            self.samplingFreq = 44100

        try:
            if startRecording:
                utils.record_audio(self.audio_file_loc,
                                   self.recordingTime, self.samplingFreq)

                self.signal.message_signal.emit('Info:Audio File Saved!')

                self.label.setText(self.audio_file_loc)
        except:
            self.signal.message_signal.emit('Error:Invalid Entry')
        
        self.record_button.setEnabled(True)

    def process_audio_event(self):
        self.process_button.setEnabled(False)
        thread = threading.Thread(target=self.processAudio)
        thread.start()

    def processAudio(self):
        startProcess = True

        if (not self.delay_time_edit.text() == ''):
            self.delayTime = float(self.delay_time_edit.text())
        elif self.audio_file_loc == '':
            self.signal.message_signal.emit('Error:Enter Valid Delay Time')
            startProcess = False

        if not self.decay_factor_edit.text() == '':
            if (not self.decay_factor_edit.text().isnumeric()):
                self.signal.message_signal.emit(
                    'Error:Enter Valid Decay Factor')
                startProcess = False
            else:
                self.decayFactor = self.decay_factor_edit.text()
        else:
            self.decayFactor = 10000

        if not self.audio_file_loc == '':
            self.audioTime, self.audioLength, self.audioWave = utils.read_audio_file(
                self.audio_file_loc)
        else:
            self.signal.message_signal.emit(
                'Error:Record or Load Audio Please')
            startProcess = False

        try:
            if startProcess:
                self.processedSignal = dsp.schroeder_reverberator(
                    self.audioWave.ys, self.audioLength/self.audioTime, self.delayTime)

                self.processedWave = utils.make_wave(
                    self.processedSignal, self.audioLength/self.audioTime)

                self.ax1.clear()
                self.ax2.clear()
                dsp.plot_magnitude_spectrum(
                    wave=self.audioWave, axis=self.ax1, peakFreq=8000)
                dsp.plot_magnitude_spectrum(
                    wave=self.processedWave, axis=self.ax2, peakFreq=8000)
                self.defineSpectrums()

                fileName = self.audio_file_loc.split('/')[-1]
                fileName, _ = os.path.splitext(fileName)
                self.processedFileName = f'{base_path}\\data\\{fileName}_processed.wav'
                utils.make_audio_file(
                    self.processedWave, self.processedFileName)
        except:
            self.signal.message_signal.emit('Error:Invalid Entry')
            
        self.process_button.setEnabled(True)

    def play_processed_event(self):
        self.play_processed_button.setEnabled(False)
        thread = threading.Thread(target=self.playProcessed)
        thread.start()

    def playProcessed(self):
        try:
            utils.play_audio_file(self.processedFileName)
        except:
            self.signal.message_signal.emit('Error:No processed audio loaded')
        
        self.play_processed_button.setEnabled(True)

    def playFile_event(self):
        self.play_file_button.setEnabled(False)
        thread = threading.Thread(target=self.playFile)
        thread.start()

    def playFile(self):
        try:
            utils.play_audio_file(self.audio_file_loc)
        except:
            self.signal.message_signal.emit('Error:No opened audio file')
        
        self.play_file_button.setEnabled(True)

    def check_resources(self):
        if (not os.path.isdir(os.path.join(base_path, 'data'))):
            os.mkdir(os.path.join(base_path, 'data'))
            QtWidgets.QMessageBox.information(
                self, "Info", "data directory created", QtWidgets.QMessageBox.Ok)
        if (not os.path.isdir(os.path.join(base_path, 'etc\\artwork'))):
            QtWidgets.QMessageBox.warning(
                self, "Warning", "etc\\artwork directory not found", QtWidgets.QMessageBox.Ok)
        if (not os.path.isdir(os.path.join(base_path, 'etc\\docs'))):
            QtWidgets.QMessageBox.warning(
                self, "Warning", "etc\\docs directory not found", QtWidgets.QMessageBox.Ok)

    def clear(self, param):
        if param == 'all':
            self.audio_file_loc = ''
            self.processedFileName = ''
            self.label.setText('No File Opened!')
            self.recording_name_edit.clear()
            self.recording_time_edit.clear()
            self.sampling_frequency_edit.clear()
            self.decay_factor_edit.clear()
            self.delay_time_edit.clear()
            self.ax1.clear()
            self.ax2.clear()
            self.defineSpectrums()
        elif param == 'prev_proc':
            self.audio_file_loc = ''
            self.processedFileName = ''
            self.label.setText('No File Opened!')
            self.decay_factor_edit.clear()
            self.delay_time_edit.clear()
            self.ax1.clear()
            self.ax2.clear()
            self.defineSpectrums()

    def defineSpectrums(self):
        self.ax1.set_title('Input Signal Spectrum', fontsize=10)
        self.ax1.set_xlabel('Frequency (Hz)', fontsize=8)
        self.ax1.set_ylabel('Amplitude', fontsize=8)
        self.ax1.tick_params(axis='x', labelsize=6)
        self.ax1.tick_params(axis='y', labelsize=6)

        self.ax2.set_title('Output Signal Spectrum', fontsize=10)
        self.ax2.set_xlabel('Frequency (Hz)', fontsize=8)
        self.ax2.set_ylabel('Amplitude', fontsize=8)
        self.ax2.tick_params(axis='x', labelsize=6)
        self.ax2.tick_params(axis='y', labelsize=6)

        self.canvas.draw()

    def show_message_box(self, message):
        msgType, message = message.split(':')
        if msgType == 'Info':
            QtWidgets.QMessageBox.information(
                self, "Info", message, QtWidgets.QMessageBox.Ok)
        elif msgType == 'Error':
            QtWidgets.QMessageBox.critical(
                self, "Error", message, QtWidgets.QMessageBox.Ok)
        elif msgType == 'Warning':
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok)
