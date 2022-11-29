import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

import seaborn as sns
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
import plotly.express as px

from plotly.subplots import make_subplots
from PIL import Image
from IPython.core.display import HTML
from ortools.linear_solver import pywraplp

from iso3166 import countries

#--CONFIGURACIÓN DE LA PÁGINA--

st.set_page_config(layout='wide',
page_title='FIFA23 APP',
page_icon='⚽')

#--------IMAGEN ENCABEZADO--------
st.image('gen5-horizontal-black.png')
#-------TEXTO ENCABEZADO---------
espacio1, link1, espacio2 = st.columns((2.5, 1.3, .1))
with link1:
    st.subheader('Streamlit App por [José Luis PR](https://www.linkedin.com/in/joseluisperezruiz1/)')

#---------TEXTO----------

st.write('''Esta es una multi-App que se ha creado usando Streamlit.''')
st.write('''Es una app con fines educativos, por lo que te invito a comentar, proponer mejoras y correcciones para optimizarla.''')
st.write('''Enlace al código [GITHUB](enlace)''')
st.text('')
st.write('Para navegar por las distintas apps solo debe hacer click en el índice de la izquierda')
