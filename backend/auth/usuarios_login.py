from core.config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models.models import Usuarios
from werkzeug.security import check_password_hash
from shared.validadores import validar_cpf
from functools import wraps

def login_usuario(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'usuario' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    return wrapper

def login_admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'admin' or 'cpf' not in session:
            return jsonify({'aviso': 'Admin não autenticado'}), 401
        return f(*args, **kwargs)
    return wrapper

def root_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'root' or 'cpf' not in session:
            return jsonify({'aviso': 'Root não autenticado'}), 401
        return f(*args, **kwargs)
    return wrapper

