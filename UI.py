## This file is the main file for the UI of the application. It is responsible for creating the UI and handling the user input.
## The UI allows the user to input a city and state, and then displays the weather data for that location. The UI also displays a map of the location.
## The UI also allows the user to load the log of weather data that has been inputted into the database.
## The UI is created using PyQt5, and the map is displayed using the QWebEngineView widget.
## The weather data is retrieved from the weather.gov API, and the geolocation data is retrieved from the U.S. Census Bureau's Geocoding Services API.
## The weather data is then displayed in a QTextEdit widget.
## Kyle Costlow - 4/13/24

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
import requests
import json
import csv
import log
import inputData

class Ui_GetWeather(object):

    def setupUi(self, GetWeather):
        GetWeather.setObjectName("GetWeather")
        GetWeather.resize(900, 600)  #Window size

        font = QtGui.QFont()
        font.setPointSize(5)

        #Label for City
        self.label_city = QtWidgets.QLabel(GetWeather)
        self.label_city.setGeometry(QtCore.QRect(10, 10, 40, 15))
        self.label_city.setFont(font)
        self.label_city.setObjectName("label_city")
        self.label_city.setText("City:")

        #Input for City
        self.lineEdit = QtWidgets.QLineEdit(GetWeather)
        self.lineEdit.setGeometry(QtCore.QRect(50, 10, 150, 15))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        #Label for State
        self.label_state = QtWidgets.QLabel(GetWeather)
        self.label_state.setGeometry(QtCore.QRect(10, 30, 40, 15))
        self.label_state.setFont(font)
        self.label_state.setObjectName("label_state")
        self.label_state.setText("State:")

        #Dropdown for State
        self.comboBox = QtWidgets.QComboBox(GetWeather)
        self.comboBox.setGeometry(QtCore.QRect(50, 30, 150, 15))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
                  "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
                  "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
                  "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        self.comboBox.addItems(states)

        #TextEdit for displaying the weather data/ error messages
        self.textEdit = QtWidgets.QTextEdit(GetWeather)
        self.textEdit.setGeometry(QtCore.QRect(210, 10, 780, 35))
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        #Button "Load Logs"
        self.loadLogsButton = QtWidgets.QPushButton(GetWeather)
        self.loadLogsButton.setGeometry(QtCore.QRect(10, 575, 100, 20))
        self.loadLogsButton.setFont(font)
        self.loadLogsButton.setText("Load Logs")
        self.loadLogsButton.clicked.connect(self.print_log) # - Calvin (4/13/24)

        #ButtonBox for OK/Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(GetWeather)
        self.buttonBox.setGeometry(QtCore.QRect(775, 575, 115, 20))
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.get_weather)
        self.buttonBox.rejected.connect(GetWeather.reject)

        #Create a QWebEngineView to display the map
        self.webView = QtWebEngineWidgets.QWebEngineView(GetWeather)
        self.webView.setGeometry(QtCore.QRect(10, 50, 880, 520))  # Adjusted to make the map larger and fit the space

        #Parse the CSV file to get the city and state data
        self.city_state_set = set()
        with open('us_cities_states_counties.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                city_state = (row['City'].lower(), row['State short'].lower())
                self.city_state_set.add(city_state)

    def get_weather(self):
        city = self.lineEdit.text().strip().lower()
        state = self.comboBox.currentText().strip().lower()
        location = f"{city}, {state}"

        if (city, state) not in self.city_state_set:
            self.textEdit.setText(f"The city-state combination of {city.title()}, {state.upper()} is not valid.")
            return

        # Set the URL of the QWebEngineView to a Google Maps URL for the location
        maps_url = f"https://www.google.com/maps/place/{location.replace(' ', '+')}"
        self.webView.setUrl(QtCore.QUrl(maps_url))

        # Get coordinates from U.S. Census Bureau's Geocoding Services API
        formattedadds = f"city={city}&state={state}"
        url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street=100+Main+St&{formattedadds}&benchmark=2020&format=json"
        geoinfo = requests.get(url)
        data = geoinfo.json()
        if data['result']['addressMatches']:
            coordinates = data['result']['addressMatches'][0]['coordinates']
            lat = coordinates['y']
            lon = coordinates['x']

            # Get weather data from weather.gov API
            weather_data = self.get_weather_data(lat, lon)
            if weather_data:
                self.textEdit.setText(weather_data)

                #The following snippet - Calvin (4/13/24) - Insert data into the database
                db_file = 'weather.db'
                db = inputData.Weather(db_file)  # - this is the database object
                weather_entry = {
                "city": city,
                "state": state,
                "weather": str(weather_data)
                } 
                db.insertData(weather_entry)
                #End of snippet
                
            else:
                self.textEdit.setText("Could not get weather data.")
        else:
            self.textEdit.setText("Could not get geolocation data.")

    def get_weather_data(self, lat, lon):
        weather_s = f"https://api.weather.gov/points/{lat},{lon}"
        response = requests.get(weather_s)
        js = json.loads(response.text)
        forecast_URL = js['properties']['forecast']
        final_response = requests.get(forecast_URL)
        js = json.loads(final_response.text)
        return js['properties']['periods'][0]['detailedForecast']

    ## This function prints the log of weather data that has been inputted into the database
    ## Calvin Ruch - 4/13/24
    def print_log(self):
        db_file = 'weather.db'
        db = inputData.Weather(db_file)  # - this is the database object
        output = log.log(db.getData())  #- this is the log object
        output.print_log()  # - this prints the log object

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GetWeather = QtWidgets.QDialog()
    ui = Ui_GetWeather()
    ui.setupUi(GetWeather)
    GetWeather.show()
    sys.exit(app.exec())
