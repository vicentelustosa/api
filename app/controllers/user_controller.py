from ..models.user import User
from .. import db

def listar_usuarios():
    return User.query.all()

def obter_usuario(user_id):
    return User.query.get(user_id)  # Retorna None se não encontrado

def criar_usuario(dados):
    novo = User(**dados)
    db.session.add(novo)
    db.session.commit()
    return novo

def atualizar_usuario(user, dados):
    for chave, valor in dados.items():
        setattr(user, chave, valor)
    db.session.commit()
    return user

def deletar_usuario(user):
    db.session.delete(user)
    db.session.commit()
