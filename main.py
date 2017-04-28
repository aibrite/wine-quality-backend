from routebase import WineBase
from flask import Flask, request
from os import environ
from flask_cors import CORS, cross_origin


app = Flask('Wine Quality Prediction')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

route_handler = WineBase()


@app.route("/")
def home_route():
    return route_handler.home()


@app.route('/predict', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def prediction():
    return route_handler.predict_wine()


def run():
    if __name__ == '__main__':
        print('Initializing Wine Quality Prediction App')
        print('Running on', __name__)
        server_address = '0.0.0.0'
        server_port = int(environ.get('PORT', 5000))
        print('Launch successful at port:', server_port)
        app.run(server_address, server_port)


run()
