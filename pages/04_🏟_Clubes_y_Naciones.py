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

#--------CLUBES O NACIONES------
st.text('')
clubonacion = st.radio(
    "Seleccionar",
    ('Clubes', 'Naciones'))

#--------SELECTBOXCLUBES--------
if clubonacion == 'Clubes':
        st.write('Ha seleccionado clubes')

        opcionesclubes = st.selectbox('Seleccionar gráfico de Clubes', ('Top 20 Clubes con mayor media de Valor', 'Top 20 clubes con mayor Valor acumulado',
        'Top 20 clubes con mejor media de Overall', 'Top 20 clubes con mejor media de Ritmo'))
        if opcionesclubes == 'Top 20 Clubes con mayor media de Valor':

            club = df.groupby('Club Name')['Value(in Euro)'].mean().reset_index().sort_values('Value(in Euro)', ascending=True).tail(20)
            fig = px.bar(club, x='Value(in Euro)', y='Club Name', orientation='h', title='Top 20 Clubes con mayor media de Valor', width=800, height=500)
            st.plotly_chart(fig)

        if opcionesclubes == 'Top 20 clubes con mayor Valor acumulado':

            club = df.groupby('Club Name')['Value(in Euro)'].sum().reset_index().sort_values('Value(in Euro)', ascending=True).tail(20)
            fig = px.bar(club, x='Value(in Euro)', y='Club Name', orientation='h', title='Top 20 clubes con mayor Valor acumulado', width=800, height=500)
            st.plotly_chart(fig)

        if opcionesclubes == 'Top 20 clubes con mejor media de Overall':

            club = df.groupby('Club Name')['Overall'].mean().reset_index().sort_values('Overall', ascending=True).tail(20)
            fig = px.bar(club, x='Overall', y='Club Name', orientation='h',title='Top 20 clubes con mejor media de Overall ',width=800,height=500)
            st.plotly_chart(fig)

        if opcionesclubes == 'Top 20 clubes con mejor media de Ritmo':

            cambiar = 'Pace Total'
            club = df.groupby('Club Name')[cambiar].mean().reset_index().sort_values(cambiar, ascending=True).tail(20)
            fig = px.bar(club, x=cambiar, y='Club Name', orientation='h',title='Top 20 clubes con mejor media de Ritmo',width=800,height=500)
            st.plotly_chart(fig)

#-------SELECTBOXNACIONES-------
if clubonacion == 'Naciones':
        st.write('Ha seleccionado naciones')

        opcionesnaciones = st.selectbox('Seleccionar gráfico de Naciones', ('Top 20 Países mejor jugador por Overall',
        'Top 20 Países con mayor media de Overall','Top 20 Países con mayor media de valor por jugador'))

        if opcionesnaciones == 'Top 20 Países mejor jugador por Overall':
            club = df.groupby('Nationality')['Overall'].max().reset_index().sort_values('Overall', ascending=True).tail(20)
            fig = px.bar(club, x='Overall', y='Nationality', orientation='h', title='Top 20 Países mejor jugador por Overall', width=800,height=500)
            st.plotly_chart(fig)
        
        if opcionesnaciones == 'Top 20 Países con mayor media de Overall':
            club = df.groupby('Nationality')['Overall'].mean().reset_index().sort_values('Overall', ascending=True).tail(20)
            fig = px.bar(club, x='Overall', y='Nationality', orientation='h',title='Top 20 Países con mayor media de Overall', width=800,height=500)
            st.plotly_chart(fig)
        
        if opcionesnaciones == 'Top 20 Países con mayor media de valor por jugador':
            club = df.groupby('Nationality')['Value(in Euro)'].mean().reset_index().sort_values('Value(in Euro)', ascending=True).tail(20)
            fig = px.bar(club, x='Value(in Euro)', y='Nationality', orientation='h', title='Top 20 Países con mayor media de valor por jugador',width=800,height=500)
            st.plotly_chart(fig)
            st.write('Explicación Aquí!')
            if st.button('Spoiler'):
                col1, col2 = st.columns(2)
                with col1:
                    egiptoval = df[df['Nationality']=='Egypt']
                    figegipto = px.scatter(egiptoval, y = 'Value(in Euro)', hover_name = 'Name', title = 'Distribución Valor Egipto')
                    st.plotly_chart(figegipto)
                with col2:
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.markdown('''Por cuestiones del reducido número de jugadores en algunas naciones, algunas de las superestrellas tienen un
                    peso muy importante sobre la media de Overall. En el caso de Egipto, Mohamed Salah eleva tanto la
                    media de esta nación que se coloca en la de mayor media. Lo podríamos catalogar como outlier.<br>
                    
                    La media de Egipto es de 12.474.231 €
                    
    La media sin "Mo" es de 3.888.750 €''', unsafe_allow_html=True)