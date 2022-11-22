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
    st.image('ProyectoFinal\Fifa23Players\gen5-horizontal-black.png',  width=400)
with link1:
    st.subheader('Streamlit App por [José Luis PR](https://www.linkedin.com/in/joseluisperezruiz1/)')

#--------DATAFRAME-----------
df = pd.read_csv('ProyectoFinal\Fifa23Players\Fifa23PlayersData.csv')
df.drop(['Known As', 'On Loan'], axis=1, inplace = True)
df['Type'] = pd.cut(df['Overall'], bins=[0, 64, 74, float('Inf')], labels=['Bronze', 'Silver', 'Gold'])
df.drop('Positions Played', axis=1, inplace= True)
df.rename(columns={'Best Position':'Position'}, inplace= True)
df.rename(columns={'Full Name':'Name'}, inplace= True)
df = df.drop_duplicates()

#-------TEXTO-------

st.markdown('En las siguientes páginas se hará un análisis de multitud de variables referentes a los jugadores implementados en FIFA 23')
st.write('El dataset a partir del que se ha analizado toda la información es de Kaggle [FIFA 23 DATASET](https://www.kaggle.com/datasets/sanjeetsinghnaik/fifa-23-players-dataset)')
st.markdown('Esta base de datos, a su vez, se ha obtenido a partir de webscrapping del sitio web [sofifa](https://sofifa.com/)')

#--------EXPANDER DATAFRAME------

with st.expander('Visualizar DataFrame', expanded=False):
    st.dataframe(df, width=2000)

#-------TEXTO---------

st.markdown('Las variables son las siguientes:')

with st.expander('Ver variables del DataFrame', expanded=False):
    st.table(df.columns)

st.markdown('A continuación se puede ver también el primer preprocesado de información que se ha hecho')
with st.expander('Ver Código', expanded=False):
    with st.echo():
        df = pd.read_csv('ProyectoFinal\Fifa23Players\Fifa23PlayersData.csv')
        df.drop(['Known As', 'On Loan'], axis=1, inplace = True)
        df['Type'] = pd.cut(df['Overall'], bins=[0, 64, 74, float('Inf')], labels=['Bronze', 'Silver', 'Gold'])
        df.drop('Positions Played', axis=1, inplace= True)
        df.rename(columns={'Best Position':'Position'}, inplace= True)
        df.rename(columns={'Full Name':'Name'}, inplace= True)
        df = df.drop_duplicates()


st.markdown('''<div class="waveWrapper waveAnimation"><div class="waveWrapperInner bgTop"><div class="wave waveTop" 
style="background-image: url('http://front-end-noobs.com/jecko/img/wave-top.png')"></div></div>
  <div class="waveWrapperInner bgMiddle">
    <div class="wave waveMiddle" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-mid.png')"></div>
  </div>
  <div class="waveWrapperInner bgBottom">
    <div class="wave waveBottom" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-bot.png')"></div>
  </div>
    </div>''', unsafe_allow_html=True)