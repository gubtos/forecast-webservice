import requests
import json
from datetime import date, datetime
from traceback import print_exc

from vision_app import db
from vision_app.config import CLIMATEMPO_API_KEY

from .models import City, ForecastWeather

def update():
    '''Update forecasts weather from all cities'''
    cities = City.query.all()
    for city in cities:
        save_city_data(city.id)
        # TODO

def save_city_data(id):
    '''
    Save city forecast weather

    Keyword Arguments:
    id -- id from climatempo API (integer)
    '''
    try:
        city = City.query.filter_by(id=id).first()
        if city is not None:
            # request in climatempo API
            url = "http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{}/days/15?token={}".format(id, CLIMATEMPO_API_KEY)
            resp = requests.get(url)
            resp.raise_for_status()
            json_data = resp.json()

            # save results in database
            for day in json_data['data']:
                date = datetime.strptime(day['date'], "%Y-%m-%d").date()
                forecast = ForecastWeather(
                    city_id = city.pk, 
                    date = date, 
                    rain_probability = day['rain']['probability'], 
                    rain_precipitation = day['rain']['precipitation'], 
                    temperature_min = day['temperature']['min'], 
                    temperature_max = day['temperature']['max'] 
                )
                db.session.add(forecast)
            db.session.commit()
        else:
            raise(BaseException("City not exist in database"))
    except:
        print_exc()
        raise(BaseException("Error when save city data"))

def create_city(id):
    ''' Create and save city in database
    
    Keyword Arguments
    id -- climatempo API city id (integer) 
    '''

    # use request lib to acess climatempo api
    url = "http://apiadvisor.climatempo.com.br/api/v1/locale/city/{}?token={}".format(id, CLIMATEMPO_API_KEY)
    r = requests.get(url)
    r.raise_for_status()
    json_data = r.json()
    
    name, state, country = json_data["name"], json_data["state"], json_data["country"] 
    
    # create City object and save in dabase
    city = City(id, name, state, country)

    db.session.add(city)
    db.session.commit()

    save_city_data(id)

    # return City created
    return {
        'id': city.id,
        'nome': city.name,
        'estado': city.state,
        'pais': city.country
    }