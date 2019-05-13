import json
from datetime import datetime
from flask import request, abort, jsonify, Response
from flask.views import MethodView
from sqlalchemy.sql import func
from sqlalchemy import and_
from vision_app import app, db
from vision_app.config import CLIMATEMPO_API_KEY
from .models import City, ForecastWeather
from .utils import save_city_data, create_city
import requests
from traceback import print_exc

# Views are declared here

class CityView(MethodView):
    def get(self, id=None):
        try:
            if not id:
                # rule to register city '.../cidade?id=<ID_DA_CIDADE>' like POST method
                id = request.args.get('id')
                if id is not None:
                    res = create_city(id)
                else:
                    # if not have id, return all cities
                    cities = City.query.all()
                    res = []
                    for city in cities:
                        res.append(
                            {
                                "id": city.id,
                                "cidade": city.name,
                                "estado": city.state,
                                "pais": city.country
                            }
                        )
            else:
                city = City.query.filter_by(id=id).first()

                if not city:
                    # if city dont exist return 404 error response
                    abort(404)
                else:
                    # if have id '.../<id>/' return json info from city with forecast weather
                    forecasts = []
                    for forecast in city.forecasts:
                        forecasts.append({
                            "dia": forecast.date.strftime("%d/%m/%Y"),
                            "probabilidade": forecast.rain_probability, 
                            "precipitacao": forecast.rain_precipitation,
                            "min": forecast.temperature_min,
                            "max": forecast.temperature_max
                        })
                    res = {
                        "id": city.id,
                        "cidade": city.name,
                        "estado": city.state,
                        "pais": city.country,
                        "previsao": forecasts
                    }
            return jsonify(res)
        except:
            print_exc()
            abort(404)

    def post(self):
        try:
            # get id param from post method with city id from api from climatempo 
            id = request.form.get('id')
            res = create_city(id)
            return jsonify(res)

        except:
            print_exc()
            abort(404)

    def delete(self):
        city = City.query.filter_by(id=id).first()
        if not city:
            abort(404)
        else:
            # TODO
            pass

class AnalysisView(MethodView):
    def get(self):
        try:
            # get analysis data when fields data_inicial and data_final are provided
            start_date_str = request.args.get("data_inicial")
            end_date_str = request.args.get("data_final")

            # if not provided return error response
            if start_date_str is None or end_date_str is None:
                raise(BaseException("Os parâmetros data_inicial e data_final são obrigatórios"))

            else:
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
                end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()

                # query to get max temperature
                query = ForecastWeather.query.filter(ForecastWeather.date.between(start_date, end_date))
                temperature_max_forecast = query.order_by(ForecastWeather.temperature_max.desc()).first()
                
                analysis = {
                    'data_inicial' : start_date_str,
                    'data_final' : end_date_str
                }

                if temperature_max_forecast is not None:
                    # get data from city and convert to json
                    temperature_max = temperature_max_forecast.temperature_max
                    city_id = temperature_max_forecast.city_id
                    city = City.query.get(city_id)
                    
                    analysis = {
                        **analysis,
                        'max': temperature_max,
                        'cidade': city.name,
                        'id': city.id
                    }
                
                # query to get average rain precipitation from each city
                query = ForecastWeather.query.with_entities(
                    ForecastWeather.city_id, 
                    func.avg(ForecastWeather.rain_precipitation)
                ).group_by(ForecastWeather.city_id).order_by(ForecastWeather.city_id).filter(ForecastWeather.date.between(start_date, end_date))

                # convert query to json
                avgs = []

                for avg in query:
                    id, city_avg = avg
                    city = City.query.get(id)
                    avgs.append({
                        'cidade': city.name,
                        'precipitacaoMedia': city_avg,
                        'id': city.id
                    })
                
                if len(avgs) > 0:
                    analysis = {**analysis, 'precipitacaoPorCidade':avgs}

                return jsonify(analysis)
        except Exception as e:
            print_exc()
            abort(Response(e))
