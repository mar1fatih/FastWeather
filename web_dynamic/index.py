#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from flask import Flask, render_template, abort
import requests


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def home():
    """ main page """
    return render_template('index.html')


@app.route('/weather/<string:city_name>', strict_slashes=False)
def fast_w(city_name):
    """ FastWeather is alive! """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': 'd5c4c65720c3b2d694d74e90dd9496d9',
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed']
        }
        return render_template('index-2.html', weather=weather)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
