#--------LIBRERÍAS---------
import streamlit as st

from iso3166 import countries
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px

#--CONFIGURACIÓN DE LA PÁGINA Y ENCABEZADO--

st.set_page_config(layout="wide")

imagencol1, espacio1, link1, espacio2 = st.columns((2.3, .1, 1.3, .1))
with imagencol1:
    st.image('gen5-horizontal-black.png',  width=400)
with link1:
    st.subheader('Streamlit App por [José Luis PR](https://www.linkedin.com/in/joseluisperezruiz1/)')

#--------DATAFRAME-----------
df = pd.read_csv('Fifa23PlayersData.csv')
df.drop(['Known As', 'On Loan'], axis=1, inplace = True)
df['Type'] = pd.cut(df['Overall'], bins=[0, 64, 74, float('Inf')], labels=['Bronze', 'Silver', 'Gold'])
df.drop('Positions Played', axis=1, inplace= True)
df.rename(columns={'Best Position':'Position'}, inplace= True)
df.rename(columns={'Full Name':'Name'}, inplace= True)
df = df.drop_duplicates()

#-----DICCIONARIO ALPHA3-------

diccionariopaises = {}
for c in countries:
    diccionariopaises[c.name] = c.alpha3
    
df['alpha3'] = df['Nationality']
df = df.replace({'alpha3': diccionariopaises})

gbr = ['England', 'Wales', 'Scotland', 'Northern Ireland']

df.loc[df['Nationality'].isin(gbr), 'alpha3'] = 'GBR'
df.loc[df['Nationality'] == 'Bosnia Herzegovina', 'alpha3'] = 'BIH'
df.loc[df['Nationality'] == 'Korea Republic', 'alpha3'] = 'KOR'
df.loc[df['Nationality'] == 'Czech Republic', 'alpha3'] = 'CZE'
df.loc[df['Nationality'] == 'St Lucia', 'alpha3'] = 'LCA'
df.loc[df['Nationality'] == 'Palestine', 'alpha3'] = 'PSE'
df.loc[df['Nationality'] == 'Antigua & Barbuda', 'alpha3'] = 'ATG'
df.loc[df['Nationality'] == 'St Kitts Nevis', 'alpha3'] = 'KNA'
df.loc[df['Nationality'] == 'Korea DPR', 'alpha3'] = 'PRK'
df.loc[df['Nationality'] == 'São Tomé & Príncipe', 'alpha3'] = 'STP'
df.loc[df['Nationality'] == 'Trinidad & Tobago', 'alpha3'] = 'TTO'
df.loc[df['Nationality'] == 'Bolivia', 'alpha3'] = 'BOL'
df.loc[df['Nationality'] == 'Moldova', 'alpha3'] = 'MDA'
df.loc[df['Nationality'] == 'Curacao', 'alpha3'] = 'CUW'
df.loc[df['Nationality'] == 'Tanzania', 'alpha3'] = 'TZA'
df.loc[df['Nationality'] == 'Guinea Bissau', 'alpha3'] = 'GNB'
df.loc[df['Nationality'] == 'China PR', 'alpha3'] = 'CHN'
df.loc[df['Nationality'] == 'FYR Macedonia', 'alpha3'] = 'MKD'
df.loc[df['Nationality'] == 'Iran', 'alpha3'] = 'IRN'
df.loc[df['Nationality'] == 'Syria', 'alpha3'] = 'SYR'
df.loc[df['Nationality'] == 'Cape Verde', 'alpha3'] = 'CPV'
df.loc[df['Nationality'] == 'United States', 'alpha3'] = 'USA'
df.loc[df['Nationality'] == 'Republic of Ireland', 'alpha3'] = 'IRL'
df.loc[df['Nationality'] == 'Venezuela', 'alpha3'] = 'VEN'
df.loc[df['Nationality'] == 'Russia', 'alpha3'] = 'RUS'
df.loc[df['Nationality'] == 'Ivory Coast', 'alpha3'] = 'CIV'
df.loc[df['Nationality'] == 'DR Congo', 'alpha3'] = 'COD'
df.loc[df['Nationality'] == 'Central African Rep.', 'alpha3'] = 'CAF'
df.loc[df['Nationality'] == 'Turkey', 'alpha3'] = 'TUR'
df.loc[df['Nationality'] == 'Congo DR', 'alpha3'] = 'COD'
df.loc[df['Nationality'] == 'Cape Verde Islands', 'alpha3'] = 'CPV'
df.loc[df['Nationality'] == 'Chinese Taipei', 'alpha3'] = 'TWN'
df.loc[df['Nationality'] == 'São Tomé e Príncipe', 'alpha3'] = 'STP'
df.loc[df['Nationality'] == 'Vietnam', 'alpha3'] = 'VNM'

#-------TEXTO---------------
st.text('')
st.text('')
st.markdown('Para hacer un poco más amena la información, se pueden visualizar en esta página distinta información en todo el globo.')
st.markdown('Nos vamos a basar en los códigos [ISO 3166-1 alfa-3](https://es.wikipedia.org/wiki/ISO_3166-1_alfa-3) gracias a la librería iso3166')

opcionesmapa = st.selectbox('Seleccionar mapa a mostrar', ('Número de Jugadores por País', 'Media de Edad por País',
'Valor Máximo de futbolista por País', 'Media de Potencial de futbolista por País'))

if opcionesmapa == 'Número de Jugadores por País':
    data = df.groupby(['alpha3', 'Nationality'])['Name'].count().reset_index()
    data.columns = ['alpha3', 'nationality', 'count']
    fig = px.choropleth(data, locations='alpha3', hover_name='nationality', color='count', projection='equirectangular', 
                    color_continuous_scale='burgyl', title='Número de Jugadores por País', width=1200,  height=700)
    fig.update_layout(
        coloraxis = dict(
            colorbar = dict(
                len = 0.9,
                orientation = 'h',
                y = -0.16,
                x = 0.925,
                xanchor = 'right',
                title ='Cantidad'
            )
        )
    )
    st.plotly_chart(fig)

if opcionesmapa == 'Media de Edad por País':
    data = df.groupby(['alpha3', 'Nationality'])['Age'].mean().reset_index()
    data.columns = ['alpha3', 'nationality', 'media_edad']
    fig = px.choropleth(data, locations='alpha3', hover_name='nationality', color='media_edad', projection='equirectangular',
                    color_continuous_scale='burgyl', title='Media de Edad por País', width=1200, height=700)
    fig.update_layout(
            coloraxis = dict(
                colorbar = dict(
                    len = 0.9,
                    orientation = 'h',
                    y = -0.16,
                    x = 0.925,
                    xanchor = 'right',
                    title = 'AÑOS'
                )
            )
    )
    st.plotly_chart(fig)
    edadmedia1, edadmedia2 = st.columns((0.6,0.6))
    with edadmedia1:
        st.markdown('Los países con jugadores de mayor edad son:')
        st.dataframe(df.groupby(['Nationality'])['Age'].mean().sort_values(ascending=False).head(10))
    with edadmedia2:
        st.markdown('\nLos países con jugadores de menor edad son:')
        st.dataframe(df.groupby(['Nationality'])['Age'].mean().sort_values(ascending=False).tail(10))

if opcionesmapa == 'Valor Máximo de futbolista por País':
    data = df.groupby(['alpha3', 'Nationality'])['Value(in Euro)'].max().reset_index()
    data.columns = ['alpha3', 'nationality','max_value']
    fig = px.choropleth(data, locations='alpha3',hover_name='nationality',color='max_value',projection='equirectangular',
                    color_continuous_scale= 'burgyl',title='Valor Máximo de futbolista por País',width=1200, height=700)
    fig.update_layout(
        coloraxis = dict(
            colorbar = dict(
                len = 0.9,
                orientation = 'h',
                y = -0.16,
                x = 0.925,
                xanchor = 'right',
                title = 'Valor Máximo'
            )
        )
    )
    st.plotly_chart(fig)

if opcionesmapa == 'Media de Potencial de futbolista por País':
    data = df.groupby(['alpha3', 'Nationality'])['Potential'].mean().reset_index()
    data.columns = ['alpha3', 'nationality','media_potential']
    fig = px.choropleth(data, locations='alpha3',hover_name='nationality',color='media_potential',projection='equirectangular',
                    color_continuous_scale= 'burgyl',title='Media de Potencial de futbolista por País',width=1200, height=700)
    fig.update_layout(
        coloraxis = dict(
            colorbar = dict(
                len = 0.9,
                orientation = 'h',
                y = -0.16,
                x = 0.925,
                xanchor = 'right',
                title = 'Potencial'
            )
        )
    )
    st.plotly_chart(fig)




