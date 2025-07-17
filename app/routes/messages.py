from flask import Blueprint, request
from ..schemas.message_schema import MessageSchema
from ..controllers import message_controller as controller

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = controller.listar_mensagens()
    return messages_schema.jsonify(messages), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = controller.obter_mensagem_por_id(message_id)
    return message_schema.jsonify(message), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = message_schema.load(request.get_json())
    message = controller.criar_mensagem(data)
    return message_schema.jsonify(message), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = controller.obter_mensagem_por_id(message_id)
    data = message_schema.load(request.get_json())
    message = controller.atualizar_mensagem(message, data)
    return message_schema.jsonify(message), 200
    
@messages_bp.route('/<int:message_id>', methods=['PATCH'])
def partial_update_message(message_id):
    message = controller.obter_mensagem_por_id(message_id)
    data = message_schema.load(request.get_json(), partial=True)
    message = controller.atualizar_mensagem(message, data)
    return message_schema.jsonify(message), 200
    
@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = controller.obter_mensagem_por_id(message_id)
    controller.deletar_mensagem(message)
    return '', 204