from flask import Flask
from handler import MainHandler
import logging
from api import Api


if __name__ == "__main__":
    app = Flask("__name__")
    logging.basicConfig(filename='api_server.log', level=logging.DEBUG)
    hand = MainHandler()
    api = Api(app, hand)

    hand.register_button_callback(api.weatherSwitch)

    app.run()
