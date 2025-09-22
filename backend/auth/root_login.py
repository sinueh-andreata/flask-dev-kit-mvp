from core.config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models.models import Root
from werkzeug.security import check_password_hash

def root_required(f):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'root' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login/root', methods=['GET', 'POST'])
def login_root():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            senha = request.form.get('senha')
            
            if not nome or not senha:
                return jsonify({'error': 'Nome e senha são obrigatórios'}), 400
            
            root = Root.query.filter_by(nome=nome).first()
            if root and bcrypt.check_password_hash(root.senha, senha):
                session['cpf'] = root.cpf
                session['tipo'] = 'root'
                session['nome'] = root.nome
                return jsonify({'message': 'Login feito com sucesso'}), 200
            else:
                return jsonify({'error': 'Login ou senha inválidos'}), 401
        except Exception as e:
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return render_template('login.html')

@app.route('/logout/root')
@root_required
def logout_root():
    try:
        if 'cpf' in session:
            session.pop('cpf', None)
            session.pop('tipo', None) 
            return jsonify({'message': 'Logout feito com sucesso'}), 200
        else:
            return jsonify({'error': 'Nenhuma sessão ativa encontrada'}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno ao fazer logout'}), 500