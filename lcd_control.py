import time
import constants
import custom_chars
import drivers.lcd_driver
import threading
from variables import LcdVar
from weather import Weather


class Displays:
    def __init__(self):
        self._var = LcdVar()
        self._weather = Weather()
        self._lcd0 = drivers.lcd_driver.lcd(constants.LCD.ID_0, backlight=self._var.lcd2_backlight)
        self._lcd1 = drivers.lcd_driver.lcd(constants.LCD.ID_1, backlight=self._var.lcd4_backlight)

        self._exit_datetime_event = threading.Event()
        self._thread_print_datetime = threading.Thread()
        self.print_weather()

        self._var.register_lcd_callback(self.set_backlight)

    def set_backlight(self, lcd_id, state):
        if lcd_id == constants.LCD.ID_0:
            self._lcd0.backlight(state)
        elif lcd_id == constants.LCD.ID_1:
            self._lcd1.backlight(state)

    def print_weather(self):
        self._display_weather()
        # self.start_print_datetime_short()

    def _display_weather(self):
        conditions = self._weather.get_current_conditions()
        self._lcd1.lcd_clear_line(20, 2)
        self._lcd1.lcd_clear_line(20, 3)
        self._lcd1.lcd_clear_line(20, 4)
        self._lcd1.lcd_load_custom_chars([custom_chars.celc, custom_chars.arrows[int(conditions['wind_direction'])]])
        self._lcd1.lcd_display_string(conditions['temp'], 2)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(conditions['temp_feels'], 2, 6)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(
            conditions['pressure'] + 'hPa ' + conditions['humidity'] + '% ' + conditions['wind_speed'] + 'km/h ', 3)
        self._lcd1.lcd_write_char(1)
        self._lcd1.lcd_display_string(conditions['detailed_status'], 4)
        if len(conditions['rain']) > 3:
            rain = str(round(float(conditions['rain'][7:-1]), 1))
            self._lcd1.lcd_display_string(rain + 'mm', 4, 15)

    def start_print_datetime_short(self):
        self._exit_datetime_event.clear()
        self._thread_print_datetime = threading.Thread(target=self._start_print_datetime_short)
        self._thread_print_datetime.start()

    def _start_print_datetime_short(self):
        while not (self._exit_datetime_event.is_set()):
            dt = self._weather.get_datetime_short()
            self._lcd1.lcd_display_string(dt, 1)
            time.sleep(.1)
        self._exit_datetime_event.clear()

    def exit_print_datetime_short(self):
        self._exit_datetime_event.set()
        self._thread_print_datetime.join()
        print('thread finished')

    def get_lcd_background(self):
        print([self._var.lcd2_backlight, self._var.lcd4_backlight])
        return [self._var.lcd2_backlight, self._var.lcd4_backlight]
