from flask import request, Response
import json
from main import app
from modules.contas import contas_seleciona_todos, contas_seleciona_um, contas_criar, contas_atualiza, contas_deleta, contas_filtra_nome
from modules.entradas import entradas_seleciona_todos, entradas_seleciona_um, entradas_criar, entradas_atualiza, entradas_deleta, entradas_filtro_mes_ano
from modules.usuarios import usuarios_seleciona_todos, usuarios_seleciona_um, usuarios_criar, usuarios_atualiza, usuarios_deleta, usuarios_filtra_nome
from modules.saidas import saidas_seleciona_todos, saidas_seleciona_um, saidas_criar, saidas_atualiza, saidas_deleta, saidas_filtro_mes_ano

####################### CONTAS ############################
#Endpoint GET /contas para listar todos as contas
@app.route("/contas", methods=["GET"])
def seleciona_contas():
    return contas_seleciona_todos()

#Endpoint GET /contas/<id> para lista apenas uma conta
@app.route("/contas/<id>", methods=["GET"])
def seleciona_conta(id):
    return contas_seleciona_um(id)

#Endpoint GET /contas/<id> para lista apenas uma conta
@app.route("/contas/nome/<nome>", methods=["GET"])
def filtra_conta_nome(nome):
    return contas_filtra_nome(nome)

#Endpoint POST /contas para incluir uma nova conta
@app.route("/contas", methods=["POST"])
def cria_contas():
    body = request.get_json()
    return contas_criar(body)

#Endpoint PUT /contas/<id> para atualizar uma conta
@app.route("/contas/<id>", methods=["PUT"])
def atualiza_contas(id):
    body = request.get_json()
    return contas_atualiza(id, body)

#Endpoint DELETE /contas/<id> para deletar uma conta
@app.route("/contas/<id>", methods=["DELETE"])
def deleta_contas(id):
    return contas_deleta(id)

####################### ENTRADAS ############################

#Endpoint GET /entradas para listar todos as Entradas
@app.route("/entradas", methods=["GET"])
def seleciona_entradas():
    return entradas_seleciona_todos()

#Endpoint GET /entradas/<id> para lista apenas uma entrada
@app.route("/entradas/<id>", methods=["GET"])
def seleciona_entrada(id):
    return entradas_seleciona_um(id)

#Endpoint POST /entradas para incluir uma nova entrada
@app.route("/entradas", methods=["POST"])
def cria_entidade():
    body = request.get_json()
    return entradas_criar(body)

#Endpoint PUT /entradas/<id> para atualizar uma entrada
@app.route("/entradas/<id>", methods=["PUT"])
def atualiza_entradas(id):
    body = request.get_json()
    return entradas_atualiza(id, body)

#Endpoint DELETE /entradas/<id> para deletar uma entrada
@app.route("/entradas/<id>", methods=["DELETE"])
def deleta_entradas(id):
    return entradas_deleta(id)

#Endpoint GET /entradas/<mes>/<ano> para filtrar mes e ano das entradas
@app.route("/entradas/<mes>/<ano>", methods=["GET"])
def filtra_mes_ano_entradas(mes, ano):
    return entradas_filtro_mes_ano(mes, ano)

####################### USUARIOS ############################
#Endpoint GET /usuarios para listar todos os Dispositivos
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    return usuarios_seleciona_todos()

#Endpoint GET /usuarios/<id> para lista apenas um Dispositivo
@app.route("/usuarios/<id>", methods=["GET"])
def seleciona_usuario(id):
    return usuarios_seleciona_um(id)

#Endpoint POST /usuarios para incluir um novo dispositivo
@app.route("/usuarios", methods=["POST"])
def cria_usuarios():
    body = request.get_json()
    return usuarios_criar(body)

#Endpoint PUT /usuarios/<id> para atualizar um Dispositivo
@app.route("/usuarios/<id>", methods=["PUT"])
def atualiza_usuarios(id):
    body = request.get_json()
    return usuarios_atualiza(id, body)

#Endpoint DELETE /usuarios/<id> para deletar um dispositivo
@app.route("/usuarios/<id>", methods=["DELETE"])
def deleta_usuarios(id):
    return usuarios_deleta(id)

@app.route("/usuarios/nome/<nome>", methods=["GET"])
def filtra_usuarios_nome(nome):
    return usuarios_filtra_nome(nome)

####################### SAIDAS ############################
#Endpoint GET /saidas para listar todos as saidas
@app.route("/saidas", methods=["GET"])
def seleciona_saidas():
    return saidas_seleciona_todos()

#Endpoint GET /saidas/<id> para lista apenas uma saida
@app.route("/saidas/<id>", methods=["GET"])
def seleciona_saida(id):
    return saidas_seleciona_um(id)

#Endpoint POST /saidas para incluir uma nova saida
@app.route("/saidas", methods=["POST"])
def cria_saidas():
    body = request.get_json()
    return saidas_criar(body)

#Endpoint PUT /saidas/<id> para atualizar uma saida
@app.route("/saidas/<id>", methods=["PUT"])
def atualiza_saidas(id):
    body = request.get_json()
    return saidas_atualiza(id, body)

#Endpoint DELETE /saidas/<id> para deletar uma saida
@app.route("/saidas/<id>", methods=["DELETE"])
def deleta_saidas(id):
    return saidas_deleta(id)
    
@app.route("/saidas/<mes>/<ano>", methods=["GET"])
def filtra_mes_ano_saidas(mes, ano):
    return saidas_filtro_mes_ano(mes, ano)
##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")

#Inicializador Flask
app.run()

