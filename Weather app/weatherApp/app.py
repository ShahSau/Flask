import requests
from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable =False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name = new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4c65edd7a717e23ee614acd543adccec'
    
    weather_data =[]

    for city in cities:
        r = requests.get(url.format(city.name)).json()
    
        weather= {
            'city': city.name,
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'High': r['main']['temp_max'],
            'pressure': r['main']['pressure'],
            'Low': r['main']['temp_min'],
            'description': r['weather'][0]['description'],
            'humidity': r['main']['humidity'],
            'wind_speed': r['wind']['speed'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(weather)
   
    return render_template("index.html", weather_data = weather_data)