import streamlit as st
import requests
from datetime import datetime
import locale
import pandas as pd

try: 
    locale.setlocale(locale.LC_ALL, 'pt_BR') 
except: 
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil') 

def filtra_entradas():
    st.subheader("Listar Entradas")
    default_mes = datetime.now().strftime('%B').lower()
    default_ano = datetime.now().strftime('%Y')
    mes = st.selectbox("Mês",( "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"))
    ano = st.selectbox("Ano", (2022, 2023, 2024))
    consultar = st.button("Consultar")
    if consultar == False:
        dados = requests.get(f"http://localhost:5000/entradas/{default_mes}/{default_ano}")
        dados = dados.json()
        entrada_descricao = []
        entrada_valor = []
        usuario = []
        conta = []
        for dado in dados["Entradas"]:
            usuario_id = dado["usuario_id"]
            conta_id = dado["conta_id"]
            usuario_nome = requests.get(f"http://localhost:5000/usuarios/{usuario_id}")
            usuario_nome = usuario_nome.json()
            conta_nome = requests.get(f"http://localhost:5000/contas/{conta_id}")
            conta_nome = conta_nome.json()
            conta.append(conta_nome["contas"]["conta_nome"])
            usuario.append(usuario_nome["Usuarios"]["usuario_nome"])
            entrada_descricao.append(dado["entrada_descricao"])
            valor = "R$"+str(dado["entrada_valor"])
            entrada_valor.append(valor)

        dataframe = {"Descrição": entrada_descricao, "Valor": entrada_valor, "Responsável": usuario, "Conta": conta}
        df = pd.DataFrame(data=dataframe)
        st.subheader("Hoje:")
        st.table(df)

    else:
        dados = requests.get(f"http://localhost:5000/entradas/{mes}/{ano}")
        dados = dados.json()
        entrada_descricao = []
        entrada_valor = []
        usuario = []
        conta = []
        for dado in dados["Entradas"]:
            usuario_id = dado["usuario_id"]
            conta_id = dado["conta_id"]
            usuario_nome = requests.get(f"http://localhost:5000/usuarios/{usuario_id}")
            usuario_nome = usuario_nome.json()
            conta_nome = requests.get(f"http://localhost:5000/contas/{conta_id}")
            conta_nome = conta_nome.json()
            conta.append(conta_nome["contas"]["conta_nome"])
            usuario.append(usuario_nome["Usuarios"]["usuario_nome"])
            entrada_descricao.append(dado["entrada_descricao"])
            valor = "R$"+str(dado["entrada_valor"])
            entrada_valor.append(valor)

        dataframe = {"Descrição": entrada_descricao, "Valor": entrada_valor, "Responsável": usuario, "Conta": conta}
        df = pd.DataFrame(data=dataframe)
        st.table(df)

def cria_atualiza_remove_entrada():
    st.subheader("Adicionar/Atualizar Entrada")
    seleciona = st.selectbox("Selecione a opção:", (" ","Criar", "Atualizar", "Remover"))
    if seleciona == "Criar":
        lista_responsaveis = requests.get("http://localhost:5000/usuarios")
        lista_responsaveis = lista_responsaveis.json()
        responsavel_nome = []
        for responsavel in lista_responsaveis["Usuarios"]:
            responsavel_nome.append(responsavel["usuario_nome"])
        nome = st.text_input("Nome da entrada:")
        responsavel = st.selectbox("Nome do responsável:", responsavel_nome)
        valor = st.number_input("Informe o valor:")
        mes = st.selectbox("Selecione o mês",( "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"))
        ano = st.selectbox("Selecione o ano", (2022, 2023, 2024))
        lista_contas = requests.get("http://localhost:5000/contas")
        lista_contas = lista_contas.json()
        conta_nome = []
        for conta in lista_contas["Contas"]:
            conta_nome.append(conta["conta_nome"])
        conta = st.selectbox("Nome da Conta:", conta_nome)
        criar = st.button("Adicionar Entrada")

        id_usuario = requests.get(f"http://localhost:5000/usuarios/nome/{responsavel}")
        id_usuario = id_usuario.json()
        id_conta = requests.get(f"http://localhost:5000/contas/nome/{conta}")
        id_conta = id_conta.json()
        if criar == True:
            body = {
                "entrada_descricao": nome,
                "usuario_id": id_usuario["Usuarios"]["usuario_id"],
                "entrada_valor": valor,
                "mes_nome": mes,
                "mes_ano": ano,
                "conta_id": id_conta["contas"]["conta_id"]
            }
            try:
                requests.post("http://localhost:5000/entradas", json=body)
                st.balloons()
                return st.success("Sucesso ao incluir Entrada")
            except Exception as e:
                return st.error(f"Falha ao criar entrada: {e}")


    if seleciona == "Atualizar":
        st.write("Atualizar")
