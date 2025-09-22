from core.config import app, db, bcrypt
from flask import render_template, request, jsonify, session, redirect, url_for
from models.models import Usuarios
from werkzeug.security import check_password_hash
from shared.validadores import validar_cpf
from functools import wraps

@app.route('/login', methods=['GET'])
@app.route('/', methods=['GET'])
def login_page():
    """Rota principal de login"""
    return render_template('user_login.html')

def login_usuario(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'usuario' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    return wrapper

@app.route('/login/usuarios', methods=['GET', 'POST'])
def login_usuarios():
    if request.method == 'POST':
        try:
            cpf = request.form.get('cpf')
            nome = request.form.get('nome')
            senha = request.form.get('senha')

            if not senha or (not cpf and not nome):
                return jsonify({'success': False, 'message': 'Informe CPF ou nome e a senha'}), 400

            usuario = None
            if cpf:
                if not validar_cpf(cpf):
                    return jsonify({'success': False, 'message': 'CPF inválido'}), 400
                cpf_limpo = cpf.replace('.', '').replace('-', '')
                usuario = Usuarios.query.filter_by(cpf=cpf_limpo).first()
            elif nome:
                usuario = Usuarios.query.filter_by(nome=nome).first()

            if usuario and bcrypt.check_password_hash(usuario.senha, senha):
                session['cpf'] = usuario.cpf
                session['tipo'] = 'usuario'
                session['nome'] = usuario.nome
                return jsonify({'success': True, 'message': 'Login feito com sucesso'}), 200
            else:
                return jsonify({'success': False, 'message': 'Usuário ou senha inválidos'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

    return render_template('user_login.html')

@app.route('/logout/usuarios', methods=['POST'])
@login_usuario
def logout_usuarios():
    try:
        if 'cpf' in session:
            session.pop('cpf', None)
            session.pop('tipo', None)
            session.pop('nome', None)
            return redirect(url_for('login_page'))
        else:
            return redirect(url_for('login_page'))
    except Exception as e:
        return redirect(url_for('login_page'))
    

@app.route('/user_dashboard.html')
@login_usuario
def user_dashboard_html():
    return render_template('user_dashboard.html')