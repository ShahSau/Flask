import requests
from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'


@app.route('/')
def index():
    url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4c65edd7a717e23ee614acd543adccec'
    city = 'Vantaa'

    r = requests.get(url.format(city)).json()
    
    weather= {
        'city': city,
        'temperature': r['main']['temp'],
        'feels like': r['main']['feels_like'],
        'High': r['main']['temp_max'],
        'Low': r['main']['temp_min'],
        'description': r['weather'][0]['description'],
        'humidity': r['main']['humidity'],
        'wind speed': r['wind']['speed'],
        'icon': r['weather'][0]['icon'],
    }
    #print(weather)
   
    return render_template("index.html", weather = weather)