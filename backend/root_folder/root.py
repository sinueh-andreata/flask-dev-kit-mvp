from flask import jsonify, request, session, render_template, redirect, url_for
from core.config import app, db, bcrypt
from models.models import Root
from auth.root_login import root_required

@app.route('/root/dashboard')
@root_required
def root_dashboard():
    return jsonify({
        'mensagem': 'Dashboard do Root',
        'usuario': session.get('nome', 'Root'),
        'tipo': session.get('tipo'),
        'cpf': session.get('cpf')
    }), 200

