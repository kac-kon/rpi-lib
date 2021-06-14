import datetime
import threading

import subprocess, tempfile
import time

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import TimeoutError



class Weather:
    def __init__(self):
        self._cords = [50.06860205597571, 19.906051141042095]
        self._config_dict = get_default_config()
        self._config_dict['language'] = 'en'
        self._owm = OWM('5107288b7cd05e5e4d3a167c10eb87e4', self._config_dict)
        self._manager = self._owm.weather_manager()
        self._one_call = self._manager.one_call(self._cords[0], self._cords[1])
        self._current_conditions = self._one_call.current
        self._current_temperatures = self._read_temp_raw()
        self._update_thread = threading.Thread(target=self._update_weather_loop)
        self._update_thread.start()

    @staticmethod
    def _degrees_to_cardinal(d):
        dirs = [0, 1, 2, 3, 4, 5, 6, 7]
        ix = round((d + 180) / (360. / len(dirs)))
        return dirs[ix % len(dirs)]

    @staticmethod
    def get_datetime_long():
        return str(datetime.datetime.now().today())[:19]

    @staticmethod
    def get_datetime_short():
        tmp = str(datetime.datetime.now().today())
        return "{}.{} {}".format(tmp[8:10], tmp[5:7], tmp[11:19])

    @staticmethod
    def get_datetime_shortest():
        tmp = str(datetime.datetime.now().today())
        return "{}.{} {}".format(tmp[8:10], tmp[5:7], tmp[11:16])

    @staticmethod
    def get_time():
        return str(datetime.datetime.now().today())[11:19]

    @staticmethod
    def get_time_short():
        return str(datetime.datetime.now().today())[11:16]

    @staticmethod
    def get_date_long():
        return str(datetime.datetime.now().today())[:10]

    @staticmethod
    def get_date_short():
        tmp = str(datetime.datetime.now().today())
        return "{}.{}".format(tmp[8:10], tmp[5:7])

    @staticmethod
    def _read_temp_raw():
        with tempfile.TemporaryFile() as tempf:
            proc = subprocess.Popen("sensors | grep temp1", stdin=subprocess.PIPE, shell=True, stdout=tempf)
            proc.wait()
            tempf.seek(0)
            lines = tempf.readlines()
            temps = []
            for i in range(3):
                line = str(lines[i])
                start_pos = (line.find('+') + 1 or line.find('-'))
                end_pos = line.find('\\')
                temps.append(float(line[start_pos: end_pos]))
            return temps

    def get_temps(self):
        self._current_temperatures = self._read_temp_raw()
        return self._current_temperatures

    def _update_weather(self):
        t1 = threading.Thread(target=self._update_temperatures())
        t2 = threading.Thread(target=self._update_one_call())
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self._current_conditions = self._one_call.current

    def _update_weather_loop(self):
        while True:
            try:
                self._update_weather()
            except TimeoutError:
                time.sleep(6)
                print("exception handled")
            except Exception:
                pass
            time.sleep(10)

    def _update_temperatures(self):
        self._current_temperatures = self._read_temp_raw()

    def _update_one_call(self):
        self._one_call = self._manager.one_call(self._cords[0], self._cords[1])

    def _get_forecast_daily(self):
        forecast = []
        for i in range(len(self._one_call.forecast_daily)):
            conditions = {
                'temp': str(round(self._one_call.forecast_daily[i].temperature('celsius')['day'], 1)),
                'temp_feels': str(round(self._one_call.forecast_daily[i].temperature('celsius')['feels_like_day'], 1)),
                'pressure': str(self._one_call.forecast_daily[i].pressure['press']),
                'rain': str(self._one_call.forecast_daily[i].rain),
                'snow': str(self._one_call.forecast_daily[i].snow),
                'wind_speed': str(int(round(self._one_call.forecast_daily[i].wind(unit='km_hour')['speed'], 0))),
                'wind_direction': str(
                    self._degrees_to_cardinal(self._one_call.forecast_daily[i].wind(unit='km_hour')['deg'])),
                'humidity': str(self._one_call.forecast_daily[i].humidity),
                'humidex': str(self._one_call.forecast_daily[i].humidex),
                'ref_time': str(self._one_call.forecast_daily[i].reference_time('date') + datetime.timedelta(hours=2)),
                'status': str(self._one_call.forecast_daily[i].status),
                'detailed_status': str(self._one_call.forecast_daily[i].detailed_status),
                'clouds': str(self._one_call.forecast_daily[i].clouds),
                'icon': str(self._one_call.forecast_daily[i].weather_icon_name),
            }
            forecast.append(conditions)
        return forecast

    def _get_forecast_hourly(self):
        forecast = []
        for i in range(len(self._one_call.forecast_hourly)):
            conditions = {
                'temp': str(round(self._one_call.forecast_hourly[i].temperature('celsius')['temp'], 1)),
                'temp_feels': str(round(self._one_call.forecast_hourly[i].temperature('celsius')['feels_like'], 1)),
                'pressure': str(self._one_call.forecast_hourly[i].pressure['press']),
                'rain': str(self._one_call.forecast_hourly[i].rain),
                'snow': str(self._one_call.forecast_hourly[i].snow),
                'wind_speed': str(int(round(self._one_call.forecast_hourly[i].wind(unit='km_hour')['speed'], 0))),
                'wind_direction': str(
                    self._degrees_to_cardinal(self._one_call.forecast_hourly[i].wind(unit='km_hour')['deg'])),
                'humidity': str(self._one_call.forecast_hourly[i].humidity),
                'humidex': str(self._one_call.forecast_hourly[i].humidex),
                'ref_time': str(self._one_call.forecast_hourly[i].reference_time('date') + datetime.timedelta(hours=2)),
                'status': str(self._one_call.forecast_hourly[i].status),
                'detailed_status': str(self._one_call.forecast_hourly[i].detailed_status),
                'clouds': str(self._one_call.forecast_hourly[i].clouds),
                'icon': str(self._one_call.forecast_hourly[i].weather_icon_name),
            }
            forecast.append(conditions)
        return forecast

    def _get_current_values(self):
        conditions = {
            'temp': str(round(self._current_conditions.temperature('celsius')['temp'], 1)),
            'temp_feels': str(round(self._current_conditions.temperature('celsius')['feels_like'], 1)),
            'pressure': str(self._current_conditions.pressure['press']),
            'rain': str(self._current_conditions.rain),
            'snow': str(self._current_conditions.snow),
            'wind_speed': str(int(round(self._current_conditions.wind(unit='km_hour')['speed'], 0))),
            'wind_direction': str(self._degrees_to_cardinal(self._current_conditions.wind(unit='km_hour')['deg'])),
            'humidity': str(self._current_conditions.humidity),
            'humidex': str(self._current_conditions.humidex),
            'ref_time': str(self._current_conditions.reference_time('date') + datetime.timedelta(hours=2)),
            'status': str(self._current_conditions.status),
            'detailed_status': str(self._current_conditions.detailed_status),
            'clouds': str(self._current_conditions.clouds),
            'icon': str(self._current_conditions.weather_icon_name),
            'temp_ambient': str(self._current_temperatures[0]),
            'temp_outdoor': str(self._current_temperatures[2]),
            'temp_core': str(self._current_temperatures[1])
        }

        return conditions

    def get_current_conditions(self):
        # self._update_weather()
        return self._get_current_values()

    def get_forecast_daily(self):
        # self._update_weather()
        forecast = self._get_forecast_daily()
        return forecast

    def get_forecast_hourly(self):
        # self._update_weather()
        return self._get_forecast_hourly()
