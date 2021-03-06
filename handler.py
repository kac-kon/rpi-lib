import time, threading, numpy as np

import subprocess

import constants
from button import ButtonsHandler
from led_control import LED
from infrared import IR, irk
from lcd_control import Displays
from weather import Weather
from spectrum import Spec
from flask import Flask, jsonify, request
from flask_restful import Api, Resource


class Buttons:
    @staticmethod
    def button_pressed(num, value):
        print(f"button {num} is pressed? {value}")


class IRParser:
    def __init__(self, led: LED):
        self._led = led

    def color_keycode_received(self, keycode):
        self._led.set_color(irk.color_codes[keycode])


class MainHandler:
    def __init__(self):
        self._but = ButtonsHandler()
        self._led = LED()
        self._ir = IR()
        self._weather = Weather()
        self._dis = Displays(self._weather)
        self._spec = Spec(self._led)

        self._but.start_loop()
        self._ir_parser = IRParser(self._led)

        # self._but.register_button_callback(Buttons.button_pressed)
        # self._ir.register_color_callback(self._ir_parser.color_keycode_received)

        self.set_strip_brightness(0)
        self.set_colors([255, 0, 180])

    def start_auto_led(self):
        self._spec.start_auto()

    def stop_auto_led(self):
        self._spec.stop_auto()

    def register_button_callback(self, callback):
        self._but.register_button_callback(callback)

    def start_display_weather(self):
        self._dis.start_print_datetime_short()

    def stop_display_weather(self):
        self._dis.exit_print_datetime_short()

    def get_colors(self):
        return self._led.get_colors()

    def get_lcd_background(self):
        return self._dis.get_lcd_background()

    def get_strip_enable(self):
        return self._led.get_strip_enable()

    def get_strip_brightness(self):
        return self._led.get_strip_brightness()

    def set_colors(self, colors):
        self._led.set_color(colors)

    def set_lcd_background(self, id_, state):
        if id_ == 2:
            self._dis.set_backlight(constants.LCD.ID_0, state)
        if id_ == 3:
            self._dis.set_backlight(constants.LCD.ID_1, state)

    def set_strip_enable(self, strip, state):
        self._led.set_enable_state(strip, state)

    def set_strip_brightness(self, new_value):
        self._led.set_brightness(new_value)

    def send_ir_signal(self, key_code):
        self._ir.send_signal(key_code)

    def get_current_conditions(self):
        return self._weather.get_current_conditions()

    def get_forecast_daily(self):
        return self._weather.get_forecast_daily()

    def get_forecast_hourly(self):
        return self._weather.get_forecast_hourly()

    def get_current_temperatures(self):
        return self._weather.get_temps()

    def auto_is_alive(self):
        return self._spec.auto_is_alive()

    def set_sensitivity(self, new_value):
        self._spec.set_sensitivity(new_value)

    def set_inertia(self, new_value):
        self._spec.set_inertia(new_value)

    def set_analyzed_frequency(self, new_value):
        self._spec.set_analyzed_frequency(new_value)

    def set_fade_speed(self, new_value):
        self._spec.set_speed(new_value)

    def sleep_amplituner(self, sleep_time):
        self._ir.sleep(sleep_time)

    def get_sleep_timer(self):
        return self._ir.get_state()
