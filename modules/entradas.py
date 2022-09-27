from main import db
from flask import Response
import json

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Entradas(db.Model):
    entrada_id = db.Column(db.Integer, primary_key = True)
    entrada_descricao = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer)
    entrada_valor = db.Column(db.Float)
    mes_nome = db.Column(db.String(50))
    mes_ano = db.Column(db.Integer)
    conta_id = db.Column(db.Integer)


    def to_json(self):
        return {"entrada_id": self.entrada_id,
                "entrada_descricao": self.entrada_descricao,
                "usuario_id": self.usuario_id,
                "entrada_valor": self.entrada_valor,
                "mes_nome": self.mes_nome,
                "mes_ano": self.mes_ano,
                "conta_id": self.conta_id
                }

#Endpoint GET /entradas para listar todos as entradas
def entradas_seleciona_todos():
    entradas = Entradas.query.all()
    entradas_json = [entrada.to_json() for entrada in entradas]
    return gera_response(200, "Entradas", entradas_json, "Entradas listadas com sucesso")

#Endpoint GET /entradas/<id> para lista apenas uma entradas
def entradas_seleciona_um(id):
    entradas = Entradas.query.filter_by(entrada_id=id).first()
    entradas_json = entradas.to_json()
    return gera_response(200, "Entradas", entradas_json, "Entradas listadas com sucesso")

#Endpoint POST /entradas para incluir uma nova entrada
def entradas_criar(body):
    try:
        entrada = Entradas(
            entrada_descricao=body["entrada_descricao"],
            usuario_id=body["usuario_id"],
            entrada_valor=body["entrada_valor"],
            mes_nome=body["mes_nome"],
            mes_ano=body["mes_ano"],
            conta_id=body["conta_id"]
        )
        db.session.add(entrada)
        db.session.commit()
        return gera_response(201, "Entradas", entrada.to_json(), "entrada criada com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Entradas", {}, f"Erro ao Cadastrar entrada:{e}")

#Endpoint PUT /entradas/<id> para atualizar uma Entidade
def entradas_atualiza(id, body):
    entradas = Entradas.query.filter_by(entrada_id=id).first()
    try:
        if "entrada_descricao" in body:
            entradas.entrada_descricao = body["entrada_descricao"]
        if "usuario_id" in body:
            entradas.usuario_id = body["usuario_id"]
        if "entrada_valor" in body:
            entradas.entrada_valor = body["entrada_valor"]
        if "mes_id" in body:
            entradas.mes_id = body["mes_id"]
        if "conta_id" in body:
            entradas.conta_id = body["conta_id"]

        db.session.add(entradas)
        db.session.commit()
        return gera_response(200, "Entradas", entradas.to_json(), "entrada atualizada com sucesso")
    except Exception as e:
        return gera_response(400, "Entradas", {}, f"Erro ao Atualizar entrada:{e}")

#Endpoint DELETE /entradas/<id> para deletar uma entrada
def entradas_deleta(id):
    entradas = Entradas.query.filter_by(entrada_id=id).first()
    try:
        db.session.delete(entradas)
        db.session.commit()
        return gera_response(200, "Entradas", entradas.to_json(), "entrada deletado com sucesso")
    except Exception as e:
        return gera_response(400, "Entradas", {}, f"Erro ao deletar entrada:{e}")

def entradas_filtro_mes_ano(mes, ano):
    try:
        entradas = Entradas.query.filter(Entradas.mes_ano==ano, Entradas.mes_nome==mes)
        entradas_json = [entrada.to_json() for entrada in entradas]
        return gera_response(200, "Entradas", entradas_json, "Entradas listadas com sucesso")
    except Exception as e:
        return gera_response(400, "Entradas", {}, f"Erro ao filtrar entrada:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
