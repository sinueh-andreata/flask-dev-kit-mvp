from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# carregando as variáveis do .env
load_dotenv()

# extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)

# criação app
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# configs
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # mudar para True em produção
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# inicialização do app
db.init_app(app)
bcrypt.init_app(app)
limiter.init_app(app)
CORS(app, origins=('http://localhost:3000', 'http://localhost:5000'), supports_credentials=True)
