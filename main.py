import streamlit as st
from pages import newDrug, newVirus, sobre

# setting page configuration
# this setting refers to the page title at the top of the browser tab, as well as the favicon
st.set_page_config(page_title= 'Projeto de TCC | EMAp - FGV', 
                   page_icon="https://raw.githubusercontent.com/GermanoAndrade/AED-Listas/main/Lista%203/Quest%C3%B5es/Cap%C3%ADtulo%204/FGV-EMAp.png", 
                   layout="wide",# 'centered' or 'wide'
                   initial_sidebar_state="expanded",# 'auto', 'expanded' or 'collapsed'
                   )

# these are the pages of the interface
PAGES = {'Nova Droga': newDrug,
         'Novo Vírus': newVirus,
         'Sobre'     : sobre}

# removing page footer
st.markdown(""" <style>
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# removing sidebar navigation list
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# removing "deploy" button from top right
st.markdown(""" <style>
.stDeployButton {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# adding information from the project in the interface
st.sidebar.markdown("---")
st.sidebar.header("Reposicionamento de Drogas")
st.sidebar.markdown("Projeto de TCC - 2023 | EMAp - FGV")
st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)

# creating list of options to navigate between pages
option = st.sidebar.radio('Ir para:', options=list(PAGES.keys()), index=0)
page = PAGES[option]

# adding footer to the sidebar
st.sidebar.markdown("""
---

Germano Andrade | Dezembro, 2023  
[<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" width="30px"> Github](https://github.com/GermanoAndrade/)

""", unsafe_allow_html=True)
#init.begin_variables()

page.app()




