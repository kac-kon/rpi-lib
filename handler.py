import time, threading, numpy as np
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

    def get_colors(self):
        return self._led.get_colors()

    def set_colors(self, colors):
        self._led.set_color(colors)



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


    class RGB(Resource):
        def get(self):
            colors = hand.get_colors()
            response = jsonify([{"Red": colors[0]},
                                {"Green": colors[1],
                                 "Blue": colors[2]}])
            return response

        def post(self):
            json_data = request.get_json(force=True)
            red = json_data['Red']
            green = json_data['Green']
            blue = json_data['Blue']
            hand.set_colors([red, green, blue])


    api.add_resource(RpiServer, "/dupa")
    api.add_resource(CheckStatus, "/checkStatus")
    api.add_resource(RGB, "/RGB")

    app.run(debug=True, host="0.0.0.0", port=5000)
