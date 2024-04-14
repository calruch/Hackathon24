## Project Weatherapp_The Brit & others


## Problem
Imagine you are planning a trip to a new city and you want to know the weather conditions there. 
However, you don't want to rely on generic weather forecasts. 
You want a weather app that can provide accurate and up-to-date weather information for any given location. 
This app should also display a map of the location so that you can get a better understanding of the area. 
Additionally, you want the ability to log all the weather queries you make, so that you can review them later. 
Your problem is to develop a weather app that fulfills all these requirements and provides a seamless user experience.
This is all providing they have a way to run a python project on a device.

## Description 
This is a weather app that will take in a city and state as a parameter from text boxes inside of a gui 
then uses an API call to find the longitude and lattitude. 
From this the program will then use the weather.gov api to find the weather of the given location
Simultaneously the program will load in the google maps that location.
After the weather has been retrieved, it will upload that information to a database inside the weather.db file.
When the logs button is pressed it will load up a result of all of the queries made to the database inside of a text file, nicely formatted.

## Technical Difficulties
Some of the technical difficulties we ran into was converting city/state combinations 
into coordinates to feed into the weather.gov API; learning how to make a GUI in Python; 
and preventing duplicate entries into the database.

## Languages 
We used Python for the Frontend GUI 
we used Python for the background operations
For the Data management we used sqlite3
