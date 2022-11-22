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

#--------FUNCIONES----------- 

#Función adaptada del usuario KOSTIANTYN ISAIENKOV de kaggle link https://www.kaggle.com/code/isaienkov/fifa2019-eda-modeling-field-visualization
def plot_pie_count(data, field='', percent_limit=0.5, title=''):
    
    data = data[field].value_counts().to_frame()

    total = data[field].sum()
    data['porcentaje'] = 100 * data[field]/total    

    percent_limit = percent_limit
    otherdata = data[data['porcentaje'] < percent_limit] 
    others = otherdata['porcentaje'].sum()  
    maindata = data[data['porcentaje'] >= percent_limit]

    data = maindata
    other_label = 'Otros(<' + str(percent_limit) + '% por valor)'
    data.loc[other_label] = pd.Series({field:otherdata[field].sum()}) 
    
    labels = data.index.tolist()   
    datavals = data[field].tolist()
    
    trace=go.Pie(
        labels=labels,
        values=datavals
    )

    layout = go.Layout(
        title = title,
        height=600,
        width=800
        )
    
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig)

#--------TEXTO---------
st.text('')
st.write('''En esta página podrá visualizar un gráfico circular con los porcentajes sobre el tipo de información que desee. En la barra desplegable, seleccione
la opción que quiera visualizar. Y en el slide podrá ajustar el porcentaje bajo el que quiera agrupar información.''')

#---------FORMA PÁGINA--------

# A PARTIR DEL TEXTO

colselectbox1, slidercol1, espaciadocol1 = st.columns((0.6,0.4,1))

with slidercol1:
    percent_slider = st.slider('Porcentaje para agrupar', 0.0, 10.0, 1.0, step=0.1)

with colselectbox1:
    opciones = st.selectbox(
    'Campo que desea visualizar',
    ('Nacionalidades', 'Posiciones', 'Pierna Preferida', 'Equipo internacional en el juego (poner slide alto)', 
    'Estrellas de Regates', 'Estrellas Pierna Mala'))

col1, col2 = st.columns((1.2,0.8))
with col1:

    if 'Nacionalidades' in opciones:
        plot_pie_count(df, 'Nationality',percent_limit=percent_slider, title = 'Número de jugadores por Nacionalidad')
        with col2:
            st.table(df['Nationality'].value_counts().head(5))
            st.table(df['Nationality'].value_counts().tail(5))
    
    if 'Posiciones' in opciones:
        plot_pie_count(df, 'Position', percent_limit=percent_slider, title = 'Número de jugadores por Posición')
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.write('Pequeño diccionario de las posiciones')
            st.markdown(
'''ST = Delantero Centro(DC)<br>  CF = Falso 9(SD) <br>   CB = Defensa Central(DFC)<br>    CAM = Mediapunta(MCO)<br>
RB = Lateral Derecho(LD)<br>    LB = Lateral Izquierdo(LI)<br> RWB = Carrilero Derecho(CAD)<br>    LWB = Carrilero Izquierdo(CAI)<br>
LM = Mediocentro Izquierdo(MI)<br>  RM = Mediocentro Derecho(MD)<br>    LW = Extremo Izquierdo(EI)<br>  RW = Extremo Derecho(ED)<br>
CM = Mediocentro(MC)<br>  CDM = Mediocentro Defensivo(MCD)<br>    GK = Portero(POR)''',
    unsafe_allow_html=True)


    if 'Pierna Preferida' in opciones:
        plot_pie_count(df, 'Preferred Foot', percent_limit=percent_slider, title = 'Número de jugadores por pierna buena')
        st.write('''Tan solo una cuarta parte de los futbolistas juega con pierna izquierda.''')
        with col2:
            with st.expander('Ver mejores jugadores Diestros', expanded=False):
                st.dataframe(df[df['Preferred Foot'] == 'Right'][['Name','Overall']].sort_values('Overall', ascending=False).head(10))
        with col2:    
            with st.expander('Ver mejores jugadores Zurdos', expanded=False):
                st.dataframe(df[df['Preferred Foot'] == 'Left'][['Name','Overall']].sort_values('Overall', ascending=False).head(10))

    if 'Equipo internacional en el juego (poner slide alto)' in opciones:
        plot_pie_count(df, 'National Team Name', percent_limit=percent_slider, title = 'Jugadores con Selección Nacional')
        st.write('''Tener en cuenta que los que aparezcan agrupados por el filtro, serán los jugadores con los que se puede jugar con su selección nacional.
    Si ajustamos el slider a 0 veremos que aparecen multitud de grupos de 0.125%, estas serán las selecciones nacionales implementadas.''')

    if 'Estrellas de Regates' in opciones:
        plot_pie_count(df, 'Skill Moves',percent_limit = 0, title = 'Estrellas de Regate')
        st.markdown('''Esta variable puede tener un valor entre 1 y 5. La mayoría de los jugadores poseen 2 y 3 estrellas. <br>
    A continuación puede visualizar aquellos que tienen 5 estrellas de regate:''')
        with col2:
            with st.expander('Lista de Jugadores con 5 Estrellas de Regate', expanded=False):
                st.dataframe(df[df['Skill Moves']==5].sort_values('Overall', ascending = False, ignore_index=True))

    if 'Estrellas Pierna Mala' in opciones:
        plot_pie_count(df, 'Weak Foot Rating',percent_limit = 0, title = 'Estrellas de Pierna Mala')
        st.markdown('''Esta variable puede tener un valor entre 1 y 5. Casi dos tercios de los jugadores poseen 3 estrellas. <br>
    Por la naturaleza de esta variable, podemos considerar ambidiestros los que tengan 5 estrellas de esta característica.''')
        with col2:
            with st.expander('Lista de Jugadores con 5 Estrellas de Pierna Mala', expanded=False):
                st.dataframe(df[df['Weak Foot Rating']==5].sort_values('Overall', ascending = False, ignore_index=True))