## import required modules and methods
from flask import Flask, render_template, request
import seaborn as sns
import json
import requests
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

# Bokeh libraries
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure,output_file, show
from bokeh.embed import file_html, components
from bokeh.resources import CDN

app = Flask(__name__)
global hf

@app.route('/')
def index():
## NWS report weather conditions in 2.5km^2 grids. 
## As grid numbers are obscure, we will collect
## geocordinates as input from the user and the API
## will kindly map to the relevant grid reference.
    return render_template('index.html')

@app.route('/forecast')
def forecast():
    ## assign National Weather Service API URL to string variable
    api_base_url = 'https://api.weather.gov/points/'

    ## create reference variables for later use
    city_or_place = ''
    state = ''
    
    ## retrieve user input
    lat = str(request.args.get('lat'))
    lon = str(request.args.get('lon'))
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
    #print(response)
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
    #   print(type(num_coor))
    for hour in range(0,96):
        hf.append([hour, response_f.json()['properties']['periods'][hour]['shortForecast'], response_f.json()['properties']['periods'][hour]['temperature']])
        #starting_window
    for i in range(0, len(response_f.json()['geometry']['coordinates'][0])):
        polygon_bounding.append( [ [response_f.json()['geometry']['coordinates'][0][i][0] ], [ response_f.json()['geometry']['coordinates'][0][i][1] ] ] )
    x_sc = list(range(0,96))
    y_sc = list(range(10,120))
    y_lab = 'Temperature [degrees F]'
    x_lab = 'Houly Increments of Time'
    y_vals = []
    for i in range(0,96):
        y_vals.append(hf[i][2])
    x_vals = np.array(range(0,96))
    source = ColumnDataSource()
    source.data = dict(x = x_vals, y = y_vals)
    fig = figure(plot_height=600, plot_width=720)
    fig.circle(x_vals, y_vals, size=8)
    fig.xaxis.axis_label = 'Houly Increments of Time'
    fig.yaxis.axis_label = 'Temperature [degrees F]'
    g = show(fig)
    return render_template('forecast.html', script0=polygon_bounding, script1=[city_or_place, state], script2=hf, graphic=g)
    
#@app.route('/vis')
#def visual_forecast():
#    affirm = str(request.args.get('vis_want'))
#    print(affirm)
#    if affirm == "V":
#        x_sc = list(range(0,96))
#        y_sc = list(range(10,120))
#        y_lab = 'Temperature [degrees F]'
#        x_lab = 'Houly Increments of Time'
#        y_vals = []
#        for i in range(0,96):
            #y_vals[i] = hf[i][2]
#            print(hf)
#        x_vals = np.array(range(0,96))
        #source = ColumnDataSource()
        #source.data = dict(x = x_vals, y = y_vals)
        #print(source)
        #fig = figure(plot_height=600, plot_width=720)
        #fig.circle(x_vals, y_vals, size=8)
        #fig.xaxis.axis_label = 'Houly Increments of Time'
        #fig.yaxis.axis_label = 'Temperature [degrees F]'
#    return render_template('vis.html')#, v=fig)

if __name__ == '__main__':
    app.run(port=8000, debug=True)