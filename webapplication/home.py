import streamlit as st
from streamlit_option_menu import option_menu
from modules.entradas import filtra_entradas, cria_atualiza_remove_entrada
from modules.saidas import filtra_saidas, cria_atualiza_remove_saida
from modules.contas import filtra_contas, cria_atualiza_remove_conta
from modules.usuarios import filtra_usuarios, cria_atualiza_remove_usuario

st.set_page_config(layout="wide")

with st.sidebar:
    opcao = option_menu("Financeiro", ["Inicio", "Entradas", "Saidas", "Contas", "Usuarios"],
                         icons=['house', 'arrow-up', 'arrow-down', 'credit-card','people'],
                         menu_icon="currency-dollar", default_index=0)

if opcao == "Entradas":
    col1, col2 = st.columns(2)
    with col1:
        filtra_entradas()
    with col2:
        cria_atualiza_remove_entrada()

if opcao == "Saidas":
    col1, col2 = st.columns(2)
    with col1:
        filtra_saidas()
    with col2:
        cria_atualiza_remove_saida()

if opcao == "Contas":
    col1, col2 = st.columns(2)
    with col1:
        filtra_contas()
    with col2:
        cria_atualiza_remove_conta()

if opcao == "Usuarios":
    col1, col2 = st.columns(2)
    with col1:
        filtra_usuarios()
    with col2:
        cria_atualiza_remove_usuario()