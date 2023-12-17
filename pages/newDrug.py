import streamlit as st
import re
import functions
import json
from utils.utils import gradientDescentAdam, convert_result
import numpy as np

def app():
# Título da página
    st.title('Nova Droga')
    st.markdown("---")
    
    cols = st.columns(4)
    with cols[3]:
        with st.expander("Info"):
            st.info("Para mais informações, visite a aba \"Sobre\".", icon="ℹ")
    
    st.subheader("Insira as proteínas alvo das drogas:")
    
    
    
    cols1, cols2 = st.columns(2)
    with cols1:
        txt = st.text_area(
        "Insira as proteínas separadas por vírgula",
        placeholder="proteina1, proteina2,...",
        )
    with cols2:
        uploaded_file = st.file_uploader("Insira um arquivo com uma proteína em cada linha")
    
    
    
    if uploaded_file is not None:
        stringio = uploaded_file.readlines()
        prots = [i.decode( "utf-8" ).replace("\n", "").replace("\r", "").strip() for i in stringio]
    
        #st.write(len(stringio))
    elif txt is not None:
        prots = re.split(';|,|\n', txt)
        prots = [i.replace("\n", "").replace("\r", "").strip() for i in prots]
      
        
    resultado = {}
    
    if prots:
        if prots[0]:
            P_linha = functions.get_a_vector(prots, functions.client)
            resultado = gradientDescentAdam(np.vstack([functions.A, P_linha]), functions.B, functions.G)
    
    
    if resultado:
        st.divider()
        st.subheader("Resultado:")
        resultado = convert_result(resultado)
        cols = st.columns((1,2,1))
        with cols[1]:
            with st.expander("Resultado"):
                st.download_button(
                label="Download do json com os scores",
                data=json.dumps(resultado),
                file_name='scores.json',
                mime='text/csv',
                    )   
