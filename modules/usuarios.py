# Imports de bibliotecas
from main import db
from flask import Response
import json

# Principal CLASS para consultas e criações no banco de dados dos usuários
# Juntamente com uma função TO_JSON que converte os campos em json
class Usuarios(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(50), nullable=False)
    conta_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"usuario_id": self.usuario_id,
                "usuario_nome": self.usuario_nome,
                "conta_id": self.conta_id
                }

# Endpoint GET que lista todos os usuários dentro do banco de dados
def usuarios_seleciona_todos():
    try:
        usuarios = Usuarios.query.all()
        usuarios_json = [usuario.to_json() for usuario in usuarios]
        return gera_response(200, "Usuarios", usuarios_json, "Usuarios listados com sucesso!")
    except Exception as e:
        return gera_response(200, "Usuarios", usuarios_json, f"Falha ao listar usuários! Mensagem: {e}")

# Endpoint GET para listar apenas um usuário do banco
# Filtrando pelo ID do usuário
def usuarios_seleciona_um(id):
    try:
        usuarios = Usuarios.query.filter_by(usuario_id=id).first()
        usuarios_json = usuarios.to_json()
        return gera_response(200, "Usuarios", usuarios_json, "Usuario listado com sucesso!")
    except Exception as e:
        return gera_response(200, "Usuarios", usuarios_json, f"Falha ao listar usuário! Mensagem: {e}")

# Endpoint GET para listar apenas um usuário do banco
# Filtrando pelo NOME
def usuarios_filtra_nome(nome):
    try:
        usuarios = Usuarios.query.filter_by(usuario_nome=nome).first()
        usuarios_json = usuarios.to_json()
        return gera_response(200, "Usuarios", usuarios_json, "Usuario listado com sucesso!")
    except Exception as e:
        return gera_response(200, "Usuarios", usuarios_json, f"Falha ao listar usuário! Mensagem: {e}")

# Endpoint GET que realiza a criação de novos usuários
# É necessáro informar um body correto para que seja possível criar o usuário no banco
def usuarios_criar(body):
    try:
        usuario = Usuarios(
            usuario_nome=body["usuario_nome"],
            conta_id=1
        )

        if usuario.usuario_nome == None or usuario.usuario_nome == "":
            return gera_response(200, "Usuarios", {}, f"Falha ao criar usuário! Mensagem: O nome do usuário deve ser informado")

        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "Usuarios", usuario.to_json(), "Usuario criado com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "Usuarios", {}, f"Falha ao criar usuário! Mensagem:{e}")

# Endpoint PUT que realiza alterações em usuários já criados no banco de dados
# Filtrando pelo ID de usuário
def usuarios_atualiza(id, body):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    try:
        if "usuario_nome" in body:
            usuarios.usuario_nome = body["usuario_nome"]

        if usuarios.usuario_nome == None or usuarios.usuario_nome == "":
            return gera_response(200, "Usuarios", {}, f"Falha ao criar usuário! Mensagem: O nome do usuário deve ser informado")

        db.session.add(usuarios)
        db.session.commit()
        return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario atualizado com sucesso!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao atualizar usuario! Mensagem:{e}")

# Endpoint DELETE que realiza a remoção de usuários no banco de dados
# Deve ser informado o ID do usuário para que funcione corretamente
def usuarios_deleta(id):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    try:
        db.session.delete(usuarios)
        db.session.commit()
        return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao deletar usuario! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")