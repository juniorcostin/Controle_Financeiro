import streamlit as st
import requests
import pandas as pd

url = "http://localhost:5000/"

# Função que exibe na interface todas as contas cadastradas no banco de dados
def filtra_contas():
    st.subheader("Contas")
    # Request para coletar todas as contas da API
    contas = requests.get(url+"/contas")
    contas = contas.json()

    # Variáveis globais para o armazenamento das contas
    contas_ids = []
    contas_nomes = []
    contas_limites = []
    contas_usuarios = []

    # Loop para varrer todo o objeto criado pela API de contas
    for conta in contas["Contas"]:
        # Variáveis para filtrar e transformar o ID do usuário em nome
        usuario_id = conta["usuario_id"]
        usuario_nome = requests.get(f"http://localhost:5000/usuarios/{usuario_id}")
        usuario_nome = usuario_nome.json()

        # Variáveis para filtrar e incluir o simbolo R$ na frente do valor do limite
        conta_limite = "R$"+str(conta["conta_limite"])
        
        # Atribuições dos parãmetros dentro das variáveis globais
        contas_ids.append(conta["conta_id"])
        contas_nomes.append(conta["conta_nome"])
        contas_limites.append(conta_limite)
        contas_usuarios.append(usuario_nome["Usuarios"]["usuario_nome"])


    # Criação do dataframe com Pandas para a exibição da tabela na interface WEB
    dataframe = {"ID": contas_ids, "Nome": contas_nomes, "Limite": contas_limites, "Responsável": contas_usuarios}
    df = pd.DataFrame(data=dataframe)
    df.set_index("ID", inplace=True)
    st.table(df)

# Função que exibe na interface web para Criação, Atualização ou Exclusão de contas
def cria_atualiza_remove_conta():
    # Inclusão dos campos na interface WEB
    st.subheader("Ajustes")
    seleciona = st.selectbox("Selecione a opção:", (" ","Criar", "Atualizar", "Remover"))

    # IF para alterar a interface caso seja selecionado a opção para Criar conta
    if seleciona == "Criar":
        # Request para coletar os usuários criados na Plataforma
        lista_usuarios = requests.get("http://localhost:5000/usuarios")
        lista_usuarios = lista_usuarios.json()
        # Variável global para o armazenamento dos usuarios
        conta_usuarios = []

        # Loop para varrer todo o objeto criado pela API de usuarios
        for usuario in lista_usuarios["Usuarios"]:
            # Atribuições dos parãmetros dentro das variáveis globais
            conta_usuarios.append(usuario["usuario_nome"])
        
        # Criação dos campos na interface WEB
        conta_nome = st.text_input("Nome da conta:")
        conta_limite = st.number_input("Limite da conta:")
        conta_usuario = st.selectbox("Nome do responsável:", (conta_usuarios))
        adicionar = st.button("Adicionar Conta")

        # Transformação do nome de usuário para ID
        id_usuario = requests.get(f"http://localhost:5000/usuarios/nome/{conta_usuario}")
        id_usuario = id_usuario.json()
        
        # IF para criação da conta caso ele seja precionado
        if adicionar == True:
            # Validação de erros
            if conta_nome == None or conta_nome == "":
                return st.error("Falha ao criar conta! Mensagem: O nome da conta deve ser informado")
            if conta_limite == None:
                return st.error("Falha ao criar conta! Mensagem: O limite da conta deve ser informado")
            if conta_usuario == None:
                return st.error("Falha ao criar conta! Mensagem: O usuario da conta deve ser informado")

            # Criação do body para informar na API
            body = {
                "conta_nome": conta_nome,
                "conta_limite": conta_limite,
                "usuario_id": id_usuario["Usuarios"]["usuario_id"]
            }

            # Request para realizar o POST na API para a criação da conta
            try:
                requests.post("http://localhost:5000/contas", json=body)
                return st.success("Conta incluida com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao criar conta! Mensagem: {e}")

    # IF para alterar a interface caso seja selecionado a opção para Atualizar conta
    if seleciona == "Atualizar":
        # Request para coletar todas as contas da API
        contas = requests.get(url+"/contas")
        contas = contas.json()

        # Request para coletar os usuários criados na Plataforma
        lista_usuarios = requests.get("http://localhost:5000/usuarios")
        lista_usuarios = lista_usuarios.json()

        # Variável global para o armazenamento dos usuarios
        conta_usuarios = []
        conta_ids = []

        # Loop para varrer todo o objeto criado pela API de usuarios
        for usuario in lista_usuarios["Usuarios"]:
            # Atribuições dos parãmetros dentro das variáveis globais
            conta_usuarios.append(usuario["usuario_nome"])

        # Loop para varrer todo o objeto criado pela API de contas
        for conta in contas["Contas"]:
            conta_ids.append(conta["conta_id"])

        # Criação dos campos na interface WEB
        conta_id = st.selectbox("Número da conta", (conta_ids))
        conta_nome = st.text_input("Novo nome da conta:", placeholder="Opcional")
        conta_limite = st.number_input("Novo limite da conta:")
        conta_usuario = st.selectbox("Novo nome do responsável:", (conta_usuarios))
        adicionar = st.button("Atualizar Conta")

        # Transformação do nome de usuário para ID
        id_usuario = requests.get(f"http://localhost:5000/usuarios/nome/{conta_usuario}")
        id_usuario = id_usuario.json()
        # IF para atualização da conta caso ele seja precionado
        if adicionar == True:
            # Criação do body para informar na API
            body = {
                "conta_nome": conta_nome,
                "conta_limite": conta_limite,
                "usuario_id": id_usuario["Usuarios"]["usuario_id"]
            }

            # Request para realizar o POST na API para a atualização da conta
            try:
                requests.put(f"http://localhost:5000/contas/{conta_id}", json=body)
                return st.success("Conta incluída com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao atualizar conta! Mensagem: {e}")

# IF para alterar a interface caso seja selecionado a opção para Atualizar conta
    if seleciona == "Remover":
        # Request para coletar todas as contas da API
        contas = requests.get(url+"/contas")
        contas = contas.json()

        # Variável global para o armazenamento dos usuarios
        conta_ids = []

        # Loop para varrer todo o objeto criado pela API de contas
        for conta in contas["Contas"]:
            conta_ids.append(conta["conta_id"])

        # Criação dos campos na interface WEB
        conta_id = st.selectbox("Número da conta", (conta_ids))
        deletar = st.button("Deletar Conta")

        # IF para atualização da conta caso ele seja precionado
        if deletar == True:
            # Request para realizar o POST na API para a atualização da conta
            try:
                requests.delete(url+f"/contas/{conta_id}")
                return st.success("Conta deletada com sucesso! Reinicie a página")
            except Exception as e:
                return st.error(f"Falha ao deletar conta! Mensagem: {e}")

