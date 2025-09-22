from config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models import Usuarios
from werkzeug.security import check_password_hash

def login_usuario(f):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'usuario' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

