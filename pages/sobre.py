import streamlit as st
from functions import proteinas, virus, genes

def app():
# Título da página
    st.title('Sobre')
    st.markdown("---")
    
    st.markdown("""Mostraremos aqui alguns detalhes sobre as proteínas, vírus e genes
                presentes na base para facilitar o uso da interface.""")
    
    tab_labels = ["Proteínas", "Vírus", "Genes", "Resultado"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_labels)
    
    with tab1:
       st.header(tab_labels[0])
       with st.expander("Clique para ver as proteínas"):
           st.write(f"Temos aqui uma lista com as {len(proteinas)} proteínas (IDs do Drugbank) presentes na base:")
           st.write(proteinas)
       
    
    with tab2:
       st.header(tab_labels[1])
       with st.expander("Clique para ver os vírus"):
           st.write(f"Temos aqui uma lista com os {len(virus)} vírus presentes na base:")
           st.write(virus)
    with tab3:
       st.header(tab_labels[2])
       st.write("As expressões genéticas que devem que devem ser fornecidas juntamente com os seus genes têm as seguintes possibilidades:")
       st.markdown(f"""
                    - 0: indica que não houve mudança significativa de expressão
                    - -1: indica genes subexpressos, 
                    - 1:  indica genes superexpressos
                    """)
       with st.expander("Clique para ver os genes"):
           st.write(f"Temos aqui uma lista com os {len(genes)} genes presentes na base:")
           st.write(genes)
    with tab4:
       st.header(tab_labels[3])
       
       st.write("""O resultado disponibilizado consiste em um json com os scores (Matriz $\hat{X} = D\cdot V^T$) 
                e as matrizes $D$, $V$, $P$ e $U$.""")
       st.markdown("""
        ```json
        {
            'scores': array([[...]]),
            'D': array([[...]]),
            'V': array([[...]]),
            'P': array([[...]]),
            'U': array([[...]])
        }
        ```
        """)
    
    st.divider()
    st.subheader("Informações")   
    st.markdown("""Essa interface faz parte do projeto de TCC elaborado como requisito 
            para o grau de bacharel em Ciência de Dados na Escola de Matemática
             Aplicada da FGV Rio. Este trabalho teve como tema \"Implementação 
             de uma nova abordagem de decomposição de matriz para o reposicionamento 
             de drogas antivirais\".""")
    

