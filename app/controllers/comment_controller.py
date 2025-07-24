from ..models.comment import Comment
from .. import db

def listar_comentarios(message_id):
    return Comment.query.filter_by(message_id=message_id).all()

def obter_comentario(comment_id):
    return Comment.query.get(comment_id)

def criar_comentario(dados):
    novo = Comment(**dados)
    db.session.add(novo)
    db.session.commit()
    return novo

def atualizar_comentario(comment, dados):
    for chave, valor in dados.items():
        setattr(comment, chave, valor)
    db.session.commit()
    return comment

def deletar_comentario(comment):
    db.session.delete(comment)
    db.session.commit()