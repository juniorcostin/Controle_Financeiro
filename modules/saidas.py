from main import db
from flask import Response
import json

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Saidas(db.Model):
    saida_id = db.Column(db.Integer, primary_key = True)
    saida_nome = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer)
    saida_data = db.Column(db.Date)
    saida_valor = db.Column(db.Float)
    mes_nome = db.Column(db.String(50))
    mes_ano = db.Column(db.Integer)
    conta_id = db.Column(db.Integer)


    def to_json(self):
        return {"saida_id": self.saida_id,
                "saida_nome": self.saida_nome,
                "usuario_id": self.usuario_id,
                "saida_data": self.saida_data,
                "mes_nome": self.mes_nome,
                "mes_ano": self.mes_ano,
                "conta_id": self.conta_id,
                "saida_valor": self.saida_valor
                }

#Endpoint GET /saidas para listar todos as saidas
def saidas_seleciona_todos():
    saidas = Saidas.query.all()
    saidas_json = [saida.to_json() for saida in saidas]
    return gera_response(200, "Saidas", saidas_json, "Saidas listadas com sucesso")

#Endpoint GET /saidas/<id> para lista apenas uma saidas
def saidas_seleciona_um(id):
    saidas = Saidas.query.filter_by(saida_id=id).first()
    saidas_json = saidas.to_json()
    return gera_response(200, "saidas", saidas_json, "saidas listadas com sucesso")

#Endpoint POST /saidas para incluir uma nova saida
def saidas_criar(body):
    try:
        saida = Saidas(
            saida_nome=body["saida_nome"],
            usuario_id=body["usuario_id"],
            saida_valor=body["saida_valor"],
            saida_data=body["saida_data"],
            mes_nome=body["mes_nome"],
            mes_ano=body["mes_ano"],
            conta_id=body["conta_id"]
        )
        db.session.add(saida)
        db.session.commit()
        return gera_response(201, "Saidas", saida.to_json(), "saida criada com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Saidas", {}, f"Erro ao Cadastrar saida:{e}")

#Endpoint PUT /saidas/<id> para atualizar uma saida
def saidas_atualiza(id, body):
    saidas = Saidas.query.filter_by(saida_id=id).first()
    try:
        if "saida_nome" in body:
            saidas.saida_nome = body["saida_nome"]
        if "usuario_id" in body:
            saidas.usuario_id = body["usuario_id"]
        if "saida_valor" in body:
            saidas.saida_valor = body["saida_valor"]
        if "conta_id" in body:
            saidas.conta_id = body["conta_id"]
        if "saida_data" in body:
            saidas.saida_data = body["saida_data"]

        db.session.add(saidas)
        db.session.commit()
        return gera_response(200, "saidas", saidas.to_json(), "saida atualizada com sucesso")
    except Exception as e:
        return gera_response(400, "saidas", {}, f"Erro ao Atualizar saida:{e}")

#Endpoint DELETE /saidas/<id> para deletar uma saida
def saidas_deleta(id):
    saidas = Saidas.query.filter_by(saida_id=id).first()
    try:
        db.session.delete(saidas)
        db.session.commit()
        return gera_response(200, "saidas", saidas.to_json(), "saida deletado com sucesso")
    except Exception as e:
        return gera_response(400, "saidas", {}, f"Erro ao deletar saida:{e}")

def saidas_filtro_mes_ano(mes, ano):
    try:
        saidas = Saidas.query.filter(Saidas.mes_ano==ano, Saidas.mes_nome==mes)
        saidas_json = [saida.to_json() for saida in saidas]
        return gera_response(200, "Saidas", saidas_json, "Saidas listadas com sucesso")
    except Exception as e:
        return gera_response(400, "Saidas", {}, f"Erro ao filtrar saidas:{e}")


##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
