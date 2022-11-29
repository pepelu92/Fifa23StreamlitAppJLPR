#--------LIBRERÍAS---------
import streamlit as st

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

#----------Funciones---------
st.text('')
st.text('')
st.markdown('En esta página podrá buscar cualquier jugador por su índice y visualizar sus atributos principales o estadísticas detalladas')
st.markdown('En la siguiente casilla puede buscar por nombre para ver el índice')


#-------BUSCADOR NOMBRE---------

colbusqueda1, colbusqueda2 = st.columns((0.5,1.5))
with colbusqueda1:
    busqueda = st.text_input('Búsqueda 🔍', value='', placeholder='Introduzca nombre')

# Buscador de jugador
col1, col2 = st.columns(2)
with col1:
    dfbuscador=df[['Name','Age','Position','Overall', 'Potential', 'Nationality', 'Value(in Euro)','Club Jersey Number','Type']]
    st.dataframe(dfbuscador[dfbuscador['Name'].str.contains(busqueda, case=False)], height=200)

with col2:
    options = st.multiselect(
    'Qué estadísticas quiere visualizar',
    ['Pace Total', 'Shooting Total', 'Passing Total',
       'Dribbling Total', 'Defending Total', 'Physicality Total', 'Crossing',
       'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys',
       'Dribbling', 'Curve', 'Freekick Accuracy', 'LongPassing', 'BallControl',
       'Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance',
       'Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots',
       'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
       'Composure', 'Marking', 'Standing Tackle', 'Sliding Tackle'],

    ['Pace Total', 'Shooting Total', 'Passing Total',
       'Dribbling Total', 'Defending Total', 'Physicality Total'])

#----------PLAYERINDEX--------
colbusqueda3, colbusqueda4 = st.columns((0.5,1.5))
with colbusqueda3:
    busqueda2 = st.text_input('Introducir Índice 🔢', placeholder='Sólo Números', value='')

#Introducimos todas las variables dentro del botón para que no se inicialicen en 0 o valores nulos y aparezcan errores indeseados
if st.button('MOSTRAR'):

    player_index = int(busqueda2)
    col = options
    nombretes = df.iloc[player_index]['Name'] 
    mediajugador = df.iloc[player_index]['Overall']


    espacio1,foto1,foto2,texto1,espacio3 = st.columns((0.2,0.1,0.1,0.2,1))
    
    with foto1:
        imagen = df['Image Link'].to_list()
        st.image(imagen[player_index])

    with texto1:
        st.markdown(f'{nombretes} - {mediajugador}')

    with foto2:
        nacionalimagen = df['National Team Image Link'].to_list()
        st.image(nacionalimagen[player_index])

    campo = df.loc[player_index,col].astype('int64')

    player_index = int(busqueda2)

    categories = []
    for i in col:
        categories.append(i + ': ' + str(int(campo[i]))+'%')

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(r=campo, theta=categories,fill='toself',
                              name=df.iloc[player_index]['Name'],line_color='red'))

    fig.update_layout(polar=dict(radialaxis=dict(visible=False,range=[0, 100])),showlegend=False)


    st.plotly_chart(fig)
