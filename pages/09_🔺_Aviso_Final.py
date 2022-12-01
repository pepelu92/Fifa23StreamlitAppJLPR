#--------LIBRERÍAS---------
import streamlit as st

import pandas as pd
import numpy as np

#--CONFIGURACIÓN DE LA PÁGINA Y ENCABEZADO--

st.set_page_config(layout="wide")

imagencol1, espacio1, link1, espacio2 = st.columns((2.3, .1, 1.3, .1))
with imagencol1:
    st.image('gen5-horizontal-black.png',  width=400)
with link1:
    st.subheader('Streamlit App por [José Luis PR](https://www.linkedin.com/in/joseluisperezruiz1/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))

st.markdown('\n')
st.markdown('\n')
st.markdown('\n')
st.markdown('\n')
st.markdown('Soy José Luis, he creado de esta App como proyecto final del bootcamp Data Analytics en UpgradeHub.')
st.markdown('''Aclarar que FIFA es propiedad de Electronic Arts y se reserva todos sus derechos. Esta aplicación se ha realizado con 
                fines educativos por y para fans del viodeojuego FIFA.''')
st.markdown('Si estás interesad@ en el código o en aportar mejoras para este, no dudes en hacerlo y contactar! [GITHUB](https://github.com/pepelu92/Fifa23StreamlitAppJLPR)') #INTRODUCIR ENLACE GITHUB
st.markdown('')
st.markdown('Tributes to:')

tribute1, tribute2, tribute3 = st.columns(3) 
with tribute1:
    st.markdown('[SANJEET SINGH NAIK](https://www.kaggle.com/datasets/sanjeetsinghnaik/fifa-23-players-dataset)')
with tribute2:
    st.markdown('[KOSTIANTYN ISAIENKOV](https://www.kaggle.com/code/isaienkov/fifa2019-eda-modeling-field-visualization)')
with tribute3:
    st.markdown('[MOHAMED ELSAYED](https://www.kaggle.com/code/mhmdsyed/fifa-19-dream-team#Dream-Team)')

st.markdown('En especial a mis profesores y compañeros de bootcamp. Muchas Gracias!')
