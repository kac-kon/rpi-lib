import time
import constants
import custom_chars
import drivers.lcd_driver
import threading
from variables import Vars
from weather import Weather

class Displays:
    def __init__(self):
        self._weather = Weather()
        self._lcd0 = drivers.lcd_driver.lcd(constants.LCD.id(0))
        self._lcd1 = drivers.lcd_driver.lcd(constants.LCD.id(1))
        self._lcd0.backlight(constants.INITIALS.LCD2_BACKLIGHT)
        self._lcd1.backlight(constants.INITIALS.LCD4_BACKLIGHT)
        
    
    def set_backlight(self, lcd_id, state):
        if lcd_id == 0 : self._lcd0.backlight(state)
        elif lcd_id == 1 : self._lcd1.backlight(state)
    
    
    
    def _display_weather(self):
        conditions = self._weather.get_current_conditions()
        self._lcd1.lcd_clear_line(20,2)
        self._lcd1.lcd_clear_line(20,3)
        self._lcd1.lcd_load_custom_chars([custom_chars.celc, custom_chars.arrows[int(conditions['wind_direction'])]])
        self._lcd1.lcd_display_string(conditions['temp_now'], 2)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(conditions['temp_feels'], 2, 6)
        self._lcd1.lcd_write_char(0)
        self._lcd1.lcd_display_string(conditions['pressure_now'] + 'hPa ' + conditions['humidity'] + '% ' + conditions['wind_speed'] + 'km/h ', 3)
        self._lcd1.lcd_write_char(1)