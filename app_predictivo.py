from codigo_ejecucion import *
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'MEIDAT',
     page_icon = 'meidat.png',
     layout = 'wide')

#MAIN
st.title('MEIDAT - MANTENIMIENTO PREVENTIVO')

#SIDEBAR
with st.sidebar:
    st.image('meidat.jpg')

#CARGA DE DATOS

    archivo = st.file_uploader('Selecciona un archivo csv')

    @st.cache()
    def cargar_datos(archivo):
        if archivo is not None:
            df = pd.read_csv(archivo,index_col= 'Date', sep = ',')
        else:
            st.stop()
        return(df)

    df = cargar_datos(archivo)
    st.write('Archivo cargado sactifactoriamente')

#INPUTS DE LA APLICACIÓN

    campaña = st.selectbox('Tipo de campaña', ['Esparrago','Judia'])
    personal_prod = st.slider('Personal de producción', 1, 20)
    volumen = st.number_input("Volumen de producción (kg)", 1, 1000)
    otro = st.number_input("Otros Costes (€)", 1, 10000)

#Valores fijos
    horas_arreglo = 5
    euros_hora = 15
    personal_mant = 2
    valor_esparrago = 0.5
    valor_judia = 0.3


#CALCULOS

impacto_judia = int(horas_arreglo * (personal_prod *euros_hora + personal_mant*euros_hora) + volumen * valor_judia + otro)
impacto_esparrago = int(horas_arreglo * (personal_prod *euros_hora + personal_mant*euros_hora) + volumen * valor_esparrago + otro)


#EJECUCIÓN DEL PIPE
if st.sidebar.button('CLICK PARA CALCULAR'):
    scoring = ejecutar_modelo(df)
    scoring = int(scoring)
    
    if campaña == 'Esparrago':
        perdida = int(impacto_esparrago * scoring/100)
        impacto = impacto_esparrago
    else:
        perdida = int(impacto_judia * scoring/100)
        impacto = impacto_judia

    pd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "PD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": scoring, "name": "%"}],
                }
            ],
        }
    
    
    st.write('La probabilidad de fallo por avería es de:')
    st_echarts(options=pd_options,width = "85%")
        
#kpis
    col1,col2 = st.columns(2)
    with col1:
        st.write('El valor económico del proceso es (Euros):')
        st.metric(label="Valor económico €", value=impacto, delta="- Impacto",delta_color="normal")
    with col2:
        st.write('La pérdida esperada es de (Euros):')
        st.metric(label="Pérdida esperada €", value=perdida, delta="- Pérdida",delta_color="normal")
else:
    st.write('DEFINE LOS PARÁMETROS DE LA LÍNEA DE PRODUCCIÓN Y HAZ CLICK EN CALCULAR % AVERÍA')