from core.config import app, db
from auth.usuarios_login import login_usuario
from flask import render_template, jsonify

@app.route('/')
def tela_login():
    return render_template('user_login.html')

@app.route('/user_login.html')
def user_login_html():
     return render_template('user_login.html')

@app.route('/admin_login.html')
def admin_login_html():
     return render_template('admin_login.html')

@app.route('/root_login.html')
def root_login_html():
     return render_template('root_login.html')