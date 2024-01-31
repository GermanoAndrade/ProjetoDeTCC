import streamlit as st
import re
import functions
import json
from utils.utils import gradientDescentAdam, convert_result
import numpy as np

def app():
    # Page title
    st.title('Nova Droga')
    st.markdown("---")

    # Add "Sobre" button at the top right of the page
    cols = st.columns(4)
    with cols[3]:
        with st.expander("Info"):
            st.info("Para mais informações, visite a aba \"Sobre\".", icon="ℹ")

    # subtitle
    st.subheader("Insira as proteínas alvo das drogas:")

    # creating columns to receive input from the user
    cols1, cols2 = st.columns(2)
    # left side will give the option to the user to put manually the proteins
    with cols1:
        txt = st.text_area(
        "Insira as proteínas separadas por vírgula",
        placeholder="proteina1, proteina2,...",
        )
    # right side will give the option to the user to upload a file with the proteins
    with cols2:
        uploaded_file = st.file_uploader("Insira um arquivo com uma proteína em cada linha")
    
    
    # if the user upload a file, get the values into a list named "prots"
    if uploaded_file is not None:
        stringio = uploaded_file.readlines()
        prots = [i.decode( "utf-8" ).replace("\n", "").replace("\r", "").strip() for i in stringio]
    
        #st.write(len(stringio))
    # else, if the user pass the values in the text box, parse it and store into the "prots" list
    elif txt is not None:
        prots = re.split(';|,|\n', txt)
        prots = [i.replace("\n", "").replace("\r", "").strip() for i in prots]
      
    # result    
    resultado = {}
    
    if prots:
        if prots[0]:
            P_linha = functions.get_a_vector(prots, functions.client)
            # run gradient algorithm to get the scores and values to return to the user
            resultado = gradientDescentAdam(np.vstack([functions.A, P_linha]), functions.B, functions.G)
    
    # creating a section to return the result to the user
    if resultado:
        st.divider()
        st.subheader("Resultado:")
        # create download button to allow user download the result as json
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
