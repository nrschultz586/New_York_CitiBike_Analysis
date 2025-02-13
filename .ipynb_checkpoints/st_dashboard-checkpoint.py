################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

top20 = pd.read_csv('C:/Users/nrsmi/Documents/CareerFoundry/New_York_CitiBike_Analysis/Data/Prepared_Data/top_20.csv', index_col = 0)
df = pd.read_csv('C:/Users/nrsmi/Documents/CareerFoundry/New_York_CitiBike_Analysis/Data/Prepared_Data/avgTemp_BikeRidesDaily.csv', index_col = 0)

########################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in Chicago',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title='Daily Bike Trips and Temperatures in 2022',
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    yaxis2_title='Average Daily Temperature (°C)'
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = 'C:/Users/nrsmi/Documents/CareerFoundry/New_York_CitiBike_Analysis/Bike Trips Aggregated.html' 

# Read file and keep in variable

with open('C:/Users/nrsmi/Documents/CareerFoundry/New_York_CitiBike_Analysis/Bike Trips Aggregated.html','r', encoding='utf-8') as f:
    html_data = f.read()
    
## Show in webpage
st.header("Aggregated Bike Trips in Chicago")
st.components.v1.html(html_data,height=1000)
