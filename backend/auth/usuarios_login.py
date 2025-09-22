from config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models import Usuarios
from werkzeug.security import check_password_hash
from validadores import validar_cpf

def login_usuario(f):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'usuario' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login/usuarios', methods=['POST'])
def login_usuarios():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    if not validar_cpf(senha):
        return jsonify({'sucesss': False, 'aviso': 'CPF inválido'}), 400

    usuarios = Usuarios.query.filter_by(nome=nome).first()
    if usuarios and bcrypt.check_password_hash(usuarios.senha, senha):
        session['cpf'] = usuarios.cpf
        session['tipo'] = 'usuarios'
        return jsonify({'success': True, 'aviso': 'Login feito com sucesso'}), 200
    else:
        return jsonify({'success': False, 'aviso': 'Login ou senha inválidos'}), 401

@app.route('/logout')
@login_usuario
def logout_usuario():
    if 'cpf' in session:
        session.pop('cpf', None)
        return jsonify({'aviso': 'Logout feito com sucesso'}), 200
    else:
        return jsonify({'aviso': 'Erro interno ao fazer logout'}), 500

