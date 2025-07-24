from .. import ma
from marshmallow import fields, validate
from ..models.comment import Comment

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        fields = ("id", "content", "created_at", "message_id")

    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    created_at = fields.DateTime(dump_only=True)
    message_id = fields.Int(required=True, load_only=True)