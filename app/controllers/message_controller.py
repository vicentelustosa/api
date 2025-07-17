from flask import abort
from ..models.message import Message
from .. import db

def listar_mensagens():
    return Message.query.all()

def obter_mensagem_por_id(message_id):
    # Por simplicidade, usamos get_or_404 neste projeto.
    return Message.query.get_or_404(message_id)

def criar_mensagem(data):
    nova_mensagem = Message(**data)
    db.session.add(nova_mensagem)
    db.session.commit()
    return nova_mensagem

def atualizar_mensagem(message, data):
    for key, value in data.items():
        setattr(message, key, value)
    db.session.commit()
    return message

def deletar_mensagem(message):
    db.session.delete(message)
    db.session.commit()