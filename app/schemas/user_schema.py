from .. import ma
from marshmallow import fields, validate
from ..models.user import User
from .message_schema import MessageSchema
from .comment_schema import CommentSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "nome", "email","senha", "messages")

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True, validate=validate.Length(min=1))
    email = ma.auto_field(required=True, validate=validate.Email())
    senha = ma.auto_field(load_only=True, required=True, validate=validate.Length(min=6))

   # Relacionamentos
    messages = fields.Nested(MessageSchema, many=True, dump_only=True)