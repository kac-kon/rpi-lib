import time, threading, numpy as np
import constants
from button import ButtonsHandler
from led_control import LED
from infrared import IR, irk
from lcd_control import Displays
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
        self._dis = Displays()
        # self._spec = Spec()

        self._but.start_loop()
        self._ir_parser = IRParser(self._led)

        self._but.register_button_callback(Buttons.button_pressed)
        self._ir.register_color_callback(self._ir_parser.color_keycode_received)

        self.set_colors([50, 50, 100])

    def get_colors(self):
        return self._led.get_colors()

    def set_colors(self, colors):
        self._led.set_color(colors)

    def set_lcd_background(self, id_, state):
        if id_ == 2:
            self._dis.set_backlight(constants.LCD.ID_0, state)
        if id_ == 3:
            self._dis.set_backlight(constants.LCD.ID_1, state)

    def set_strip_enable(self, strip, state):
        self._led.set_enable_state(strip, state)


if __name__ == "__main__":
    app = Flask("__name__")
    api = Api(app)
    hand = MainHandler()


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
            elif switchID == 2 or switchID == 3:
                hand.set_lcd_background(switchID, state)


    api.add_resource(RpiServer, "/dupa")
    api.add_resource(CheckStatus, "/checkStatus")
    api.add_resource(RGBSet, "/RGB/<int:red>/<int:green>/<int:blue>")
    api.add_resource(RGBGet, "/RGB")
    api.add_resource(Switches, "/switch/<int:switchID>/<boolean:state>")

    app.run(debug=True, host="0.0.0.0", port=5000)
