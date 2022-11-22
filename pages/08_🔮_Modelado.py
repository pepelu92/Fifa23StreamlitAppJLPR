#--------LIBRERÍAS---------
import streamlit as st

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio


from sklearn.metrics import mean_squared_error

#--CONFIGURACIÓN DE LA PÁGINA Y ENCABEZADO--

st.set_page_config(layout="wide")

imagencol1, espacio1, link1, espacio2 = st.columns((2.3, .1, 1.3, .1))
with imagencol1:
    st.image('ProyectoFinal\Fifa23Players\gen5-horizontal-black.png',  width=400)
with link1:
    st.subheader('Streamlit App por [José Luis PR](https://www.linkedin.com/in/joseluisperezruiz1/)')

#--------DATAFRAME Y VARIABLES-----------
df = pd.read_csv('ProyectoFinal\Fifa23Players\Fifa23PlayersData.csv')
df.drop(['Known As', 'On Loan'], axis=1, inplace = True)
df['Type'] = pd.cut(df['Overall'], bins=[0, 64, 74, float('Inf')], labels=['Bronze', 'Silver', 'Gold'])
df.drop('Positions Played', axis=1, inplace= True)
df.rename(columns={'Best Position':'Position'}, inplace= True)
df.rename(columns={'Full Name':'Name'}, inplace= True)
df = df.drop_duplicates()


#--------texto---------

st.text('')
st.subheader('Modelo Regresivo')
st.text('')
st.markdown('''En este apartado vamos a tratar de realizar de predecir la variable "Potential". Para ello recurriremos a distintos 
algoritmos de regresión de la librería [Sklearn](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning)''')
st.text('')

st.markdown('En primer lugar, elegimos aquellas variables que queremos introducir en el modelo.')
with st.echo():
    columnasmodel = ['Overall', 'Potential', 'Value(in Euro)','Age', 'Height(in cm)', 'Weight(in kg)','TotalStats', 'BaseStats','Wage(in Euro)','Weak Foot Rating',
    'Skill Moves','Attacking Work Rate','Defensive Work Rate', 'Crossing','Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys', 'Dribbling', 'Curve', 
    'Freekick Accuracy', 'LongPassing', 'BallControl','Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance','Shot Power', 'Jumping', 'Stamina', 
    'Strength', 'Long Shots','Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties','Composure', 'Marking', 'Standing Tackle', 
    'Sliding Tackle']
    dfmodel = df[columnasmodel]
st.markdown('')
st.markdown('Ahora veremos las correlaciones')

# Calculamos correlaciones
corr = dfmodel.corr()

trace = go.Heatmap(z=corr.values,
                  x=corr.index.values,
                  y=corr.columns.values,
                  colorscale='BrBG'
                  )
fig = go.Figure()
fig.update_layout(
    autosize=False,
    width=1000,
    height=700)
fig.add_trace(trace)
st.plotly_chart(fig)

st.text('')
st.markdown('''A simple vista vemos que 'Height' y 'Weight' tienen nula correlación. Por lo que procederemos a eliminarlas''')
with st.echo():
    dfmodel.drop(['Height(in cm)', 'Weight(in kg)'], axis=1, inplace= True)

st.markdown('Por otro lado, debemos transformar las variables object.')
st.markdown('En nuestro caso, son variables que se refieren al rendimiento ofensivo y defensivo. Cuyos valores pueden ser Low - Medium - High.')
st.markdown('Teniendo en cuenta que todos los atributos y estadísticas van del 1 al 99. Les daremos un valor de 33, 66, 99 respectivamente.')
st.markdown('Hemos recurrido a esta opción puesto que aplicar OneHotEncoder empeoraba mucho los resultados')
with st.echo():
    dfmodel['Attacking Work Rate'].replace({'Low': 33, 'Medium': 66, 'High': 99}, inplace=True)
    dfmodel['Defensive Work Rate'].replace({'Low': 33, 'Medium': 66, 'High': 99}, inplace=True)

st.markdown('Después de estos cambios, tenemos listo nuestro dataset para comenzar a trabajar.')
with st.expander('Ver dataset para el modelo'):
    st.dataframe(dfmodel)

st.markdown('Comenzamos a separar los datos entre train y test')
with st.echo():
    from sklearn.model_selection import train_test_split
    train, test = train_test_split(dfmodel, test_size=0.075, random_state=10)

    #Creamos las variables de train y test
    X_train = train.drop(["Potential"], axis=1)
    Y_train = train["Potential"]
    X_test  = test.drop(["Potential"], axis=1)
    Y_test = test["Potential"]
    X_train.shape, Y_train.shape, X_test.shape, Y_test.shape

st.subheader('ElasticNet')
with st.echo():
    
    from sklearn.linear_model import ElasticNet
    #Inicializamos modelo y parámetros
    alpha = .15 #Parámetro que mide el peso que tienen los regularizadores frente a la función original
    l1_ratio = .15 #Parámetro que mide el tradeoff entre el peso l1 y el l2
    #Instanciamos el modelo
    model = ElasticNet(alpha = alpha, l1_ratio = l1_ratio, max_iter = 200, random_state = 10)
    #Entrenamos modelo y elaboramos predicciones
    model.fit(X_train, Y_train)
    prediccionEN = model.predict(X_test)
    mse_ElasticNet = mean_squared_error(Y_test, prediccionEN)

st.text('')
st.subheader('SVR')
with st.echo():
    
    from sklearn import svm
    #Inicializamos modelo y parámetros
    C = 1 #Parámetro regularizador
    kernel = 'rbf' #Núcleo transformador
    #Instanciamos el modelo
    model = svm.SVR(C = C, kernel = kernel)
    #Entrenamos modelo y elaboramos predicciones
    model.fit(X_train, Y_train)
    prediccionSVR = model.predict(X_test)
    mse_SVR = mean_squared_error(Y_test, prediccionSVR)

st.text('')
st.subheader('Random Forest Regressor')
with st.echo():
    
    from sklearn.ensemble import RandomForestRegressor
    #Inicializamos modelo y parámetros
    n_estimators = 200 #Estimadores del modelo
    criterion = 'mse' #Forma de calcular el error
    max_depth = None #Límite de profundidad de los árboles
    min_samples_split = 2 #Criterio de parada de profundidad
    verbose = 1 #Información devuelta por el método
    #Instanciamos el modelo
    model = RandomForestRegressor(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, verbose=verbose)
    #Entrenamos modelo y elaboramos predicciones
    model.fit(X_train, Y_train)
    prediccionRF = model.predict(X_test)
    mse_RF = mean_squared_error(Y_test, prediccionRF)

st.text('')
st.subheader('Boosting: Gradient Descent')
with st.echo():
    
    import xgboost as xgb
    #Inicializamos modelo y parámetros
    params = {"booster":"gbtree", "max_depth": 2, "eta": 0.3, "objective": "reg:squarederror", "nthread":2}
    num_boost_round = 10
    #Convertimos los datos a formato DMatrix
    train_data = xgb.DMatrix(X_train, label=Y_train)
    test_data = xgb.DMatrix(X_test, label=Y_test)
    #Instanciamos el modelo, entrenamos y elaboramos predicciones
    model = xgb.train(params = params, dtrain = train_data, num_boost_round=num_boost_round)
    prediccionXGB = model.predict(test_data)
    mse_XGB = mean_squared_error(Y_test, prediccionXGB)

st.text('')
st.subheader('Resultados')
st.markdown('Después de ejecutar todos los algoritmos, vamos a plotear los errores cuadráticos medios obtenidos para compararlos')
mse = [mse_ElasticNet, mse_SVR, mse_RF, mse_XGB]
modelos = ['ElasticNet', 'SVR', 'RF', 'XGB']
fig2 = px.scatter(x=modelos, y= mse, height=400, width=600)
fig2.update_layout(yaxis_title=None, xaxis_title = None)
st.plotly_chart(fig2)

st.text('')
st.text('')
st.markdown('En este caso vamos a elegir el modelo de Random Forest como el más idóneo para la predicción de "Potential".')
ejey = np.array(Y_test)
st.markdown('Vamos a graficarlo para poder verlo mejor, desde 2 perspectivas.')
col1,col2 = st.columns(1.2,0.8)
with col1:
    fig3 = px.scatter(x = ejey, y = prediccionRF)
    st.plotly_chart(fig3)
with col2:
    fig4 = plt.scatter(ejey, prediccionRF, alpha=0.3)
    st.pyplot(fig4)

