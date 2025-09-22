from flask import jsonify, request, session, render_template, redirect, url_for
from config import app, db, bcrypt
from models import Root
from backend.auth.usuarios_login import root_required

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
            session.pop('tipo', None)  # Remove tipo também
            return jsonify({'message': 'Logout feito com sucesso'}), 200
        else:
            return jsonify({'error': 'Nenhuma sessão ativa encontrada'}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno ao fazer logout'}), 500

