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
import folium
from folium.plugins import FastMarkerCluster
from PIL import Image
import streamlit.components.v1 as components
from unicodedata import name 

#-----configuracion de página--------------------------------------------------------------------------
st.set_page_config(page_title='Inside AirBnB: San Diego Exploratory Data Analysis', layout='centered', page_icon='🌇')

#-----Data Preprocessing-------------------------------------------------------
url = 'https://github.com/llorenc-fer/San-Diego-EDA/blob/main/listings.csv'
df = pd.read_csv(url, index_col='id')

calendar = pd.read_csv(r'C:\Users\lluri\Documents\samplerepo\Upgrade Hub\Modulo 2\20-Trabajo Módulo 2\San Diego Airbnb\calendar.csv.gz', 
                        compression='gzip', 
                        parse_dates=['date'],
                        index_col=['listing_id'],
                        low_memory=False)
url2 = https://github.com/llorenc-fer/San-Diego-EDA/blob/main/neighbourhoods%20(1).geojson
SDneighborhoods = json.load(open(url))                                                

#drop unusable columns
df = df.drop('neighbourhood_group', axis=1)
df = df.drop('license', axis=1)

#cleaning columns
calendar['price'] = calendar['price'].str.replace("$", "", regex=True)
calendar['price'] = calendar['price'].str.replace(",", "", regex=True)
calendar['date'] = calendar['date'].replace("-", "/", regex=True)
calendar.head()

#converting date to datetime and price to numeric
calendar['date'] = pd.to_datetime(calendar['date'])
calendar['month'] = calendar['date'].dt.month
calendar['price'] = pd.to_numeric(calendar['price'])

#repair outliers
def outliers_repair (df):
    """
    outliers_repair: se usa para identificar y reparar valores atípicos en un DataFrame dado.
    param df_listings: DataFrame para el cual se deben reparar los valores atípicos.
    returns: dataFrame sin valores atípicos.
    """
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    outliers = (df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))

    dataset_wo_outliers = df.copy()
    dataset_wo_outliers = pd.DataFrame(df)
    for col in df.columns:
        if df[col].dtype == 'object':
            moda = df[col].mode()[0]
            dataset_wo_outliers.loc[outliers[col], col] = moda
        else:
            media = df[col].mean()
            dataset_wo_outliers.loc[outliers[col], col] = media

    return dataset_wo_outliers

df = outliers_repair(df)

df_grouped = df.groupby('neighbourhood').size().nlargest(10)
df_top10 = df[df['neighbourhood'].isin(df_grouped.index)]
neighborhood_prices = df_top10.groupby(['neighbourhood'])['price'].mean().sort_values(ascending=False)


df_pivot = df.pivot_table(values='host_id', index=['neighbourhood'], aggfunc='count')# Create pivot table
df_pivot = df_pivot.reset_index()# Reset index
df_pivot.rename(columns={'id': 'Number of apartments'}, inplace=True)# Rename columns

sd_coordinates = (32.8242404,-117.3891768)


def drop_rows(df, column, value):
    """drop rows elimina el valor que queremos de una fila de una columna
    :param df: dataframe que vamos a usar
    :param column: columna que tendrá los valores de las filas que queremos borrar
    :param value: valor que queremos borrar
    """
    df = df[df[column] != value]
    return df
df = drop_rows(df, "latitude", 32.763520185713716)
df = drop_rows(df, 'longitude', -117.17384504564319)


#-----empieza la app-----------------------------------------------------------------------------------
st.image('https://i0.wp.com/christ-pres.church/wp-content/uploads/2018/07/sandiego-header.jpg?ssl=1')
st.text("San Diego skyline, image from Christ Church Presbyterian")
st.title("Exploring San Diego's AirBnB data")




#-----tablas que podemos usar--------------------------------------------------------------------------
#-----configuracion de tablas---------------------------------------------------------------------------
tabs = st.tabs(["Exploring San Diego's Neighborhoods", "Price Data Exploration"])
#-----tabla 1-----------
tab_plots = tabs[0]

with tab_plots:        
    st.image('https://secretsandiego.com/wp-content/uploads/2022/10/sd-header-wp-1024x478.jpg')
    st.text("Image from secretsandiego.com")
    st.title("Exploring San Diego's Neighbourhoods")

with tab_plots:
    
    index = df['room_type'].value_counts().head().index
    fig4 = px.bar(x=df['room_type'].value_counts().head().index, 
            y=df['room_type'].value_counts().head().values,
            color=index)
    fig4.update_layout(title="Room Type", 
                xaxis_title="Listings", 
                yaxis_title="Listings per Room Type",
                template = 'plotly_dark')
    st.plotly_chart(fig4)


with tab_plots:    
    values=df['neighbourhood'].value_counts().head(10).values
    fig = px.bar(x=df['neighbourhood'].value_counts().head(10).index, 
            y=df['neighbourhood'].value_counts().head(10).values,
            color=values)
    fig.update_layout(title="Top 10 Neighbourhoods: Where do people stay?", 
                xaxis_title="Neighbourhoods", 
                yaxis_title="Listings per neighbourhood", 
                template = 'plotly_dark')
    st.plotly_chart(fig)

with tab_plots: 
    html = open("map2.html", "r", encoding='utf-8').read()
    st.components.v1.html(html,height=600)



with tab_plots:
    especies1 = df['neighbourhood'].value_counts()
    fig3 = px.treemap(especies1, 
            path=[especies1.index], 
            values=especies1,height=500, 
            title='All neighbourhood listings by size', 
            color_discrete_sequence = px.colors.qualitative.Dark24,
            template = 'plotly_dark'
            ) 
    st.plotly_chart(fig3)

with tab_plots:
    st.write("Exploring the most popular neighbourhoods in San Diego")
    table = pd.pivot_table(df_top10, 
                        index =['neighbourhood'],
                        columns='room_type', 
                        values ='price', 
                        aggfunc ='mean')
    table = table.reset_index()
    table = table.melt(id_vars='neighbourhood', 
                    value_vars=['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'], 
                    var_name='room_type', 
                    value_name='price')
    fig1 = px.bar(table,
            x='price', 
            y='neighbourhood', 
            color='room_type', 
            orientation='h',
            barmode='stack',
            labels={'price':'Number of total rooms','neighbourhood':'Neighbourhood','room_type':'Bedrooms'},
            title='Bedroom Count per Neighborhood',
            )
    fig1.update_layout(xaxis=dict(categoryorder='total descending'),
                yaxis=dict(title='Neighbourhood'),
                legend=dict(title='Bedrooms', 
                                x=1, 
                                y=0, 
                                traceorder='normal',
                                font=dict(family='Arial, sans-serif', 
                                            size=12, 
                                            color='#FFF',
                                            )),
                showlegend = True,
                title_font_color='white',
                bargap=0.2,
                bargroupgap=0.1,
                template = 'plotly_dark'
                )
    st.plotly_chart(fig1)
    st.write("Most rentals come from entire home/apt")
    st.write("The median home value in Del Mar Heights is $1.1 million, 497% higher than the national average.")

#-----tabla 2-----------
tab_plots = tabs[1]

with tab_plots:        
    st.image('https://149361101.v2.pressablecdn.com/wp-content/uploads/2019/12/beach-resort-san-diego-bay-sun-set.jpg')
    st.text("Image from secretsandiegoexplorer.com")
    st.title("Exploring Prices")

with tab_plots:
        #finding the average price per month 
    monthly_prices = calendar.groupby(calendar['date'].dt.month)['price'].mean()

    #mapping number and their names
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    monthly_prices.index = monthly_prices.index.map(month_dict)
    #plotting the values
    trace = go.Scatter(x=monthly_prices.index, 
                    y=monthly_prices.values)
    data = [trace]
    layout = go.Layout(title='Temporal Patterns in Mean Airbnb Price', 
                    xaxis=dict(title='Month'), 
                    yaxis=dict(title='Average Price'), 
                    template = 'plotly_dark')
    fig5 = go.Figure(data=data, 
                layout=layout)
    st.plotly_chart(fig5)

with tab_plots:
    image = Image.open(r'C:\Users\lluri\Documents\samplerepo\Upgrade Hub\Modulo 2\20-Trabajo Módulo 2\San Diego Airbnb\newplot.png')
    st.image(image)

with tab_plots:
    fig2 = px.bar(neighborhood_prices, 
            x='price', 
            y=neighborhood_prices.index, 
            labels={'price':'Average Price','neighbourhood':'Neighbourhood'}, 
            title='Average Airbnb Price by Neighbourhood',
            color='price',
            template = 'plotly_dark')
    st.plotly_chart(fig2)

with tab_plots:
    fig6 = px.scatter(df_top10, 
                x="neighbourhood", 
                y="price", 
                color="room_type",
                title="Room Type per Neighbourhood by Price",
                size='price', 
                hover_data=['price'],
                template = 'plotly_dark'            
                )
    fig6.update_layout(xaxis=dict(title='Neighbourhood',
                            categoryorder='total descending'),
                yaxis=dict(title='Price'),
                legend=dict(title='Room Type', 
                                x=1, 
                                y=1, 
                                traceorder='normal',
                                font=dict(family='Arial, sans-serif', 
                                            size=12, 
                                            color='#FFF',
                                            )))
    st.plotly_chart(fig6)

with tab_plots:
    st.text("Number of listings by neighbourhood")
    fig8 = px.choropleth_mapbox(df_pivot, 
                            geojson=SDneighborhoods, 
                            locations='neighbourhood', 
                            color='host_id',
                            color_continuous_scale='PuRd',
                            title = 'Price by location',
                            featureidkey="properties.neighbourhood",
                            center={"lat": 32.7173603217, "lon": -117.162609086}, 
                            mapbox_style="carto-positron", 
                            zoom=8.5,
                            labels={'Number of apartments':'Number of Apartments'})
    fig8.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig8)  

with tab_plots:
    map = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                        opacity=1.0, 
                        color =  'price', 
                        title = ('Price by location'),
                        color_continuous_scale=px.colors.sequential.Jet, 
                        height = 600, zoom = 9.7,
                        text= 'room_type',
                        hover_name = 'name')
    map.update_layout(mapbox_style="open-street-map")
    map.update_layout(margin={"r":80,"t":80,"l":80,"b":80})
    st.plotly_chart(map)
    st.text("Map by Roberto Herguedas, all rights reserved.")
#-----tabla 3-----------
# tab_plots = tabs[2]
# with tab_plots:
#     st.write('esta es mi tercera tabla')
    



# #-----sidebar------------------------------------------------------------------------------------------
# st.set_option('deprecation.showPyplotGlobalUse', False) #para que no muestre warnings de versiones desfasadas
# st.sidebar.title('Menu')
# st.sidebar.image('https://media.gettyimages.com/id/1310911999/es/foto/smoking-pipe-isolated-on-white-background.jpg?s=612x612&w=gi&k=20&c=G-4B2VqPafwGGgCa5bEPFV9jf6aao2xxXFE1wSrSv0Y=', width=100)
# st.sidebar.write('un texto')
# st.sidebar.write('---')
# st.sidebar.write('ootro texto')
# st.sidebar.write('---')
# if st.sidebar.button('Ver Dataframe'):
#     st.dataframe(df)
# if st.sidebar.button('Segundo click'):
#     st.write('Whoops! Algo salío mal')
#     st.image('https://media.gettyimages.com/id/1310911999/es/foto/smoking-pipe-isolated-on-white-background.jpg?s=612x612&w=gi&k=20&c=G-4B2VqPafwGGgCa5bEPFV9jf6aao2xxXFE1wSrSv0Y=', width=100)

# st.sidebar.slider('Slider sample', min_value=0,max_value=100)
# st.sidebar.checkbox('check sample', help='select values')
# st.sidebar.text_input(label='insert text')
# if(st.sidebar.button('botón de prueba')):
#     sns.set_theme(style='white')
#     sns.relplot(data=df, kind='scatter')
#     st.pyplot()
