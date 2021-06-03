from handler import MainHandler
from flask import jsonify, request, Flask
import ir_remote_keybinding as irk
import constants


class Api:
    def __init__(self, app: Flask, hand: MainHandler):
        self.hand = hand
        self.app = app

        self.app.add_url_rule('/checkStatus', 'getStatus', self.getStatus, methods=['GET'])
        self.app.add_url_rule('/RGB/<int:red>/<int:green>/<int:blue>', 'setRGB', self.setRGB, methods=['POST'])
        self.app.add_url_rule('/RGB', 'getRGB', self.getRGB, methods=['GET'])
        self.app.add_url_rule('/switch/<int:switchID>/<int:state>', 'setSwitches', self.setSwitches, methods=['POST'])
        self.app.add_url_rule('/brightness/<int:brightness>', 'setBrightness', self.setBrightness, methods=['POST'])
        self.app.add_url_rule('/state', 'getCurrentState', self.getCurrentState, methods=['GET'])
        self.app.add_url_rule('/amplituner/<int:code>', 'setAmplituner', self.setAmplituner, methods=['POST'])
        self.app.add_url_rule('/amplituner/sleep/<int:sleep_time>', 'sleepAmplituner', self.sleepAmplituner, methods=['POST'])
        self.app.add_url_rule('/amplituner/sleep/state', 'getAmpSleepState', self.getAmpSleepState, methods=['GET'])
        self.app.add_url_rule('/temperatures', 'getTemperatures', self.getTemperatures, methods=['GET'])
        self.app.add_url_rule('/weather', 'getCurrentWeather', self.getCurrentWeather, methods=['GET'])
        self.app.add_url_rule('/forecast/daily', 'getForecastDaily', self.getForecastDaily, methods=['GET'])
        self.app.add_url_rule('/forecast/hourly', 'getForecastHourly', self.getForecastHourly, methods=['GET'])
        self.app.add_url_rule('/spec/<int:sensitivity>/<float:inertia>/<int:freq>/<int:speed>', 'setSpecConfig',
                              self.setSpecConfig, methods=['POST'])

        self.hand.register_button_callback(self.weatherSwitch)
        self.hand.register_button_callback(self.autoLEDSwitch)

#######################################
#   REST API ENDPOINTS
#######################################

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
        if switchID in [0, 1]:
            self.hand.set_strip_enable(switchID, state)
            ids = ["LED5", "LED12"]
            response = jsonify(dict(zip(ids, self.hand.get_strip_enable())))
            return response
        elif switchID in [2, 3]:
            if switchID == 2:
                self.hand.set_lcd_background(constants.LCD.ID_0, state)
            else:
                self.hand.set_lcd_background(constants.LCD.ID_1, state)
            ids = ["LCD0", "LCD1"]
            response = jsonify(dict(zip(ids, self.hand.get_lcd_background())))
            return response
        elif switchID in [4]:
            self.setAutoLED(state)
            response = jsonify({"AutoLED": self.hand.auto_is_alive()})
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
        auto_en = {"auto_led": self.hand.auto_is_alive()}

        response = jsonify(brtns, cols, led_en, lcd_en, auto_en)
        return response

    def setAmplituner(self, code):
        codes = {0: irk.yamaha['KEY_STANDBY'],
                 1: irk.yamaha['KEY_SLEEP'],
                 2: irk.yamaha['KEY_VOLUME_DOWN'],
                 3: irk.yamaha['KEY_VOLUME_UP']}
        if code != 1:
            self.hand.send_ir_signal(codes[code])
            return jsonify({"status": "OK"})

    def sleepAmplituner(self, sleep_time):
        self.hand.sleep_amplituner(sleep_time)
        return self.hand.get_sleep_timer()

    def getAmpSleepState(self):
        return jsonify(self.hand.get_sleep_timer())

    def getTemperatures(self):
        temps = self.hand.get_current_temperatures()
        codes = ['ambient', 'core', 'outdoor']
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

    def setAutoLED(self, new_state):
        if new_state:
            self.hand.start_auto_led()
        else:
            self.hand.stop_auto_led()

    def setSpecConfig(self, sensitivity, inertia, freq, speed):
        self.hand.set_sensitivity(sensitivity)
        self.hand.set_inertia(inertia)
        self.hand.set_analyzed_frequency(freq)
        self.hand.set_fade_speed(speed)

#######################################
#   BUTTONS ENDPOINTS
#######################################

    def weatherSwitch(self, num, state):
        if state:
            if num == 1:
                self.hand.start_display_weather()
                self.hand.set_lcd_background(constants.LCD.ID_0, True)
                self.hand.set_lcd_background(constants.LCD.ID_1, True)
            elif num == 2:
                self.hand.stop_display_weather()
                self.hand.set_lcd_background(constants.LCD.ID_0, False)
                self.hand.set_lcd_background(constants.LCD.ID_1, False)

    def autoLEDSwitch(self, num, state):
        if state and num == 3:
            if self.hand.auto_is_alive():
                self.hand.stop_auto_led()
            elif not self.hand.auto_is_alive():
                self.hand.start_auto_led()
