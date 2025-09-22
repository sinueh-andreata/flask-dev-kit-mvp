from flask import jsonify, request, session, render_template, redirect, url_for
from config import app, db, bcrypt
from models import Root
from login import root_required

@app.route('/login/root', methods=['GET', 'POST'])
def root_required():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        
        root = Root.query.filter_by(nome=nome).first()
        if root and bcrypt.check_password_hash(root.senha, senha):
            session['cpf'] = root.cpf
            session['tipo'] = 'root'
            return jsonify({'aviso': 'Login feito com sucesso'}), 200
        else:
            return jsonify({'aviso': 'Login ou senha inválidos'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@root_required
def logout_root():
    if 'cpf' in session:
        session.pop('cpf', None)
        return jsonify({'aviso': 'Logout feito com sucesso'}), 200
    else:
        return jsonify({'aviso': 'Erro interno ao fazer logout'}), 500
