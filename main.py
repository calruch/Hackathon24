#! /usr/bin/env python3

import inputData
import requests
import json

def main():   
    dbFile = "weather.db"
    weather_info = "Dark" # self.get_weather("Spokane")

    weather_entry = {
        "city": "San Antonio",
        "state": "TX",
        "weather": str(weather_info)
    } 

    

    '''
    dbFile = "weather.db"
    # Variables below need to be defined
    city_name = ...
    state_name = ...
    weather_info = ... load in from API call
    weather_entry = {
        "city": city_name,
        "state": state_name,
        "weather": str(weather_info)
    } 
    db = inputData.Weather(dbFile)
    db.insertData(weather_entry)
    '''

    print(db.getData())
    
    """ Used for testing - not to be used for production
    print("Deleting data")
    db.deleteData()
    print(db.getData())
    """    



if __name__ == "__main__":
    main()