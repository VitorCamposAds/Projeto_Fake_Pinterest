from . import database, login_manager  # Importando a instância do banco de dados e do LoginManager
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader  # Decorador para carregar o usuário
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  # Retorna o usuário pelo ID

class Usuario(database.Model, UserMixin):  # Classe para o modelo de usuário
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)  # Relacionamento com a classe Foto

class Foto(database.Model):  # Classe para o modelo de fotos
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))  # Data de criação
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)  # FK para usuário
