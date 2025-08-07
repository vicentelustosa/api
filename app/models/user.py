from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)  # Tratamento seguro no capítulo de autenticação

    # Relacionamentos reversos
    messages = db.relationship("Message", backref="autor", lazy=True)
    comments = db.relationship("Comment", backref="autor", lazy=True)