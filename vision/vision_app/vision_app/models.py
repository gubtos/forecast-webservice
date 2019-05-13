from vision_app import db

class City(db.Model):
    pk = db.Column(db.Integer, primary_key=True) # database primary key
    id = db.Column(db.Integer, unique=True) # id from climatempo
    name = db.Column(db.String(64)) # city name
    state = db.Column(db.String(64)) # city state
    country = db.Column(db.String(64)) # city country
    forecasts = db.relationship('ForecastWeather', backref='city', lazy=True) # forecasts objects
 
    def __init__(self, id, name, state, country):
        '''
        City object constructor.

        Keyword Arguments:
        id -- id from climatempo API (integer)
        name -- city name (string)
        state -- state name (string)
        country -- country name (string)
        '''
        self.id = id
        self.name = name
        self.state = state
        self.country = country

    def __repr__(self):
        return '<Cidade ' + self.id + '>'

class ForecastWeather(db.Model):
    pk = db.Column(db.Integer, primary_key=True) # database primary key
    city_id = db.Column(db.Integer, db.ForeignKey('city.pk'), nullable=False) # database foreign key
    rain_probability = db.Column(db.Integer)
    rain_precipitation = db.Column(db.Integer)
    temperature_min = db.Column(db.Integer)
    temperature_max = db.Column(db.Integer)
    date = db.Column(db.Date) # forecast day
    
    def __init__(self, city_id, date, rain_probability, rain_precipitation, temperature_min, temperature_max):
        '''
        ForecastWeather constructor

        Keyword Arguments:

        city_id -- forecast API city id (integer)
        date -- date from forecast day (python Date object)
        rain_probability -- integer
        rain_precipitation -- integer
        temperature_min -- integer
        temperature_max -- integer
        '''
        self.city_id = city_id
        self.date = date
        self.rain_probability = rain_probability
        self.rain_precipitation = rain_precipitation
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max

    def __repr__(self):
        return '<Previsão ' + self.city_id + '>'