import streamlit as st
import requests
import pandas as pd

url = "http://localhost:5000/"

# Função que exibe na interface todas os usuarios cadastrados no banco de dados
def filtra_usuarios():
    st.subheader("Usuários")
    # Request para coletar todos os usuarios da API
    usuarios = requests.get(url+"/usuarios")
    usuarios = usuarios.json()

    # Variáveis globais para o armazenamento dos usuarios
    usuarios_ids = []
    usuarios_nomes = []

    # Loop para varrer todo o objeto criado pela API de usuarios
    for usuario in usuarios["Usuarios"]:
        # Variaveis de atribuição
        usuario_id = usuario["usuario_id"]
        usuario_nome = usuario["usuario_nome"]
        
        # Atribuições dos parãmetros dentro das variáveis globais
        usuarios_ids.append(usuario_id)
        usuarios_nomes.append(usuario_nome)

    # Criação do dataframe com Pandas para a exibição da tabela na interface WEB
    dataframe = {"ID": usuarios_ids, "Nome": usuarios_nomes}
    df = pd.DataFrame(data=dataframe)
    df.set_index("ID", inplace=True)
    st.table(df)

# Função que exibe na interface web para Criação, Atualização ou Exclusão de usuarios
def cria_atualiza_remove_usuario():
    # Inclusão dos campos na interface WEB
    st.subheader("Ajustes")
    seleciona = st.selectbox("Selecione a opção:", (" ","Criar", "Atualizar", "Remover"))

    # IF para alterar a interface caso seja selecionado a opção para Criar usuario
    if seleciona == "Criar":
        
        # Criação dos campos na interface WEB
        usuario_nome = st.text_input("Nome do usuário:")
        adicionar = st.button("Adicionar usuário")
        
        # IF para criação do usuario caso ele seja precionado
        if adicionar == True:
            # Validação de erros
            if usuario_nome == None or usuario_nome == "":
                return st.error("Falha ao criar usuario! Mensagem: O nome do usuario deve ser informado")

            # Criação do body para informar na API
            body = {
                "usuario_nome": usuario_nome
            }

            # Request para realizar o POST na API para a criação do usuario
            try:
                requests.post("http://localhost:5000/usuarios", json=body)
                return st.success("Usuario incluido com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao criar usuario! Mensagem: {e}")

    # IF para alterar a interface caso seja selecionado a opção para Atualizar usuario
    if seleciona == "Atualizar":
        # Request para coletar todas os usuarios da API
        usuarios = requests.get(url+"/usuarios")
        usuarios = usuarios.json()

        # Request para coletar os usuários criados na Plataforma
        lista_usuarios = requests.get(url+"/usuarios")
        lista_usuarios = lista_usuarios.json()

        # Variável global para o armazenamento dos usuarios
        usuarios_ids = []
        
        # Loop para varrer todo o objeto criado pela API de usuarios
        for usuario in lista_usuarios["Usuarios"]:
            # Atribuições dos parãmetros dentro das variáveis globais
            usuarios_ids.append(usuario["usuario_id"])

        # Criação dos campos na interface WEB
        usuario_id = st.selectbox("Número do usuário", (usuarios_ids))
        usuario_nome = st.text_input("Novo nome do usuário:")
        adicionar = st.button("Atualizar Conta")

        # IF para atualização do usuario caso ele seja precionado
        if adicionar == True:
            # Criação do body para informar na API
            body = {
                "usuario_nome": usuario_nome
            }

            # Request para realizar o POST na API para a atualização do usuário
            try:
                requests.put(f"http://localhost:5000/usuarios/{usuario_id}", json=body)
                return st.success("Usuario incluída com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao atualizar usuario! Mensagem: {e}")

# IF para alterar a interface caso seja selecionado a opção para Deletar usuario
    if seleciona == "Remover":
        # Request para coletar todas os usuarios da API
        usuarios = requests.get(url+"/usuarios")
        usuarios = usuarios.json()

        # Variável global para o armazenamento dos usuarios
        usuarios_ids = []

        # Loop para varrer todo o objeto criado pela API de usuarios
        for usuario in usuarios["Usuarios"]:
            usuarios_ids.append(usuario["usuario_id"])

        # Criação dos campos na interface WEB
        conta_id = st.selectbox("Número do usuário", (usuarios_ids))
        deletar = st.button("Deletar Conta")

        # IF para atualização da conta caso ele seja precionado
        if deletar == True:
            # Request para realizar o POST na API para a remoção do usuario
            try:
                requests.delete(url+f"/usuarios/{conta_id}")
                return st.success("Usuario deletada com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao deletar usuario! Mensagem: {e}")

