from .. import ma
from marshmallow import validate
from ..models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True, validate=validate.Length(min=1))
    email = ma.auto_field(required=True, validate=validate.Email())
    senha = ma.auto_field(load_only=True, required=True, validate=validate.Length(min=6))
