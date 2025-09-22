from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt, limiter
from models.models import Usuarios
from auth.usuarios_login import login_usuario
from shared.validadores import validar_cpf

@app.route('/user_dashboard.html')
@login_usuario
def user_dashboard_html():
    return render_template('user_dashboard.html')