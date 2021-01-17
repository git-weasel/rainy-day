## general order #1: test code marked with %@ for later removal

## import required modules and methods
import seaborn as sns
import json
import requests
import time
import datetime
import pandas as pd
import numpy as np

# Bokeh libraries
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel

## assign National Weather Service API URL to string variable
api_base_url = 'https://api.weather.gov/points/'

## create reference variables for later use
city_or_place = ''
state = ''

## NWS report weather conditions in 2.5km^2 grids. 
## As grid numbers are obscure, we will collect
## geocordinates as input from the user and the API
## will kindly map to the relevant grid reference.

## Short explanation of what the program offers and what
## information is required to use it effectively.

#print("""
#Hello. I can provide current weather information for you. 
#Before we start, please have ready the latitude and 
#longitute for the location you'd like to obtain
#weather input about. Please format the geocordinates 
#as using the simple decimal standard coordinates: 

#15.23456, -30.67890.

#DO NOT use any of the following common formats:
#(1) Decimal Degrees (DD)
#(2) Degrees and Decimal Minutes (DDM)
#(3) Degrees, Minutes, and Seconds (DMS)
#
#ONLY SIMPLE DECIMAL STANDARD COORDINATES WILL WORK
#
#""")

## %@ 

lat = '37.910076'
lon = '-122.065186'

## Receive the latitude from the user's input.

#lat = str(input("Please input the latitude.\n"))

## Receive the longitude from the user's input.

#lon = str(input("Please input the latitude.\n"))

## Print inputs for review by user.

#print(f"""
#So you would like to obtain weather information for:
#{lat}, {lon}
#""")

confirm = input("""Is the correct?
Enter 'A' for 'affirmative' or 'N' for 'negative', please.\n""")

if confirm == 'A':
	query_url = api_base_url + lat + "," + lon
	## To get the hourly forecast with NWS you need to feed
	## it the following data in the url: (1) the relevant 
	## NWS field office code (str); and, (2) two grid values referring
	## to an unspecified proprietary or USG map grid system, (a)
	## gridx (int); and, (b) gridy(int).
	## Luckly, the query on the grids associated with lat, lon
	## provides this as a json object value already properly
	## formatted.


	response = requests.get(query_url)
	#points_res = json.loads(response.text)
	#print(points_res)
	city_or_place = str(response.json()['properties']['relativeLocation']['properties']['city'])
	state = str(response.json()['properties']['relativeLocation']['properties']['state'])
	final_url = str(response.json()['properties']['forecastHourly'])
	#print(f'{city_or_place}, {state}')
	#print(final_url)
	response_f = requests.get(final_url)
	hf = []
	polygon_bounding = []
	
	#num_coor = json.loads(response_f.json()['geometry']['coordinates'][0])
	#	print(type(num_coor))
	for hour in range(0,96):
		hf.append([hour, response_f.json()['properties']['periods'][hour]['shortForecast'], response_f.json()['properties']['periods'][hour]['temperature']])
		#starting_window
	for i in range(0, len(response_f.json()['geometry']['coordinates'][0])):
		polygon_bounding.append( [ [response_f.json()['geometry']['coordinates'][0][i][0] ], [ response_f.json()['geometry']['coordinates'][0][i][1] ] ] )
	
elif confirm == 'N':
	secs = 3
	print(f"""
Please rerun this program and input the correct geocordinates.
This program will quit in {secs} seconds.
	""")
	time.sleep(secs)	
	quit()
else:
	quit()


# Determine where the visualization will be rendered
output_file('filename.html')  # Render to static HTML

# Set up the figure(s)
fig = figure()  # Instantiate a figure() object

# Connect to and draw the data

# Organize the layout

# Preview and save 
show(fig)  # See what I made, and save if I like it