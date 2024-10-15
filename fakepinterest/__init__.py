from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os  # Importando a biblioteca os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///comunidade.db")  # Configuração do banco de dados
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "821c366a2b3fee7fcce6dd2a2f0eb185")  # Chave secreta para sessões
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)  # Instância do banco de dados
bcrypt = Bcrypt(app)  # Instância do Bcrypt para hashing de senhas
login_manager = LoginManager(app)  # Instância do LoginManager para autenticação
login_manager.login_view = "homepage"  # Define a rota de login

from . import routes  # Importar rotas após a definição do app e database
