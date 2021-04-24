from flask import Flask, jsonify
from handler import MainHandler
import ir_remote_keybinding as irk
import logging
from api import Api


if __name__ == "__main__":
    app = Flask("__name__")
    logging.basicConfig(filename='api_server.log', level=logging.DEBUG)
    hand = MainHandler()
    api = Api(hand)

    app.add_url_rule(rule='/status', view_func=api.getStatus, methods=['GET'])
    app.add_url_rule(rule='/RGB/<int:red>/<int:green>/<int:blue>', view_func=api.setRGB, methods=['POST'])

    app.run(host='0.0.0.0', port=5000)
