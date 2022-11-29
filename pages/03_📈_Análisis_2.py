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

#-------TEXTO---------------
st.text('')
st.markdown('En esta página se pueden analizar distintos gráficos de dispersión e histogramas acerca de los jugadores.')

#-------FORMA PÁGINA--------


opciones = st.selectbox('Qué gráfico desea ver', ('Gráfico de dispersión para Valor y Overall',
'Gráfico de dispersión para Edad y Overall','Valor Medio por Edad','Gráfico de dispersión para Edad y Potencial',
'Distribución de Overall','Distribución de Edad','Distribución de Valor(en Euros)'))

col1, col2 = st.columns((1.2,0.8))

with col1:
    if opciones == 'Gráfico de dispersión para Valor y Overall':
        fig = px.scatter(df, x='Overall', y='Value(in Euro)', hover_name='Name', height=600,width=800,title='Gráfico de dispersión para Valor y Overall')
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('10 Jugadores más caros')
            st.dataframe(df.sort_values('Value(in Euro)', ascending=False, ignore_index=True)[['Name', 'Age', 'Value(in Euro)', 'Overall','Club Name']].head(10))

    if opciones == 'Gráfico de dispersión para Edad y Overall':
        fig = px.scatter(df, x='Age', y='Overall', hover_name='Name', height=600,width=800,title='Gráfico de dispersión para Edad y Overall')
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('Descripción de la variable "Age"')
            st.table(df['Age'].describe().astype(int))

    if opciones == 'Valor Medio por Edad':
        edad = df.groupby('Age')['Value(in Euro)'].mean().reset_index()
        fig = px.bar(edad, x='Age', y='Value(in Euro)', orientation='v', title='Valor Medio por Edad')
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('Jugadores con 44 años')
            buffon = df[df['Age']== 44]
            st.table(buffon[['Name', 'Value(in Euro)', 'Overall', 'Potential']].reset_index())

    if opciones == 'Gráfico de dispersión para Edad y Potencial':
        fig = px.scatter(df, x='Age', y='Potential', height=600, width=800, hover_data=['Overall'], hover_name='Name', title='Gráfico de dispersión para Edad y Potencial')
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('10 Jugadores con mayor potencial')
            st.dataframe(df.sort_values('Potential', ascending=False, ignore_index=True)[['Name', 'Age', 'Value(in Euro)', 'Overall', 'Potential']].head(10))

    if opciones == 'Distribución de Overall':
        fig = px.histogram(df, x='Overall', title='Distribución de Overall',width=800,height=600)
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('Descripción de la variable "Overall"')
            st.table(df['Overall'].describe().astype(int))

    if opciones == 'Distribución de Edad':
        fig = px.histogram(df, x='Age', title='Distribución de Edad',width=800,height=600)
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('10 Jugadores con mayor Edad')
            st.dataframe(df.sort_values('Age', ascending=False)[['Name', 'Age', 'Value(in Euro)', 'Overall', 'Club Name']].head(10))

    if opciones == 'Distribución de Valor(en Euros)':
        fig = px.histogram(df, x = 'Value(in Euro)', nbins=100, title='Distribución de Valor(en Euros)',width=800,height=600)
        st.plotly_chart(fig)
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            st.write('Descripción de la variable "Value(in Euro)"')
            st.table(df['Value(in Euro)'].describe().round())