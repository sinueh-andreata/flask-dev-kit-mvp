from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt, limiter
from models.models import Usuarios
from auth.usuarios_login import login_usuario
from shared.validadores import validar_cpf

@app.route('/usuario/dashboard')
@limiter.limit("10 per minute")  # Máximo 10 requests por minuto
@login_usuario
def usuario_dashboard():
    return jsonify({'mensagem': "teste limiter"}), 200