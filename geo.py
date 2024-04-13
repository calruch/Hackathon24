#! /usr/bin/env python3

import json
from geopy.exc import GeocoderTimedOut
import requests

def getWeather(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        # Attempt to geocode the location
        geo = geolocator.geocode(location)
        if geo:
            # get the latitude and longitude of the location
            lat = geo.latitude
            lon = geo.longitude
            # use the latitude and longitude to get the weather
            weather_s = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
            response = requests.get(weather_s)
            js = json.loads(response.text)
            forecast_URL = js['properties']['forecast']
            final_response = requests.get(forecast_URL)
            js = json.loads(final_response.text)
            return js['properties']['periods'][0]['detailedForecast']
        else:
            return None
    except GeocoderTimedOut:
        return "Geocoding service timed out"        
