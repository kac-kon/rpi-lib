import time, threading, numpy as np
from button import ButtonsHandler
from led_control import LED
from infrared import IR, irk
from lcd_control import Displays
from spectrum import Spec
from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask("__name__")
api = Api(app)


class RpiServer(Resource):
    def get(self):
        response = jsonify([{"data": "CHUJ"}])
        return response

class CheckStatus(Resource):
    def get(self):
        response = jsonify([{"status": "OK"}])
        return response


api.add_resource(RpiServer, "/dupa")
api.add_resource(CheckStatus, "/checkStatus")


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
        self._spec = Spec()

        self._but.start_loop()
        self._ir_parser = IRParser(self._led)

        self._but.register_button_callback(Buttons.button_pressed)
        self._ir.register_color_callback(self._ir_parser.color_keycode_received)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6666)
