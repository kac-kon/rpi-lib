import pigpio
import subprocess

from constants import GPIO
from drivers.IR_hasher import Hasher
import ir_remote_keybinding as irk


class IR:
    def __init__(self):
        self._pi = pigpio.pi()
        self._ir_hasher = Hasher(self._pi, GPIO.GPIO_IR_RX, self._cb, timeout=10)
        self._utils_callbacks = []
        self._color_callbacks = []

    def _cb(self, code):
        if code in irk.hashes:
            if irk.hashes[code] in irk.color_codes:
                self._notify_color_observers(irk.hashes[code])
            else:
                self._notify_utils_observers(code)

    def stop_hasher(self):
        self._ir_hasher.pi.stop()
        self._pi.stop()

    def start_hasher(self):
        # self.stop_hasher()
        self._pi = pigpio.pi()
        self._ir_hasher = Hasher(self._pi, GPIO.GPIO_IR_RX, self._cb, timeout=10)

    def _notify_utils_observers(self, hashcode):
        for callback in self._utils_callbacks:
            callback(hashcode)

    def register_utils_callback(self, callback):
        self._utils_callbacks.append(callback)

    def _notify_color_observers(self, hashcode):
        for callback in self._color_callbacks:
            callback(irk.color_codes[hashcode])

    def register_color_callback(self, callback):
        self._color_callbacks.append(callback)

    @staticmethod
    def send_signal(key_code):
        try:
            subprocess.run(['ir-ctl', '-S', f'nec:{key_code}'])
        except Exception as e:
            print(e)
            pass
