from main import db
from flask import Response
import json

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Contas(db.Model):
    conta_id = db.Column(db.Integer, primary_key = True)
    conta_nome = db.Column(db.String(50), nullable=False)
    conta_limite = db.Column(db.Integer, nullable=False)
    conta_valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"conta_id": self.conta_id,
                "conta_nome": self.conta_nome,
                "conta_limite": self.conta_limite,
                "conta_valor": self.conta_valor,
                "usuario_id": self.usuario_id
                }

#Endpoint GET /contas para listar todos os contas
def contas_seleciona_todos():
    contas = Contas.query.all()
    contas_json = [conta.to_json() for conta in contas]
    return gera_response(200, "Contas", contas_json, "Contas Listadas Corretamente")

#Endpoint GET /contas/<id> para lista apenas um Contas
def contas_seleciona_um(id):
    contas = Contas.query.filter_by(conta_id=id).first()
    contas_json = contas.to_json()
    return gera_response(200, "contas", contas_json, "conta Listada Corretamente")


#Endpoint GET /contas/<id> para lista apenas um Contas
def contas_filtra_nome(nome):
    contas = Contas.query.filter_by(conta_nome=nome).first()
    contas_json = contas.to_json()
    return gera_response(200, "contas", contas_json, "conta Listada Corretamente")


#Endpoint POST /contas para incluir uma nova conta
def contas_criar(body):
    try:
        conta = Contas(
            conta_nome=body["conta_nome"],
            conta_limite=body["conta_limite"],
            conta_valor=body["conta_valor"],
            usuario_id=body["usuario_id"]
        )
        db.session.add(conta)
        db.session.commit()
        return gera_response(201, "conta", conta.to_json(), "conta criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "conta", {}, f"Erro ao Cadastrar conta:{e}")

#Endpoint PUT /contas/<id> para atualizar uma conta
def contas_atualiza(id, body):
    contas = Contas.query.filter_by(conta_id=id).first()
    try:
        if "conta" in body:
            contas.conta_nome = body["conta_nome"]
        if "conta_limite" in body:
            contas.conta_limite = body["conta_limite"]
        if "conta_valor" in body:
            contas.conta_valor = body["conta_valor"]
        if "conta_valor" in body:
            contas.usuario_id = body["usuario_id"]

        db.session.add(contas)
        db.session.commit()
        return gera_response(200, "contas", contas.to_json(), "conta atualizado com sucesso")
    except Exception as e:
        return gera_response(400, "contas", {}, f"Erro ao Atualizar conta:{e}")

#Endpoint DELETE /contas/<id> para deletar uma conta
def contas_deleta(id):
    contas = Contas.query.filter_by(dispositivo_id=id).first()
    try:
        db.session.delete(contas)
        db.session.commit()
        return gera_response(200, "contas", contas.to_json(), "conta deletado com sucesso")
    except Exception as e:
        return gera_response(400, "contas", {}, f"Erro ao deletar conta:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")