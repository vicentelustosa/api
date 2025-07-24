from flask import request, abort
from functools import wraps
from ..controllers import user_controller

def usuario_existe(f):
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        user = user_controller.obter_usuario(user_id)
        if user is None:
            abort(404, description="Usuário não encontrado.")
        request.usuario = user
        return f(user_id, *args, **kwargs)
    return decorated_function
