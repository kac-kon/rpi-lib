import datetime
import time

import glob
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

import constants


class Weather:
    def __init__(self):
        self._cords = [50.06860205597571, 19.906051141042095]
        self._config_dict = get_default_config()
        self._config_dict['language'] = 'en'
        self._owm = OWM('5107288b7cd05e5e4d3a167c10eb87e4', self._config_dict)
        self._manager = self._owm.weather_manager()
        self._one_call = self._manager.one_call(self._cords[0], self._cords[1])
        self._current_conditions = self._one_call.current

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
    def _read_temp_raw(device: int):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[device]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_temp(self, device: int):
        lines = self._read_temp_raw(device)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw(device)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def _update_weather(self):
        self._one_call = self._manager.one_call(self._cords[0], self._cords[1])
        self._current_conditions = self._one_call.current

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
                'temp_ambient': str(self.get_temp(constants.TEMP.AMBIENT)),
                'temp_outdoor': str(self.get_temp(constants.TEMP.OUTDOOR))
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
                'temp_ambient': str(self.get_temp(constants.TEMP.AMBIENT)),
                'temp_outdoor': str(self.get_temp(constants.TEMP.OUTDOOR))
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
            'temp_ambient': str(self.get_temp(constants.TEMP.AMBIENT)),
            'temp_outdoor': str(self.get_temp(constants.TEMP.OUTDOOR))
        }

        return conditions

    def get_current_conditions(self):
        self._update_weather()
        return self._get_current_values()

    def get_forecast_daily(self):
        self._update_weather()
        return self._get_forecast_daily()

    def get_forecast_hourly(self):
        self._update_weather()
        return self._get_forecast_hourly()
