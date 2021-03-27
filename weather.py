import datetime
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config


class Weather:
    def __init__(self):
        self._cords = [50.06860205597571, 19.906051141042095]
        self._config_dict = get_default_config()
        self._config_dict['language'] = 'en'
        self._owm = OWM('5107288b7cd05e5e4d3a167c10eb87e4', self._config_dict)
        self._manager = self._owm.weather_manager()
        self._current_conditions = self._manager.weather_at_coords(self._cords[0], self._cords[1]).weather
        
    
    def _degrees_to_cardinal(self, d):
        dirs = [0,1,2,3,4,5,6,7]
        ix = round((d+180) / (360./len(dirs)))
        return dirs[ix % len(dirs)]
    
    def get_datetime_long(self):
        return str(datetime.datetime.now().today())[:19]
    
    def get_datetime_short(self):
        tmp = str(datetime.datetime.now().today())
        return "{}.{} {}".format(tmp[8:10], tmp[5:7], tmp[11:19])
    
    def get_datetime_shortest(self):
        tmp = str(datetime.datetime.now().today())
        return "{}.{} {}".format(tmp[8:10], tmp[5:7], tmp[11:16])
    
    def get_time(self):
        return str(datetime.datetime.now().today())[11:19]
    
    def get_time_short(self):
        return str(datetime.datetime.now().today())[11:16]
    
    def get_date_long(self):
        return str(datetime.datetime.now().today())[:10]
    
    def get_date_short(self):
        tmp = str(datetime.datetime.now().today())
        return "{}.{}".format(tmp[8:10], tmp[5:7])
    
    def _update_weather(self):
        self._current_conditions = self._manager.weather_at_coords(self._cords[0], self._cords[1]).weather
    
    def _get_values(self):
        conditions = {
        'temp_now' : str(round(self._current_conditions.temperature('celsius')['temp'], 1)),
        'temp_feels' : str(round(self._current_conditions.temperature('celsius')['feels_like'], 1)),
        'pressure_now' : str(self._current_conditions.pressure['press']),
        'rain' : str(self._current_conditions.rain),
        'snow' : str(self._current_conditions.snow),
        'wind_speed' : str(int(round(self._current_conditions.wind(unit='km_hour')['speed'], 0))),
        'wind_direction' : str(self._degrees_to_cardinal(self._current_conditions.wind(unit='km_hour')['deg'])),
        'humidity' : str(self._current_conditions.humidity),
        'humidex' : str(self._current_conditions.humidex),
        'ref_time' : str(self._current_conditions.reference_time('date') + datetime.timedelta(hours=1)),
        'status' : str(self._current_conditions.status),
        'detailed_status' : str(self._current_conditions.detailed_status),
        'clouds' : str(self._current_conditions.clouds)
        }
        
        return conditions

    def get_current_conditions(self):
        self._update_weather()
        return self._get_values()
