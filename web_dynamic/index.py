#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from flask import Flask, render_template, abort
from datetime import datetime
import requests


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

weather_icon = {
        2: 'storm.png',
        3: 'drizzle.png',
        6: 'snow.png'
        }


@app.teardown_appcontext
def close_db(error):
    """ Remove the current Session """
    storage.close()


@app.route('/', strict_slashes=False)
def home():
    """ main page """
    return render_template('index.html')


@app.route('/weather/<string:city_name>', methods=['GET'], strict_slashes=False)
def fast_w(city_name):
    """ FastWeather is alive! """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': '', # enter your API key here
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': str(data['main']['temp'])[:2] + '°C',
            'description': data['weather'][0]['description'],
            'humidity': str(data['main']['humidity']) + '%',
            'pressure': str(data['main']['pressure']) + 'mbar',
            'wind_speed': str(data['wind']['speed']) + 'km/h',
        }
        weather_id = data['weather'][0]['id']
        img_id = int(weather_id / 100)
        if img_id not in weather_icon:
            if img_id == 5:
                if weather_id > 501:
                    img_src = 'heavy_rain.png'
                else:
                    img_src = 'light_rain.png'
            if img_id == 8:
                if weather_id == 800:
                    img_src = 'sunny.png'
                else:
                    img_src = 'cloudy.png'
            if img_id == 7:
                if weather_id > 762:
                    img_src = 'tornado.png'
                else:
                    img_src = 'fog.png'
        else:
            img_src = weather_icon[img_id]

        today = datetime.today()
        date = today.strftime('%A')
        today = today.strftime('%Y-%m-%d')
        return render_template('index-2.html', weather=weather, img_src=img_src, date=date, today=today)
    else:
        abort(404)

@app.route('/weather/forecast/<string:city_name>', methods=['GET'], strict_slashes=False)
def forcast(city_name):
    """ display the weather in 5 days """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
            'q': city_name,
            'appid': '',# enter your API key here
            'units': 'metric'
            }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_list = []
        for forecast in data['list']:
            _dict = {
                    'datetime': forecast['dt_txt'],
                    'temperature': str(forecast['main']['temp']) [:2]+ '°C',
                    'description': forecast['weather'][0]['description'],
                    'humidity': str(forecast['main']['humidity']) + '%',
                    'pressure': str(forecast['main']['pressure']) + 'mbar',
                    'wind_speed': str(forecast['wind']['speed']) + 'km/h',
                    'weather_id': forecast['weather'][0]['id']

            }
            if _dict['datetime'][11:] == '12:00:00':
                forecast_list.append(_dict)

        img_list = []

        for forecast in forecast_list:
            weather_id = forecast['weather_id']
            img_id = int(weather_id / 100)
            if img_id not in weather_icon:
                if img_id == 5:
                    if weather_id > 501:
                        img_src = 'heavy_rain.png'
                    else:
                        img_src = 'light_rain.png'
                if img_id == 8:
                    if weather_id == 800:
                        img_src = 'sunny.png'
                    else:
                        img_src = 'cloudy.png'
                if img_id == 7:
                    if weather_id > 762:
                        img_src = 'tornado.png'
                    else:
                        img_src = 'fog.png'
                img_list.append(img_src)
            else:
                img_src = weather_icon[img_id]
                img_list.append(img_src)

        date_list = []
        date_format = '%Y-%m-%d %H:%M:%S'
        for forecast in forecast_list:
            date_string = forecast['datetime']
            date_obj = datetime.strptime(date_string, date_format)
            today = date_obj.strftime('%A')
            date_list.append(today)
        return render_template('index-3.html', city_name=city_name,forecast_list=forecast_list, img_list=img_list, date_list=date_list)
    else:
        abort(404)

@app.route('/login', strict_slashes=False)
def login():
    """handling login page"""
    return render_template('index-v2.html')

@app.route('/create', strict_slashes=False)
def create_acc():
    """ create new account """
    return render_template('index-v3.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
