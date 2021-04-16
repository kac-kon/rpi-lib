from constants import AUDIO
import threading
import pyaudio
from struct import unpack
import numpy as np


class Spec:
    def __init__(self, device=AUDIO.DEFAULT_DEVICE):
        self._device = device
        self.matrix = np.zeros(10)
        self.weighting = AUDIO.WEIGHTING
        self.frequencies = AUDIO.FREQUENCIES
        self.sensitivity = np.array(AUDIO.SENSITIVENESS)
        self._spec_thread = threading.Thread()
        self._exit_event = threading.Event()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=AUDIO.NO_CHANNELS,
                                  rate=AUDIO.SAMPLE_RATE,
                                  input=True,
                                  frames_per_buffer=AUDIO.CHUNK,
                                  input_device_index=self._device)

    def list_devices(self):
        i = 0
        n = self.p.get_device_count()
        while i < n:
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print(f"{i}. {dev['name']}")
            i +=1

    @staticmethod
    def _piff(val):
        return int(2 * AUDIO.CHUNK * val / AUDIO.SAMPLE_RATE)

    def _calculate_levels(self, data):
        matrix = np.zeros(10)
        data = unpack("%dh" % (len(data) / 2), data)
        data = np.array(data, dtype='h')
        fourier = np.fft.rfft(data)
        fourier = np.delete(fourier, len(fourier) - 1)
        power = np.abs(fourier)
        for i in range(10):
            matrix[i] = (int(np.max(power[self._piff(self.frequencies[i]): self._piff(self.frequencies[i+1]): 1])) / 10) ** self.sensitivity[i+1]
        matrix = np.divide(np.multiply(matrix, self.weighting), 1_000_000 / self.sensitivity[0]).astype(int)
        self.matrix = matrix.clip(0, 255)

    def catch_bit(self):
        data = self.stream.read(AUDIO.CHUNK, exception_on_overflow=False)
        self._calculate_levels(data)

    def start_monitoring(self):
        self._exit_event.clear()
        self._spec_thread = threading.Thread(target=self._start_monitoring)
        self._spec_thread.start()

    def _start_monitoring(self):
        while not self._exit_event.is_set():
            self.catch_bit()
            self.spec_matrix = self.matrix

    def stop_monitoring(self):
        self._exit_event.set()
        self._spec_thread.join()