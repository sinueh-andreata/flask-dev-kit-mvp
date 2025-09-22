from flask import Flask, jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt
from models.models import Admin
from auth.admin_login import login_admin_required

@app.route('/admin/dashboard')
@login_admin_required
def admin_dashboard():
    return jsonify({
        'mensagem': 'Dashboard do Administrador',
        'usuario': session.get('nome', 'Admin'),
        'tipo': session.get('tipo'),
        'cpf': session.get('cpf')
    }), 200
