from main import db
from flask import Response
import json

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Usuarios(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(50), nullable=False)
    conta_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"usuario_id": self.usuario_id,
                "usuario_nome": self.usuario_nome,
                "conta_id": self.conta_id
                }

#Endpoint GET /usuarios para listar todos os usuarios
def usuarios_seleciona_todos():
    usuarios = Usuarios.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios]
    return gera_response(200, "Usuarios", usuarios_json, "Usuarios Listados Corretamente")

#Endpoint GET /usuarios/<id> para lista apenas um usuario
def usuarios_seleciona_um(id):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    usuarios_json = usuarios.to_json()
    return gera_response(200, "Usuarios", usuarios_json, "usuario Listado Corretamente")

#Endpoint GET /usuarios/<id> para lista apenas um usuario
def usuarios_filtra_nome(nome):
    usuarios = Usuarios.query.filter_by(usuario_nome=nome).first()
    usuarios_json = usuarios.to_json()
    return gera_response(200, "Usuarios", usuarios_json, "usuario Listado Corretamente")

#Endpoint POST /usuarios para incluir um novo usuario
def usuarios_criar(body):
    try:
        usuario = Usuarios(
            usuario_nome=body["usuario_nome"],
            conta_id=body["conta_id"]
        )
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "Usuarios", usuario.to_json(), "Usuario criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Usuarios", {}, f"Erro ao Cadastrar usuario:{e}")

#Endpoint PUT /usuarios/<id> para atualizar um usuario
def usuarios_atualiza(id, body):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    try:
        if "usuario_nome" in body:
            usuarios.usuario_nome = body["usuario_nome"]
        if "conta_id" in body:
            usuarios.conta_id = body["conta_id"]

        db.session.add(usuarios)
        db.session.commit()
        return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario atualizado com sucesso")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao Atualizar usuario:{e}")

#Endpoint DELETE /usuarios/<id> para deletar um dispositivo
def usuarios_deleta(id):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    try:
        db.session.delete(usuarios)
        db.session.commit()
        return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario deletado com sucesso")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao deletar Usuario:{e}")




##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")