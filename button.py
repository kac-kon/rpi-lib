from drivers.MCP3008 import MCP3008
from variables import ButtonsVar
import threading
import time

THRESHOLD = 900


class ButtonsHandler:
    def __init__(self):
        self.adc = MCP3008()
        self.var = ButtonsVar()
        self.pressed = [False, False, False]
        self._exit_event = threading.Event()
        self._thread_loop = threading.Thread()

    def start_loop(self):
        self._exit_event.clear()
        self._thread_loop = threading.Thread(target=self._start_loop)
        self._thread_loop.start()

    def _start_loop(self):
        while not (self._exit_event.is_set()):
            data = self.adc.read_3()
            for i in range(3):
                if self.pressed[i] is False and data[i] > THRESHOLD:
                    if i == 0:
                        print("1 pressed")
                        self.var.button_one = True
                    elif i == 1:
                        self.var.button_two = True
                    elif i == 2:
                        self.var.button_three = True
                    self.pressed[i] = True
            for i in range(3):
                if data[i] < THRESHOLD and self.pressed[i] is True:
                    if i == 0:
                        self.var.button_one = False
                    elif i == 1:
                        self.var.button_two = False
                    elif i == 2:
                        self.var.button_three = False
                    self.pressed[i] = False
            time.sleep(0.05)
        self._exit_event.clear()

    def exit_loop(self):
        self._exit_event.set()
        self._thread_loop.join()
        print("thread finished")

    def register_button_callback(self, callback):
        self.var.register_button_callback(callback)
