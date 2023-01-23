#-----librerías----------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import plotly.express as px
import plotly.graph_objs as go
import plotly.graph_objects as go
from matplotlib import ticker
from ipywidgets.embed import embed_minimal_html
import json
import matplotlib.dates as mdates
import gmaps
import gmaps.datasets
gmaps.configure(api_key='AIzaSyA3zU5c-hozhhYLUZeioS0F45g498s8Lco')
import streamlit as st
import streamlit.components.v1 as components
import geopandas as gpd
import folium
from folium.plugins import FastMarkerCluster
from PIL import Image
import streamlit.components.v1 as components
from unicodedata import name 

#-----configuracion de página--------------------------------------------------------------------------

st.set_page_config(page_title='Inside AirBnB: San Diego Exploratory Data Analysis', layout='centered', page_icon='🌇')

#-----empieza la app-----------------------------------------------------------------------------------
st.image('https://i0.wp.com/christ-pres.church/wp-content/uploads/2018/07/sandiego-header.jpg?ssl=1')
st.text("San Diego skyline, image from Christ Church Presbyterian")
st.title("Exploring San Diego's AirBnB data")
st.image('https://m.media-amazon.com/images/I/71yuxW9lM9L._AC_SL1050_.jpg')

#-----columnas-----------------------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("Welcome to San Diego:")
    st.markdown("A vibrant and welcoming city in Southern California with a gorgeous coastline, warm climate and a rich hispanic heritage.")
    st.text('Postcard by Amazon')
    st.text('Map by Depositphotos')
with col2:

    st.image('https://st2.depositphotos.com/2670707/10754/i/950/depositphotos_107544286-stock-photo-san-diego-in-california-usa.jpg')

#-----configuracion de tablas---------------------------------------------------------------------------
tabs = st.tabs(["Exploring San Diego's Neighborhoods", "Price Data Exploration", "Crime Rate in San Diego"])

#-----tabla 1-----------
tab_plots = tabs[0]
with tab_plots:        
    st.image('https://secretsandiego.com/wp-content/uploads/2022/10/sd-header-wp-1024x478.jpg')
    st.text("")
    st.text("Image from secretsandiego.com")
    st.title("Exploring San Diego's Neighbourhoods")
with tab_plots: 
    st.markdown("A large portion of the listings are entire homes or apartments.")
    st.markdown("6x more entire apartments than private rooms.")
    html = open("roomtype.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    st.markdown("Unsurprisingly, listings are concentrated in the coastal neighbourhoods")
    html = open("top10neighbourhoods.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    st.markdown("Distribution of Airbnb Apartments in the City")
    html = open("map2.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    st.markdown("Visual representation of listings per neighbourhood")
    html = open("treemap.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    st.write("Exploring the most popular neighbourhoods in San Diego:")
    st.write("The median home value in Del Mar Heights is $1.1 million, 497% higher than the national average.")
    html = open("bedroomcountperneighbourhood.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)

with tab_plots: 
    st.markdown("The top 10 hosts hoard more than 1300 apartments (more than 10% of total listings)")
    html = open("top10hosts.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
    

#-----tabla 2-----------
tab_plots = tabs[1]

with tab_plots:        
    st.image('https://149361101.v2.pressablecdn.com/wp-content/uploads/2019/12/beach-resort-san-diego-bay-sun-set.jpg')
    st.text("Image from secretsandiegoexplorer.com")
    st.title("Exploring Prices")
with tab_plots: 
    st.markdown("As expected, average price increases in the warmer months")
    html = open("temporalpatternsinairbnbprices.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots:
    st.markdown("Specific mean by neighbourhood: a trend confirmed")
    image = Image.open('newplot.png')
    st.image(image)
with tab_plots: 
    st.markdown("Most expensive top 10 neighbours are coastal and centric")
    html = open("averaigeairbnbpricebyneighbourhood.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    html = open("roomtypeperneighbourhoodbyprice.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots: 
    html = open("choropleth.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
with tab_plots:
    html = open("robertomap.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)
    st.text("Map by Roberto Herguedas, all rights reserved.")


#-----tabla 3-----------
tab_plots = tabs[2]
with tab_plots:
    st.image('https://cdn-cplbh.nitrocdn.com/jroJNRxstilajZJELUsnaEigEZqpBufL/assets/images/optimized/rev-af72e93/wp-content/uploads/2018/03/police-equipment-inventory-header.jpg')
    st.text("Image by Asset Panda")
    st.header('Crime by neighbourhood in San Diego')
    image = Image.open('SDCrimerate.jpg')
    st.image(image)
    st.markdown("San Diego has a relatively low overall crime rate compared to other major US cities.")
    st.markdown("Property crimes such as burglary and theft tend to be the most common types of crime.")
    st.markdown("Higher Crime Rates in Downtown Area.")


