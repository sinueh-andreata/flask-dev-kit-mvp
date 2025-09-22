from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt
from models.models import Usuarios
from auth.usuarios_login import login_usuario
from shared.validadores import validar_cpf

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

