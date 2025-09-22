from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .seguranca import configurar_seguranca, obter_bcrypt, obter_limiter

# carregando as variáveis do .env
load_dotenv()

# extensões
db = SQLAlchemy()

# criação app
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# configs básicas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicialização básica
db.init_app(app)

# configuração de segurança (importada)
configurar_seguranca(app)

# acesso às extensões de segurança
bcrypt = obter_bcrypt()
limiter = obter_limiter()
