from config import app, db
from backend.auth.usuarios_login import login_usuario
from flask import render_template, jsonify

@app.route('/')
def tela_login():
    return render_template('login.html')

@app.route('/home')
@login_usuario
def home():
    if not login_usuario:
        return jsonify({'aviso': 'Usuário não autenticado'}), 401
    return render_template('home.html')