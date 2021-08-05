from drivers.initials import constants
from drivers.initials.variables import LedVar

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
        self._var.register_led_enable_callback(self._catch_enable_change)
        self._var.register_led_strip_callback(self._catch_strip_properties_change)

    @staticmethod
    def random_colors():
        c1 = random.randint(0, 1) * 255
        c2 = random.randint(0, 1) * 255
        c3 = random.randint(0, 1) * 255
        if c1 == c2 == c3 == 0:
            return [255, 255, 255]
        return [c1, c2, c3]

    def _catch_enable_change(self):
        self._set_color()

    def _catch_color_change(self):
        self._set_color()

    def _catch_strip_properties_change(self):
        self._v5_set_color()

    def _set_color(self):
        self._v12_set_color()
        self._v5_set_color()

    def _v12_set_color(self):
        if self._var.led12_on:
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_RED, int(
                self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_GREEN, int(
                self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_BLUE, int(
                self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
        else:
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_RED, 0)
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_GREEN, 0)
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_BLUE, 0)

    def _v5_set_color(self):
        if self._var.led5_on:
            for i in range(0, constants.LEDSTRIP.LED_COUNT, self._var.led_strip_direction):
                if i < self._var.led_strip_display:
                    self._strip.setPixelColorRGB(
                        i,
                        int(self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS),
                        int(self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS),
                        int(self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
                else:
                    self._strip.setPixelColorRGB(i, 0, 0, 0)
            self._strip.show()
        else:
            for i in range(0, self._var.led_strip_display, self._var.led_strip_direction):
                self._strip.setPixelColorRGB(i, 0, 0, 0)
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

    def get_colors(self):
        return [self._var.led_red, self._var.led_green, self._var.led_blue]

    def get_strip_enable(self):
        return [self._var.led5_on, self._var.led12_on]

    def get_strip_brightness(self):
        return self._var.led_brightness

    def set_enable_state(self, strip, state):
        if strip == 0:
            if state:
                self._var.led5_on = True
            else:
                self._var.led5_on = False
        elif strip == 1:
            if state:
                self._var.led12_on = True
            else:
                self._var.led12_on = False

    def set_brightness(self, new_value):
        self._var.led_brightness = new_value

    def set_strip_direction(self, new_value):
        self._var.led_strip_direction = new_value

    def set_strip_display_count(self, new_value):
        self._var.led_strip_display = new_value
