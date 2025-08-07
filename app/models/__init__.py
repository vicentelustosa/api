from app import db
from .user import User
from .message import Message
from .comment import Comment

# Definir os relacionamentos após as importações para garantir que as classes existam
'''


User.messages = db.relationship(
    "Message", back_populates="user", cascade="all, delete-orphan"
)

User.comments = db.relationship(
    "Comment", back_populates="user", cascade="all, delete-orphan"
)

Message.user = db.relationship(
    "User", back_populates="messages"
)

Message.comments = db.relationship(
    "Comment", back_populates="message", cascade="all, delete-orphan"
)

Comment.user = db.relationship(
    "User", back_populates="comments"
)

Comment.message = db.relationship(
    "Message", back_populates="comments"
)
'''