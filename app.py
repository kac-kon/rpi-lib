from flask import Flask
from handler import MainHandler
import logging
from api import Api


if __name__ == "__main__":
    app = Flask("__name__")
    logging.basicConfig(filename='api_server.log', level=logging.DEBUG)
    hand = MainHandler()
    api = Api(hand)
    hand.register_button_callback(api.weatherSwitch)

    app.add_url_rule(rule='/status', view_func=api.getStatus, methods=['GET'])
    app.add_url_rule(rule='/RGB/<int:red>/<int:green>/<int:blue>', view_func=api.setRGB, methods=['POST'])
    app.add_url_rule(rule='/RGB', view_func=api.getRGB, methods=['GET'])
    app.add_url_rule(rule='/switch/<int:switchID>/<int:state>', view_func=api.setSwitches, methods=['POST'])
    app.add_url_rule(rule='/brightness/<int:brightness>', view_func=api.setBrightness, methods=['POST'])
    app.add_url_rule(rule='/state', view_func=api.getCurrentState, methods=['GET'])
    app.add_url_rule(rule='/amplituner/<int:code>', view_func=api.setAmplituner, methods=['POST'])
    app.add_url_rule(rule='/temperatures', view_func=api.getTemperatures, methods=['GET'])
    app.add_url_rule(rule='/weather', view_func=api.getCurrentWeather, methods=['GET'])
    app.add_url_rule(rule='/forecast/daily', view_func=api.getForecastDaily, methods=['GET'])
    app.add_url_rule(rule='/forecast/hourly', view_func=api.getForecastHourly, methods=['GET'])

    app.run(host='0.0.0.0', port=5000)
