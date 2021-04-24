from handler import MainHandler
from flask import jsonify, request, Flask
import ir_remote_keybinding as irk


class Api:
    def __init__(self, app: Flask, hand: MainHandler):
        self.hand = hand
        self.app = app

        self.app.config['host'] = '0.0.0.0'
        self.app.config['port'] = 5000
        self.app.config['debug'] = False

        self.app.add_url_rule(rule='/status', view_func=self.getStatus, methods=['GET'])
        self.app.add_url_rule(rule='/RGB/<int:red>/<int:green>/<int:blue>', view_func=self.setRGB, methods=['POST'])
        self.app.add_url_rule(rule='/RGB', view_func=self.getRGB, methods=['GET'])
        self.app.add_url_rule(rule='/switch/<int:switchID>/<int:state>', view_func=self.setSwitches, methods=['POST'])
        self.app.add_url_rule(rule='/brightness/<int:brightness>', view_func=self.setBrightness, methods=['POST'])
        self.app.add_url_rule(rule='/state', view_func=self.getCurrentState, methods=['GET'])
        self.app.add_url_rule(rule='/amplituner/<int:code>', view_func=self.setAmplituner, methods=['POST'])
        self.app.add_url_rule(rule='/temperatures', view_func=self.getTemperatures, methods=['GET'])
        self.app.add_url_rule(rule='/weather', view_func=self.getCurrentWeather, methods=['GET'])
        self.app.add_url_rule(rule='/forecast/daily', view_func=self.getForecastDaily, methods=['GET'])
        self.app.add_url_rule(rule='/forecast/hourly', view_func=self.getForecastHourly, methods=['GET'])

    @staticmethod
    def getStatus():
        return jsonify([{'status': 'OK'}])

    def setRGB(self, red, green, blue):
        self.hand.set_colors([red, green, blue])
        colors = self.hand.get_colors()
        codes = ['red', 'green', 'blue']
        response = dict(zip(codes, colors))
        return response

    def getRGB(self):
        colors = self.hand.get_colors()
        codes = ['red', 'green', 'blue']
        response = dict(zip(codes, colors))
        return response

    def setSwitches(self, switchID, state):
        if switchID in [0,1]:
            self.hand.set_strip_enable(switchID, state)
            ids = ["LED5", "LED12"]
            response = jsonify(dict(zip(ids, self.hand.get_strip_enable())))
            return response
        elif switchID in [2,3]:
            self.hand.set_lcd_background(switchID, state)
            ids = ["LCD0", "LCD1"]
            response = jsonify(dict(zip(ids, self.hand.get_lcd_background())))
            return response

    def setBrightness(self, brightness):
        self.hand.set_strip_brightness(brightness)
        response = jsonify({"brightness": self.hand.get_strip_brightness()})
        return response

    def getCurrentState(self):
        brightness = self.hand.get_strip_brightness()
        colors = self.hand.get_colors()
        led_enable = self.hand.get_strip_enable()
        lcd_enable = self.hand.get_lcd_background()
        brtns = {"brightness": brightness}
        cols = dict(zip(["Red", "Green", "Blue"], colors))
        led_en = dict(zip(["led1", "led2"], led_enable))
        lcd_en = dict(zip(["lcd1", "lcd2"], lcd_enable))

        response = jsonify(brtns, cols, led_en, lcd_en)
        return response

    def setAmplituner(self, code):
        codes = {0: irk.yamaha['KEY_STANDBY'],
                 1: irk.yamaha['KEY_SLEEP'],
                 2: irk.yamaha['KEY_VOLUME_DOWN'],
                 3: irk.yamaha['KEY_VOLUME_UP']}
        self.hand.send_ir_signal(codes[code])

    def getTemperatures(self):
        temps = self.hand.get_current_temperatures()
        codes = ['outdoor', 'core', 'ambient']
        response = dict(zip(codes, temps))
        return response

    def getCurrentWeather(self):
        current = self.hand.get_current_conditions()
        return jsonify(current)

    def getForecastDaily(self):
        forecast = self.hand.get_forecast_daily()
        return jsonify(forecast)

    def getForecastHourly(self):
        forecast = self.hand.get_forecast_hourly()
        return jsonify(forecast)

    def weatherSwitch(self, num, state):
        if state:
            if num == 1:
                self.hand.start_display_weather()
            elif num == 2:
                self.hand.stop_display_weather()