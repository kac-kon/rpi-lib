import constants
from variables import LedVar

import time
import pigpio
import threading
import random
from rpi_ws281x import *


class LED:
    def __init__(self):
        self._var = LedVar()
        self._pi = pigpio.pi()
        self._strip = Adafruit_NeoPixel(constants.LEDSTRIP.LED_COUNT,
                                        constants.LEDSTRIP.LED_PIN,
                                        constants.LEDSTRIP.LED_FREQ_HZ,
                                        constants.LEDSTRIP.LED_DMA,
                                        constants.LEDSTRIP.LED_INVERT,
                                        constants.LEDSTRIP.LED_BRIGHTNESS,
                                        constants.LEDSTRIP.LED_CHANNEL)
        self._fade_exit_event = threading.Event()
        self._fade_thread_loop = threading.Thread()
        self._strip.begin()
        random.seed()

        self._var.register_led_color_callback(self._catch_color_change)

    def _catch_color_change(self, channel, val):
        self._set_color()

    def _set_color(self):
        self._v12_set_color()
        self._v5_set_color()

    def _v12_set_color(self):
        self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_RED, int(self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS) )
        self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_GREEN, int(self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS) )
        self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_BLUE, int(self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))

    def _v5_set_color(self):
        for i in range(0, self._var.led_strip_display, self._var.led_strip_direction):
            self._strip.setPixelColorRGB(i, int(self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS),
                                         int(self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS),
                                         int(self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
        self._strip.show()

    def fade_away(self):
        self._fade_away()

    def _fade_away(self):
        self._var.led_brightness = constants.INITIALS.LED_BRIGHTNESS
        time.sleep(0.1)
        while self._var.led_brightness > 0 and not self._fade_exit_event.is_set():
            if (self._var.led_brightness - self._var.fade_away_speed) < 0:
                self._var.led_brightness = 0
            else:
                self._var.led_brightness -= self._var.fade_away_speed
            time.sleep(.02)

    def set_color_rgb(self, color_r, color_g, color_b):
        self._var.led_red = color_r
        self._var.led_green = color_g
        self._var.led_blue = color_b

    def set_color(self, color_array):
        self._var.led_red = color_array[0]
        self._var.led_green = color_array[1]
        self._var.led_blue = color_array[2]
