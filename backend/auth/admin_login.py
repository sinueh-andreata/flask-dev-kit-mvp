from core.config import app, db, bcrypt
from flask import render_template, request, jsonify, session
from models.models import Admin
from werkzeug.security import check_password_hash

def login_admin_required(f):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != 'admin' or 'cpf' not in session:
            return jsonify({'aviso': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        
        admin = Admin.query.filter_by(nome=nome).first()
        if admin and bcrypt.check_password_hash(admin.senha, senha):
            session['cpf'] = admin.cpf
            session['tipo'] = 'admin'
            return jsonify({'aviso': 'Login feito com sucesso'}), 200
        else:
            return jsonify({'aviso': 'Login ou senha inválidos'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_admin_required
def logout_admin():
    if 'cpf' in session:
        session.pop('cpf', None)
        return jsonify({'aviso': 'Logout feito com sucesso'}), 200
    else:
        return jsonify({'aviso': 'Erro interno ao fazer logout'}), 500
