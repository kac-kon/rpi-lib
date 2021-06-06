from flask import Flask
from application.handler import MainHandler
import logging
from application.api import Api


if __name__ == "__main__":
    app = Flask("__name__")
    logging.basicConfig(filename='api_server.log', level=logging.DEBUG)
    hand = MainHandler()
    api = Api(app, hand)

    app.run(host='0.0.0.0', port=5000)
