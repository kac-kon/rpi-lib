from flask import Flask
from flask_restful import Api, Resource

app = Flask("__name__")
api = Api(app)


class RpiServer(Resource):
    def get(self):
        return "ss"


if __name__ == "__main__":
    app.run(debug=True)