from core.config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models.models import Usuarios
from werkzeug.security import check_password_hash
from shared.validadores import validar_cpf
from functools import wraps

@app.route('/login', methods=['GET'])
@app.route('/', methods=['GET'])
def login_page():
    """Rota principal de login"""
    return render_template('login.html')

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
            senha = request.form.get('senha')
            
            if not cpf or not senha:
                return jsonify({'success': False, 'message': 'CPF e senha são obrigatórios'}), 400
            
            # Validar CPF
            if not validar_cpf(cpf):
                return jsonify({'success': False, 'message': 'CPF inválido'}), 400
            
            # Limpar CPF (remover pontos e hífen)
            cpf_limpo = cpf.replace('.', '').replace('-', '')
            
            usuario = Usuarios.query.filter_by(cpf=cpf_limpo).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, senha):
                session['cpf'] = usuario.cpf
                session['tipo'] = 'usuario'
                session['nome'] = usuario.nome
                return jsonify({'success': True, 'message': 'Login feito com sucesso'}), 200
            else:
                return jsonify({'success': False, 'message': 'CPF ou senha inválidos'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500
    
    return render_template('login.html')

@app.route('/logout/usuarios')
@login_usuario
def logout_usuarios():
    try:
        if 'cpf' in session:
            session.pop('cpf', None)
            session.pop('tipo', None)
            session.pop('nome', None)
            return jsonify({'success': True, 'message': 'Logout feito com sucesso'}), 200
        else:
            return jsonify({'success': False, 'message': 'Nenhuma sessão ativa encontrada'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno ao fazer logout'}), 500