from flask_restful import Resource, Api
from flask import Flask, jsonify
from handler import MainHandler
import ir_remote_keybinding as irk
import subprocess, tempfile


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
        def __init__(self):
            self.lines = []

        def get(self):
            with tempfile.TemporaryFile() as tempf:
                proc = subprocess.Popen("sensors | grep temp1", stdin=subprocess.PIPE, shell=True)
                proc.wait()
                tempf.seek(0)
                self.lines = tempf.readlines()
                tempf.ty

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
            forecast = hand.get_forecast_daily()
            return jsonify(forecast)


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

    app.run(debug=False, host="0.0.0.0", port=5000)
