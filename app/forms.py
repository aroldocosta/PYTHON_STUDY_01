from flask_wtf import FlaskForm                        
from wtforms import StringField, SubmitField, PasswordField            
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db, bcrypt
from app.models import Contato, User, Post

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar', validators=[DataRequired()])

    def validate_email(self, email):
        print(email.data)
        if User.query.filter(email==email.data).first():
            return ValidationError('Usuário já cadastrado com este email!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha=senha
        )

        db.session.add(user)
        db.session.commit()
        return user
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):

        # Recuperar usuario do email
        user = User.query.filter_by(email=self.email.data).first()
        
        # Verificar se a senha é valida 
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                # Retorna usuário
                return user
            else:
                raise Exception('Senha incorreta!!!')
                return NULL
        else:
            raise Exception('Usuário não encontrado!!!')
            return NULL

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar', validators=[DataRequired()])

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data,            
        )
        db.session.add(contato)
        db.session.commit()

class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id
        )

        db.session.add(post)
        db.session.commit()