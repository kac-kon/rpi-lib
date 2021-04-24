from handler import MainHandler
from flask import jsonify, request


class Api:
    def __init__(self, hand: MainHandler):
        self.hand = hand

    @staticmethod
    def getStatus():
        return jsonify([{'status': 'OK'}])

    def setRGB(self, red, green, blue):
        self.hand.set_colors([red, green, blue])
        colors = self.hand.get_colors()
        codes = ['red', 'green', 'blue']
        response = dict(zip(codes, colors))
        return response
