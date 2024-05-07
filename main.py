import streamlit as st
import pandas as pd
from datetime import date
# import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
from streamlit_datetime_range_picker import datetime_range_picker
import datetime
import math
# %matplotlib inline



st.set_page_config(page_title="Reach", page_icon="🆙")
target = ['Individuos', 'Hombres', 'Mujeres','Rch']
st.sidebar.image("./media_stock/upartnercolor.png", use_column_width=True)

st.sidebar.image("./media_stock/media_diamond.png", use_column_width=True)

titulo =  "<p><FONT SIZE=5><span style='color:black;font-weight:bold'> <br>TARGET </span> </font></p>"

st.sidebar.markdown(titulo, unsafe_allow_html=True)



with st.sidebar:
    mode = st.sidebar.selectbox("Tipo de individuo", target)

with st.sidebar:                                      
    edad = st.sidebar.slider('Edad', 0, 100, (0,100))
    edad_cmp_inicio = edad[0]
    edad_cmp_fin = edad[1]
    
with st.sidebar:
    obj = st.sidebar.selectbox("Reach", ['Maximizar Reach', 'Optimizar Presupuesto'])

    if obj == 'Optimizar Presupuesto':
        reach = st.sidebar.text_input('Reach', '')
        # reach = 

with st.sidebar:
    pres = st.sidebar.text_input("Presupuesto", 100000)

with st.sidebar:
    
    today = datetime.date.today() 
    

    start_date = today - datetime.timedelta(days=30)
    

    start_date = st.date_input('Fecha inicial', value=start_date)
    end_date = st.date_input('Fecha final', value=today)
    
with st.sidebar:
    medios = ['SOCIAL MEDIA','TOTAL ONLINE','TV','PRENSA','REVISTAS Y SSDD','RADIO','OOH','CINE','PLATAFORMAS VOD','NETWORKS DISPLAY','PAID SOCIAL','INFLUENCERS','BRANDED CONTENT']
    medio = st.sidebar.multiselect('Selecciona los medios que se encuentran dentro del plan', medios)



############################################################################################################################################
###################################################     PASO 2      ########################################################################
############################################################################################################################################


A = {}
B = {}
C = {}

CGRP = {}
CPM = {}


audiencia = pd.read_excel('./data/Audiencias.xlsx')
audiencia_cmp = pd.read_excel('./data/Audiencias_campaña.xlsx')
costes = pd.read_excel('./data/Costes.xlsx')
potential_reach = pd.read_excel('./data/Potencial Reach.xlsx')


for i, item in enumerate(medio):
    st.markdown(f"# {item}")
    tipo = st.selectbox('Tipo de compra', ['DIRECT OFFLINE', 'DIRECT ONLINE', 'DIRECT MULTIMEDIA', 'BIDDING ONLINE', 'BIDDING MULTIMEDIA'], key=f"tipo_compra_{i}")

    modelo = st.selectbox('Modelo de compra', ['COSTE FIJO', 'CPM', 'C/GRP', 'FREE'], key=f"tipo_modelo{i}")
    tipo_ind = st.selectbox('Tipo individuo (TG de compra)', target, key=f"tipo_ind{i}")
    edad_comienzo_compra = st.text_input('Edad comienzo (TG de compra)', value=4, key = f"tipo_edad_com{i}")
    edad_fin_compra = st.text_input('Edad final (TG de compra)', value=99, key = f"tipo_edad_fin{i}")

    if edad_comienzo_compra is not "" and edad_fin_compra is not "" :
        edad_comienzo_compra = int(edad_comienzo_compra)
        edad_fin_compra = int(edad_fin_compra)
        universo_tg_compra = audiencia.loc[(audiencia['EDAD'] >= edad_comienzo_compra) & (audiencia['EDAD'] <= edad_fin_compra), tipo_ind].sum()
        universo_tg_campaña =  audiencia_cmp.loc[(audiencia_cmp['EDAD'] >= edad_cmp_inicio) & (audiencia_cmp['EDAD'] <= edad_cmp_fin), tipo_ind.upper()].sum()

    peso = st.text_input('Peso España', value= '100%', key = f"tipo_peso{i}")
    peso_dec = float(peso.strip('%')) / 100

    costes_medio = costes[costes['MEDIO']==item]
    costes_medio['CGRP'] = costes_medio['CGRP'].astype(float)
    coste_grp = costes_medio['CGRP']/peso_dec
    coste_cpm = costes_medio['CPM']/peso_dec



    POTENTIAL_REACH_TG_COMPRA =  (potential_reach.loc[(potential_reach['EDAD'] >= edad_comienzo_compra) & (potential_reach['EDAD'] <= edad_fin_compra), item].sum())/universo_tg_compra*100
    POTENTIAL_REACH_TG_CAMPAÑA =  (potential_reach.loc[(potential_reach['EDAD'] >= edad_cmp_inicio) & (potential_reach['EDAD'] <= edad_cmp_fin), item].sum())/universo_tg_campaña*100
    
    IX_AFINIDAD = POTENTIAL_REACH_TG_CAMPAÑA/POTENTIAL_REACH_TG_COMPRA*100


    if 'BIDDING' in tipo: 
        PESO_SEGMENTACION_ONLINE = 0
    else:
        PESO_SEGMENTACION_ONLINE = 1

    Porcentaje_ONCORE_PLANIFICADO = (PESO_SEGMENTACION_ONLINE) + universo_tg_campaña/universo_tg_compra*IX_AFINIDAD/100*(1-PESO_SEGMENTACION_ONLINE)


    IX_AFIN_PLANIFICADO = Porcentaje_ONCORE_PLANIFICADO/(universo_tg_campaña/universo_tg_compra)*100
    grp_tg_camapaña = int(coste_grp/IX_AFIN_PLANIFICADO*100)
    cpm_tg_campaña = float(coste_cpm/Porcentaje_ONCORE_PLANIFICADO)

    CGRP[item] = grp_tg_camapaña
    CPM[item] = cpm_tg_campaña
    st.write(cpm_tg_campaña)
   

############################################################################################################################################
###################################################     PASO 3      ########################################################################
############################################################################################################################################


    punto_grps = coste_cpm/coste_grp
    punto_reach = punto_grps/100


    punto_impresiones = 0.01*universo_tg_campaña*punto_grps
    punto_frecuencia = 0.01*punto_grps/punto_reach
    grps_1000 = punto_grps*1000
    punto_calculado_reach = POTENTIAL_REACH_TG_CAMPAÑA*0.65/100
    punto_calculado_frec = 3
    punto_calculado_grp = punto_calculado_reach*punto_calculado_frec*100
    punto_calculado_inversion = punto_calculado_grp*coste_grp

    punto_calculado_impresiones = punto_calculado_grp/100*universo_tg_campaña
    punto_calculado_grp1000 = punto_calculado_grp/1000


    
    y2 = punto_calculado_reach
    a_y2 = (POTENTIAL_REACH_TG_CAMPAÑA/100)-punto_calculado_reach
    y1 = punto_reach
    a_y1 = (POTENTIAL_REACH_TG_CAMPAÑA/100)-punto_reach
    x2 = punto_calculado_grp1000
    x1 = grps_1000
    calc_2 = math.log((y2*a_y1)/(y1*a_y2))
    calc_3 = math.log((x2/x1))
    c_ = calc_2 / calc_3
    A[item] = POTENTIAL_REACH_TG_CAMPAÑA/100
    B[item]  = int((x1**c_)*(a_y1/y1))
    C[item] = -1*c_
 
    # B[item] = B[item].split(' ')[1]
############################################################################################################################################
###################################################     PASO 4      ########################################################################
############################################################################################################################################

resultados_df = pd.DataFrame({
    'A': A,
    'B': B,
    'C': C,
    # 'CGRP': CGRP, 
    # 'CPM' : CPM
})
# st.write(resultados_df)


costes_curvas = pd.DataFrame({
    'CGRP': CGRP, 
    'CPM' : CPM
})




numeros = pd.Series(range(999, -1, -1))
pres = float(pres)
curva_total = pd.DataFrame()
curva_total['Trend'] =  numeros
curva_total['Inversión'] =  (curva_total['Trend']/999)*pres



resultados_transpuestos = resultados_df.T

for medio in resultados_transpuestos.index: 
    for variable in resultados_transpuestos.columns:  
        new_col_name = f"{medio}_{variable}"  
        curva_total[new_col_name] = resultados_transpuestos.loc[medio, variable]


for medio in resultados_transpuestos.columns:
    required_columns = [f'A_{medio}', f'B_{medio}', f'C_{medio}']
    if all(col in curva_total.columns for col in required_columns):
        curva_total[f'{medio}'] = curva_total.apply(
            lambda row: row[f'A_{medio}'] / (
                (1 + row[f'B_{medio}'] * 0.001 * row['Inversión'] / CGRP[medio]) ** row[f'C_{medio}']
            ), axis=1)
    else:
        print(f"Missing required columns for {medio}")

st.write()




plt.figure(figsize=(10, 5))

for medio in resultados_transpuestos.columns:
    
    plt.plot(curva_total[medio], curva_total.index, label=medio, marker='o', linestyle='-')


plt.xlabel('Inversión')  
plt.title('Potential Reach por medio') 
plt.legend() 


st.pyplot(plt)


plt.clf()

# defecto 100%
