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
        # self._spec = Spec()

        self._but.start_loop()
        self._ir_parser = IRParser(self._led)

        self._but.register_button_callback(Buttons.button_pressed)
        # self._ir.register_color_callback(self._ir_parser.color_keycode_received)

        self.set_colors([50, 0, 0])
        self.set_colors([50, 50, 0])

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


if __name__ == "__main__":
    app = Flask("__name__")
    api = Api(app)
    hand = MainHandler()
    # hand.start_display_weather()


    class RpiServer(Resource):
        def get(self):
            response = jsonify([{"data": "CHUJ"}])
            return response


    class CheckStatus(Resource):
        def get(self):
            response = jsonify([{"status": "OK"}])
            return response


    class RGBSet(Resource):
        def post(self, red, green, blue):
            hand.set_colors([red, green, blue])
            colors = hand.get_colors()
            codes = ["Red", "Green", "Blue"]
            response = dict(zip(codes, colors))
            return jsonify(response)


    class RGBGet(Resource):
        def get(self):
            colors = hand.get_colors()
            response = jsonify([{"Red": colors[0],
                                 "Green": colors[1],
                                 "Blue": colors[2]}])
            return response


    class Switches(Resource):
        def post(self, switchID, state):
            if switchID == 0 or switchID == 1:
                hand.set_strip_enable(switchID, state)
                ids = ["LED5", "LED12"]
                response = jsonify(dict(zip(ids, hand.get_strip_enable())))
                return response
            elif switchID == 2 or switchID == 3:
                hand.set_lcd_background(switchID, state)
                ids = ["LCD0", "LCD1"]
                response = jsonify(dict(zip(ids, hand.get_lcd_background())))
                return response


    class Brightness(Resource):
        def post(self, brightness):
            hand.set_strip_brightness(brightness)
            response = jsonify({"brightness": hand.get_strip_brightness()})
            return response


    class State(Resource):
        def get(self):
            brightness = hand.get_strip_brightness()
            colors = hand.get_colors()
            led_enable = hand.get_strip_enable()
            lcd_enable = hand.get_lcd_background()

            brtns = {"brightness": brightness}
            cols = dict(zip(["Red", "Green", "Blue"], colors))
            led_en = dict(zip(["led1", "led2"], led_enable))
            lcd_en = dict(zip(["lcd1", "lcd2"], lcd_enable))

            response = jsonify(brtns, cols, led_en, lcd_en)
            return response


    class Amplituner(Resource):
        codes = {0: irk.yamaha['KEY_STANDBY'],
                 1: irk.yamaha['KEY_SLEEP'],
                 2: irk.yamaha['KEY_VOLUME_DOWN'],
                 3: irk.yamaha['KEY_VOLUME_UP']}

        def post(self, code):
            hand.send_ir_signal(self.codes[code])


    class Temperatures(Resource):
        def get(self):
            text = str(subprocess.check_output("sensors | grep temp1", stdin=subprocess.PIPE, shell=True))
            core = float(text[text.find('+') + 1:text.find('+') + 5])
            ambient = 22.4
            outdoor = -2.2
            return jsonify({'core': core,
                            'ambient': ambient,
                            'outdoor': outdoor})


    class Weather(Resource):

        def get(self):
            current = hand.get_current_conditions()
            return jsonify(current)


    class ForecastDaily(Resource):

        def get(self):
            print("get called")
            forecast = hand.get_forecast_daily()
            print("got forecast")
            x = jsonify(forecast)
            print("returning get")
            return x


    class ForecastHourly(Resource):

        def get(self):
            forecast = hand.get_forecast_hourly()
            return jsonify(forecast)


    class LCD(Resource):
        @staticmethod
        def weather_switch(num, value):
            if num == 1:
                hand.start_display_weather()
            elif num == 2:
                hand.stop_display_weather()


    hand.register_button_callback(LCD.weather_switch)
    api.add_resource(RpiServer, "/dupa")
    api.add_resource(CheckStatus, "/checkStatus")
    api.add_resource(RGBSet, "/RGB/<int:red>/<int:green>/<int:blue>")
    api.add_resource(RGBGet, "/RGB")
    api.add_resource(Switches, "/switch/<int:switchID>/<int:state>")
    api.add_resource(Brightness, "/brightness/<int:brightness>")
    api.add_resource(State, "/state")
    api.add_resource(Amplituner, "/amplituner/<int:code>")
    api.add_resource(Temperatures, "/temperatures")
    api.add_resource(Weather, "/weather")
    api.add_resource(ForecastDaily, "/forecast/daily")
    api.add_resource(ForecastHourly, "/forecast/hourly")
    api.add_resource(LCD, "/LCD/<int:mode>")

    app.run(debug=True, host="0.0.0.0", port=5000)
