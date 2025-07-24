from flask import Blueprint, request
from ..schemas.user_schema import UserSchema
from ..controllers import user_controller
from ..middlewares.user_required import usuario_existe

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = user_controller.listar_usuarios()
    return users_schema.jsonify(usuarios), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@usuario_existe
def obter_usuario(user_id):
    return user_schema.jsonify(request.usuario), 200

@users_bp.route('/', methods=['POST'])
def criar_usuario():
    dados = user_schema.load(request.get_json())
    usuario = user_controller.criar_usuario(dados)
    return user_schema.jsonify(usuario), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
@usuario_existe
def atualizar_usuario(user_id):
    dados = user_schema.load(request.get_json())
    usuario_atualizado = user_controller.atualizar_usuario(request.usuario, dados)
    return user_schema.jsonify(usuario_atualizado), 200

@users_bp.route('/<int:user_id>', methods=['PATCH'])
@usuario_existe
def patch_usuario(user_id):
    dados = user_schema.load(request.get_json(), partial=True)
    usuario_atualizado = user_controller.atualizar_usuario(request.usuario, dados)
    return user_schema.jsonify(usuario_atualizado), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@usuario_existe
def deletar_usuario(user_id):
    user_controller.deletar_usuario(request.usuario)
    return '', 204
