from werkzeug.security import generate_password_hash
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(240), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    posts = db.relationship("PostModel", cascade="all, delete-orphan")
    comments = db.relationship("CommentModel", cascade="all, delete-orphan")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
