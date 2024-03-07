import streamlit as st
import re
import functions
import json
from utils.utils import gradientDescentAdam, convert_result
import numpy as np

def app():
    # page title
    st.title('Novo Vírus')
    st.markdown("---")
    
    # Add "Sobre" button at the top right of the page
    cols = st.columns(4)
    with cols[3]:
        with st.expander("Info"):
            st.info("Para mais informações, visite a aba \"Sobre\".", icon="ℹ")
    
    # subtitle
    st.subheader("Insira as proteínas do hospedeiro:")
    
    # creating columns to receive input from the user
    # first, the virus proteins
    cols1, cols2 = st.columns(2)
    
    # left side will give the option to the user to put manually the proteins
    with cols1:
        virus_prots_list = st.text_area(
        "Insira as proteínas separadas por vírgula",
        placeholder="proteina1, proteina2,...",
        )
    # right side will give the option to the user to upload a file with the proteins
    with cols2:
        virus_prots_file = st.file_uploader("Insira um arquivo com uma proteína em cada linha")
    
    # if the user upload a file, get the values into a list named "prots"
    if virus_prots_file is not None:
        prots_lines = virus_prots_file.readlines()
        prots = [i.decode( "utf-8" ).replace("\n", "").replace("\r", "").strip() for i in prots_lines]
    # else, if the user pass the values in the text box, parse it and store into the "prots" list
    elif virus_prots_list is not None:
        prots = re.split(';|,|\n', virus_prots_list)
        prots = [i.replace("\n", "").replace("\r", "").strip() for i in prots]
        
    
    
    #### virus information
    
    # genes
    st.subheader("Insira os genes que foram testados:")
    cols1, cols2 = st.columns(2)
    # left side will give the option to the user to put manually the proteins
    with cols1:
        genes_list = st.text_area(
        "Insira o nome dos genes separados por vírgula",
        placeholder="gene1, gene2,...",
        )
    # right side will give the option to the user to upload a file with the proteins
    with cols2:
        genes_file = st.file_uploader("Insira um arquivo com um gene em cada linha")
    
    # if the user upload a file, get the values into a list named "genes"
    if genes_file is not None:
        genes_lines = genes_file.readlines()
        genes = [i.decode( "utf-8" ).replace("\n", "").replace("\r", "").strip() for i in genes_lines]
    # else, if the user pass the values in the text box, parse it and store into the "genes" list
    elif genes_list is not None:
        genes = re.split(';|,|\n', genes_list)
        genes = [i.replace("\n", "").replace("\r", "").strip() for i in genes]
    
    # genes expressions
    st.subheader("Insira o perfil de expressão gênica das infecções virais para os genes testados, separado por vírgula:\n(1 para genes superexpressos, -1 para genes subexpressos e 0 para genes sem diferença de expressão)")
    cols1, cols2 = st.columns(2)
    # left side will give the option to the user to put manually the proteins
    with cols1:
        expressions_list = st.text_area(
        "Insira a expressão dos genes separadas por vírgula",
        placeholder="expressao1, expressao2,...",
        )
    # right side will give the option to the user to upload a file with the proteins
    with cols2:
        expressions_file = st.file_uploader("Insira um arquivo com uma expressão em cada linha")
    # if the user upload a file, get the values into a list named "expressions"
    if expressions_file is not None:
        expressions_lines = expressions_file.readlines()
        expressions = [i.decode( "utf-8" ).replace("\n", "").replace("\r", "").strip() for i in expressions_lines]
    # else, if the user pass the values in the text box, parse it and store into the "expressions" list
    elif expressions_list is not None:
        expressions = re.split(';|,|\n', expressions_list)
        expressions = [i.replace("\n", "").replace("\r", "").strip() for i in expressions]
    
    # result 
    resultado = {}
    
    if prots and genes and expressions:
        if prots[0] and genes[0] and expressions[0]:
            # get Q vector to add in the B matrix before running the gradient
            Q_linha = functions.get_b_vector(prots, functions.client)
            # get W vector to add in the G matrix before running the gradient
            W_linha = functions.get_g_vector(genes, expressions)
            # run gradient algorithm to get the scores and values to return to the user
            resultado = gradientDescentAdam(functions.A, np.vstack([functions.B, Q_linha]), np.vstack([functions.G, W_linha]))
    
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


