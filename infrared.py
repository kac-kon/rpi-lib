import pigpio
import subprocess

from constants import GPIO
from drivers.IR_hasher import Hasher
import threading, time
import ir_remote_keybinding as irk


class IR:
    def __init__(self):
        self._pi = pigpio.pi()
        self._ir_hasher = Hasher(self._pi, GPIO.GPIO_IR_RX, self._cb, timeout=10)
        self._utils_callbacks = []
        self._color_callbacks = []
        self._timer_event = threading.Event()
        self._timer_thread = threading.Thread()
        self._timer_time = -1

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

    def sleep(self, sleep_time):
        if self._timer_thread.is_alive():
            self._timer_event.set()
            self._timer_thread.join()
            self._timer_time = -1
        else:
            self._timer_event.clear()
            self._timer_thread = threading.Thread(target=self._sleep, args=[sleep_time])
            self._timer_thread.start()

    def _sleep(self, sleep_time):
        self._timer_time = sleep_time
        while self._timer_time > 0 and not self._timer_event.is_set():
            self._timer_event.wait(60)
            self._timer_time -= 1
        self.send_signal(irk.yamaha['KEY_STANDBY'])

    def get_state(self):
        codes = ["enabled", "timer"]
        response = dict(zip(codes, [self._timer_thread.is_alive(), self._timer_time]))
        return response
