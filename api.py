from handler import MainHandler
from flask import jsonify, Flask
from drivers.initials import constants, ir_remote_keybinding as irk
from components.state import State


class Api:
    def __init__(self, app: Flask, hand: MainHandler):
        self.hand = hand
        self.app = app

        self.app.add_url_rule('/checkStatus', 'getStatus', self.get_status, methods=['GET'])
        self.app.add_url_rule('/RGB/<int:red>/<int:green>/<int:blue>', 'setRGB', self.set_rgb, methods=['POST'])
        self.app.add_url_rule('/switch/<int:switch_id>/<int:state>', 'setSwitches', self.set_switches, methods=['POST'])
        self.app.add_url_rule('/brightness/<int:brightness>', 'setBrightness', self.set_brightness, methods=['POST'])
        self.app.add_url_rule('/led/strip/direction/<int:new_value>', 'setStripDirection',
                              self.set_strip_direction, methods=['POST'])
        self.app.add_url_rule('/led/strip/displayCount/<int:new_value>', 'setStripDisplayCount',
                              self.set_strip_display_count, methods=['POST'])
        self.app.add_url_rule('/state', 'getCurrentState', self.get_current_state, methods=['GET'])
        self.app.add_url_rule('/amplituner/<int:code>', 'setAmplituner', self.set_amplituner, methods=['POST'])
        self.app.add_url_rule('/amplituner/sleep/<int:sleep_time>', 'sleepAmplituner',
                              self.set_amplituner, methods=['POST'])
        self.app.add_url_rule('/amplituner/sleep/state', 'getAmpSleepState', self.get_amp_sleep_state, methods=['GET'])
        self.app.add_url_rule('/temperatures', 'getTemperatures', self.get_temperatures, methods=['GET'])
        self.app.add_url_rule('/weather', 'getCurrentWeather', self.get_current_weather, methods=['GET'])
        self.app.add_url_rule('/forecast/daily', 'getForecastDaily', self.get_forecast_daily, methods=['GET'])
        self.app.add_url_rule('/forecast/hourly', 'getForecastHourly', self.get_forecast_hourly, methods=['GET'])
        self.app.add_url_rule('/spec/<int:sensitivity>/<float:inertia>/<int:freq>/<int:speed>', 'setSpecConfig',
                              self.set_spec_config, methods=['POST'])

        # self.hand.register_button_callback(self.weatherSwitch)
        # self.hand.register_button_callback(self.autoLEDSwitch)
        self.hand.register_button_callback(self.print_menu)
        self.hand.register_menu_callback("weather_enable", self.enable_weather)
        self.hand.register_menu_callback("autoled_enable", self.enable_auto_led)
        self.hand.register_menu_callback("amp_vol_up", self.vol_up)
        self.hand.register_menu_callback("amp_vol_down", self.vol_down)

#######################################
#   REST API ENDPOINTS
#######################################

    @staticmethod
    def get_status():
        return jsonify([{'status': 'OK'}])

    def set_rgb(self, red, green, blue):
        self.hand.set_colors([red, green, blue])
        colors = self.hand.get_colors()
        codes = ['red', 'green', 'blue']
        response = dict(zip(codes, colors))
        return response

    def set_switches(self, switch_id, state):
        if switch_id in [0, 1]:
            self.hand.set_strip_enable(switch_id, state)
            ids = ["LED5", "LED12"]
            response = jsonify(dict(zip(ids, self.hand.get_strip_enable())))
            return response
        elif switch_id in [2, 3]:
            if switch_id == 2:
                self.hand.set_lcd_background(constants.LCD.ID_0, state)
            else:
                self.hand.set_lcd_background(constants.LCD.ID_1, state)
            ids = ["LCD0", "LCD1"]
            response = jsonify(dict(zip(ids, self.hand.get_lcd_background())))
            return response
        elif switch_id in [4]:
            self.set_auto_led(state)
            response = jsonify({"AutoLED": self.hand.auto_is_alive()})
            return response

    def set_brightness(self, brightness):
        self.hand.set_strip_brightness(brightness)
        response = jsonify({"brightness": self.hand.get_strip_brightness()})
        return response

    def get_current_state(self):
        brightness = self.hand.get_strip_brightness()
        colors = self.hand.get_colors()
        led_enable = self.hand.get_strip_enable()
        lcd_enable = self.hand.get_lcd_background()
        auto_enable = self.hand.auto_is_alive()
        state = State(brightness, colors[0], colors[1], colors[2], led_enable[0], led_enable[1],
                      lcd_enable[0], lcd_enable[1], auto_enable)
        # brtns = {"brightness": brightness}
        # cols = dict(zip(["Red", "Green", "Blue"], colors))
        # led_en = dict(zip(["led1", "led2"], led_enable))
        # lcd_en = dict(zip(["lcd1", "lcd2"], lcd_enable))
        # auto_en = {"auto_led": self.hand.auto_is_alive()}

        # response = jsonify(brtns, cols, led_en, lcd_en, auto_en)

        response = jsonify(state.__dict__)
        return response

    def set_amplituner(self, code):
        codes = {0: irk.yamaha['KEY_STANDBY'],
                 1: irk.yamaha['KEY_SLEEP'],
                 2: irk.yamaha['KEY_VOLUME_DOWN'],
                 3: irk.yamaha['KEY_VOLUME_UP']}
        if code != 1:
            self.hand.send_ir_signal(codes[code])
            return jsonify({"status": "OK"})

    def sleep_amplituner(self, sleep_time):
        self.hand.sleep_amplituner(sleep_time)
        return self.hand.get_sleep_timer()

    def get_amp_sleep_state(self):
        return jsonify(self.hand.get_sleep_timer())

    def get_temperatures(self):
        temps = self.hand.get_current_temperatures()
        codes = ['ambient', 'core', 'outdoor']
        response = dict(zip(codes, temps))
        return response

    def get_current_weather(self):
        current = self.hand.get_current_conditions()
        return jsonify(current)

    def get_forecast_daily(self):
        forecast = self.hand.get_forecast_daily()
        return jsonify(forecast)

    def get_forecast_hourly(self):
        forecast = self.hand.get_forecast_hourly()
        return jsonify(forecast)

    def set_auto_led(self, new_state):
        if new_state:
            self.hand.start_auto_led()
        else:
            self.hand.stop_auto_led()

    def set_strip_direction(self, new_value):
        self.hand.set_strip_direction(new_value - 3)

    def set_strip_display_count(self, new_value):
        self.hand.set_strip_display_count(new_value)

    def set_spec_config(self, sensitivity, inertia, freq, speed):
        self.hand.set_sensitivity(sensitivity)
        self.hand.set_inertia(inertia)
        self.hand.set_analyzed_frequency(freq)
        self.hand.set_fade_speed(speed)

#######################################
#   BUTTONS ENDPOINTS
#######################################

    # def weather_switch(self, num, state):
    #     if state:
    #         if num == 1:
    #             self.hand.start_display_weather()
    #             self.hand.set_lcd_background(constants.LCD.ID_0, True)
    #             self.hand.set_lcd_background(constants.LCD.ID_1, True)
    #         elif num == 2:
    #             self.hand.stop_display_weather()
    #             self.hand.set_lcd_background(constants.LCD.ID_0, False)
    #             self.hand.set_lcd_background(constants.LCD.ID_1, False)
    #
    # def auto_led_switch(self, num, state):
    #     if state and num == 3:
    #         if self.hand.auto_is_alive():
    #             self.hand.stop_auto_led()
    #         elif not self.hand.auto_is_alive():
    #             self.hand.start_auto_led()

    def print_menu(self, num, state):
        self.hand.print_menu(num, state)

#######################################
#   BUTTONS ENDPOINTS
#######################################

    def enable_weather(self):
        if self.hand.weather_print_is_alive():
            self.hand.stop_display_weather()
            # self.hand.set_lcd_background(constants.LCD.ID_0, False)
            self.hand.set_lcd_background(constants.LCD.ID_1, False)
        else:
            self.hand.start_display_weather()
            # self.hand.set_lcd_background(constants.LCD.ID_0, True)
            self.hand.set_lcd_background(constants.LCD.ID_1, True)

    def enable_auto_led(self):
        if self.hand.auto_is_alive():
            self.hand.stop_auto_led()
        else:
            self.hand.start_auto_led()

    def vol_up(self):
        code = irk.yamaha['KEY_VOLUME_UP']
        self.hand.send_ir_signal(code)

    def vol_down(self):
        code = irk.yamaha['KEY_VOLUME_DOWN']
        self.hand.send_ir_signal(code)
