from flask import Flask
from config import app, db

# importação das tabelas do banco de dados
from models import *

# importação das rotas/endpoints/APIs
from usuario import *
from admin import *
from rotas_html import *
from root import *
from users_padrao import criar_users_padrao

with app.app_context():
     db.create_all()
     criar_users_padrao()
if __name__ == '__main__':
    app.run(debug=True)