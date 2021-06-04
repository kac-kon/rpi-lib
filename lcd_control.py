import time
import constants
import custom_chars
import drivers.lcd_driver
import threading
from variables import LcdVar
from weather import Weather
from menu import Menu


class Displays:
    def __init__(self, weather: Weather, menu: Menu):
        self._var = LcdVar()
        self._weather = weather
        self._menu = menu
        self._lcd0 = drivers.lcd_driver.lcd(constants.LCD.ID_0, backlight=self._var.lcd2_backlight)
        self._lcd1 = drivers.lcd_driver.lcd(constants.LCD.ID_1, backlight=self._var.lcd4_backlight)

        self._exit_datetime_event = threading.Event()
        self._thread_print_datetime = threading.Thread()
        self._thread_print_datetime_weather = threading.Thread()
        self._exit_print_weather_event = threading.Event()

        self.current_content = "root"
        self.current_node = 0
        self.print_menu()
        # self.print_weather()

        # self._var.register_lcd_callback(self.set_backlight)

    def set_backlight(self, lcd_id, state):
        if lcd_id == constants.LCD.ID_0:
            self._lcd0.backlight(state)
            self._var.lcd2_backlight = bool(state)
        elif lcd_id == constants.LCD.ID_1:
            self._lcd1.backlight(state)
            self._var.lcd4_backlight = bool(state)

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
        self._lcd1.lcd_display_string(conditions['temp_outdoor'], 2, 6)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(conditions['temp_ambient'], 2, 12)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(
            conditions['pressure'] + 'hPa ' + conditions['humidity'] + '% ' + conditions['wind_speed'] + 'km/h ', 3)
        self._lcd1.lcd_write_char(1)
        self._lcd1.lcd_display_string(conditions['detailed_status'], 4)
        if len(conditions['rain']) > 3:
            rain = str(round(float(conditions['rain'][7:-1]), 1))
            self._lcd1.lcd_display_string(rain + 'mm', 4, 15)

    def start_print_datetime_short(self):
        if self._thread_print_datetime.is_alive():
            self.exit_print_datetime_short()
        self._exit_datetime_event.clear()
        self._thread_print_datetime = threading.Thread(target=self._start_print_datetime_short)
        self._thread_print_datetime.start()

    def _start_print_datetime_short(self):
        t = time.time()
        self._display_weather()
        while not (self._exit_datetime_event.is_set()):
            dt = self._weather.get_datetime_short()
            self._lcd1.lcd_display_string(dt, 1)
            time.sleep(.1)
            if (time.time() - t) > 60 * 10:
                t = time.time()
                self._lcd1.lcd_clear()
                self._display_weather()
        self._exit_datetime_event.clear()

    def exit_print_datetime_short(self):
        self._exit_datetime_event.set()
        self._thread_print_datetime.join()
        self._lcd1.lcd_clear()
        # print('thread finished')

    def get_lcd_background(self):
        return [self._var.lcd2_backlight, self._var.lcd4_backlight]

    def print_menu(self):
        self._lcd0.lcd_clear()
        self._lcd0.lcd_load_custom_chars([custom_chars.arrows[0], custom_chars.arrows[2]])
        self._lcd0.lcd_write(0x80)
        self._lcd0.lcd_write_char(1)
        menu = self._menu.getChildrenText(self.current_content)
        # if self.current_node >= len(menu) - 1:
        #     self.current_node = 0
        if self.current_node < 0:
            self.current_node = len(menu) - 1
        self._lcd0.lcd_display_string(menu[self.current_node % len(menu)], 1, 1)
        if len(menu) > 1:
            self._lcd0.lcd_display_string(menu[(self.current_node+1) % len(menu)], 2, 1)

    def print_menu_back(self):
        self._lcd0.lcd_write(0x80)
        self._lcd0.lcd_write_char(0)
