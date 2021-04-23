from handler import MainHandler
from flask_restful import Resource
from flask import jsonify


class Api:
    def __init__(self, hand: MainHandler):
        self.hand = hand

    class CheckStatus(Resource):
        def __init__(self, hand: MainHandler):
            super(self).__init__()
            self.hand = hand

        def get(self):
            response = jsonify([{"status": "OK"}])
            return response

    class RGBSet(Resource):
        def __init__(self, hand: MainHandler):
            super(self).__init__()
            self.hand = hand

        def post(self, red, green, blue):
            self.hand.set_colors([red, green, blue])
            colors = self.hand.get_colors()
            codes = ["Red", "Green", "Blue"]
            response = dict(zip(codes, colors))
            return jsonify(response)

    class RGBGet(Resource):
        def __init__(self, hand: MainHandler):
            super(self).__init__()
            self.hand = hand

        def get(self):
            colors = self.hand.get_colors()
            response = jsonify([{"Red": colors[0],
                                 "Green": colors[1],
                                 "Blue": colors[2]}])
            return response
    #
    # class Switches(Resource):
    #     def post(self, switchID, state):
    #         if switchID == 0 or switchID == 1:
    #             hand.set_strip_enable(switchID, state)
    #             ids = ["LED5", "LED12"]
    #             response = jsonify(dict(zip(ids, hand.get_strip_enable())))
    #             return response
    #         elif switchID == 2 or switchID == 3:
    #             hand.set_lcd_background(switchID, state)
    #             ids = ["LCD0", "LCD1"]
    #             response = jsonify(dict(zip(ids, hand.get_lcd_background())))
    #             return response
    #
    # class Brightness(Resource):
    #     def post(self, brightness):
    #         hand.set_strip_brightness(brightness)
    #         response = jsonify({"brightness": hand.get_strip_brightness()})
    #         return response
    #
    # class State(Resource):
    #     def get(self):
    #         brightness = hand.get_strip_brightness()
    #         colors = hand.get_colors()
    #         led_enable = hand.get_strip_enable()
    #         lcd_enable = hand.get_lcd_background()
    #
    #         brtns = {"brightness": brightness}
    #         cols = dict(zip(["Red", "Green", "Blue"], colors))
    #         led_en = dict(zip(["led1", "led2"], led_enable))
    #         lcd_en = dict(zip(["lcd1", "lcd2"], lcd_enable))
    #
    #         response = jsonify(brtns, cols, led_en, lcd_en)
    #         return response
    #
    # class Amplituner(Resource):
    #     codes = {0: irk.yamaha['KEY_STANDBY'],
    #              1: irk.yamaha['KEY_SLEEP'],
    #              2: irk.yamaha['KEY_VOLUME_DOWN'],
    #              3: irk.yamaha['KEY_VOLUME_UP']}
    #
    #     def post(self, code):
    #         hand.send_ir_signal(self.codes[code])
    #
    # class Temperatures(Resource):
    #     def get(self):
    #         text = str(subprocess.check_output("sensors | grep temp1", stdin=subprocess.PIPE, shell=True))
    #         core = float(text[text.find('+') + 1:text.find('+') + 5])
    #         ambient = 22.4
    #         outdoor = -2.2
    #         return jsonify({'core': core,
    #                         'ambient': ambient,
    #                         'outdoor': outdoor})
    #
    # class Weather(Resource):
    #
    #     def get(self):
    #         current = hand.get_current_conditions()
    #         return jsonify(current)
    #
    # class ForecastDaily(Resource):
    #
    #     def get(self):
    #         forecast = hand.get_forecast_daily()
    #         return jsonify(forecast)
    #
    # class ForecastHourly(Resource):
    #
    #     def get(self):
    #         forecast = hand.get_forecast_hourly()
    #         return jsonify(forecast)
    #
    # class LCD(Resource):
    #     @staticmethod
    #     def weather_switch(num, value):
    #         if num == 1:
    #             hand.start_display_weather()
    #         elif num == 2:
    #             hand.stop_display_weather()
