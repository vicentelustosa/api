from functools import wraps
from flask import request, abort
from app import db

def recurso_existe(modelo, param_id):
    @wraps(f)
    def wrapped(*args, **kwargs):
        print(f"param_id: {param_id} kwargs: {kwargs}")
        resource_id = kwargs.get(param_id)
        if resource_id is None:
            abort(400, f"Parâmetro '{param_id}' é obrigatório na URL.")
        resource = db.session.get(modelo, resource_id)
        if not resource:
            abort(404, f"Recurso não encontrado.")
        request.resource = resource
        return f(*args, **kwargs)
    return wrapped
