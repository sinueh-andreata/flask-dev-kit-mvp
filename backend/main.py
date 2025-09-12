from flask import Flask
from config import app, db

# importação das tabelas do banco de dados
from models import *

# importação das rotas/endpoints/APIs
from usuario import *
from admin import *
from rotas_html import *


with app.app_context():
     db.create_all()
if __name__ == '__main__':
    app.run(debug=True)