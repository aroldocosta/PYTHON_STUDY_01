from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id);

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, id, active=True):
        self.id = id
        self.active = active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Contato(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True) 
    mensagem = db.Column(db.String, nullable=True)
    respondido = db.Column(db.Integer, default=0)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    mensagem = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    