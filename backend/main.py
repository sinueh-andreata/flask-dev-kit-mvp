from flask import Flask
from core.config import app, db

# importação das tabelas do banco de dados
from models.models import *

# importação das rotas/endpoints/APIs
from auth.usuarios_login import *
from user_folder.usuario import *
from admin_folder.admin import *
from rotas_html import *
from root_folder.root import *
from shared.users_padrao import criar_users_padrao

with app.app_context():
     db.create_all()
     criar_users_padrao()
if __name__ == '__main__':
    app.run(debug=True)