# Imports utilizados são:
# URI do banco de dados
# Response da biblioteca Flask para trabalhar com os erros gerados ao consumir as APIs
# Json para a transformação e leitura de parametros em formato JSON
from main import db
from flask import Response
import json

# Principal CLASS que faz a construção da tabela Contas no banco de dados
# E também conta com uma função nomeada TO_JSON que transporma o payload das APIs em JSON para a inclusão correta no banco
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

####### Inicio das funções que são chamadas pelos Endpoints ########

# Endpoint GET que retorna todas as contas dentro do banco
def contas_seleciona_todos():
    try:
        contas = Contas.query.all()
        contas_json = [conta.to_json() for conta in contas]
        return gera_response(200, "Contas", contas_json, "Contas listadas com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Ouve um erro ao listar as contas! Mensagem: {e}")

# Endpoint GET que retorna apenas uma conta dentro do banco
# Sendo filtrada pelo ID
def contas_seleciona_um(id):
    try:
        contas = Contas.query.filter_by(conta_id=id).first()
        contas_json = contas.to_json()
        return gera_response(200, "Contas", contas_json, "Conta listada com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Ouve um erro ao listar a conta! Mensagem: {e}")

# Endpoint GET que retorna uma conta dentro do banco
# Sendo filtrada pelo NOME
def contas_filtra_nome(nome):
    try:
        contas = Contas.query.filter_by(conta_nome=nome).first()
        contas_json = contas.to_json()
        return gera_response(200, "Contas", contas_json, "Conta listada com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Ouve um erro ao listar a conta! Mensagem: {e}")

# Endpoint POST que realiza o cadastro de uma nova conta dentro do banco
# Sendo necessário informar o body correto para que a construção seja realizada com sucesso
def contas_criar(body):
    try:
        conta = Contas(
            conta_nome=body["conta_nome"],
            conta_limite=body["conta_limite"],
            conta_valor=0,
            usuario_id=body["usuario_id"]
        )
        #Validação dos campos
        if conta.conta_nome == None or conta.conta_nome == "":
            return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O nome da conta não foi informado")
        if conta.conta_limite == None:
            return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O limite da conta não foi informado")
        if conta.usuario_id == None:
            return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O ID do usuario da conta não foi informado")

        db.session.add(conta)
        db.session.commit()
        return gera_response(201, "Contas", conta.to_json(), "Conta criado com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Erro ao Cadastrar conta! Mensagem:{e}")

# Endpoint PUT que atualiza uma conta criada dentro do banco
# Sendo necessário informar um body com pelo menos uma opção
def contas_atualiza(id, body):
    contas = Contas.query.filter_by(conta_id=id).first()
    try:
        if "conta_nome" in body:
            contas.conta_nome = body["conta_nome"]   
        if "conta_limite" in body:
            contas.conta_limite = body["conta_limite"]   
        if "usuario_id" in body:
            contas.usuario_id = body["usuario_id"]

        if contas.conta_nome == None or contas.conta_nome == "":
                return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O nome da conta não foi informado") 
        if contas.conta_limite == None:
                return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O limite da conta não foi informado") 
        if contas.usuario_id == None:
                return gera_response(400, "Contas", {}, f"Erro ao cadastrar conta! Mensagem: O ID do usuario da conta não foi informado")

        db.session.add(contas)
        db.session.commit()
        return gera_response(200, "Contas", contas.to_json(), "Conta atualizada com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Erro ao atualizar conta! Mensagem:{e}")

# Endpoint DELETE que deleta uma conta criada dentro do banco
# Sendo necessário informar apenas um ID para que ela seja deletada
def contas_deleta(id):
    contas = Contas.query.filter_by(conta_id=id).first()
    try:
        db.session.delete(contas)
        db.session.commit()
        return gera_response(200, "Contas", contas.to_json(), "Conta deletada com sucesso!")
    except Exception as e:
        return gera_response(400, "Contas", {}, f"Erro ao deletar conta! Mensagem:{e}")

######## Fim das funções chamadas pelos endpoints ###########

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")