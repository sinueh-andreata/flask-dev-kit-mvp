from flask import jsonify, request
from config import app, db, bcrypt, limiter
from backend.auth.usuarios_login import login_admin_required
from validadores import validar_cpf, validar_senha, validar_nome

@app.route('/criar/usuario', methods=['POST'])
@login_admin_required
def criar_usuario():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON inválido ou vazio'}), 400
            
        nome = data.get('nome')
        cpf = data.get('cpf')
        senha = data.get('senha')

        if not nome or not cpf or not senha:
            return jsonify({'error': 'Nome, CPF e senha são obrigatórios'}), 400

        validacao_nome = validar_nome(nome)
        if validacao_nome != True:
            return validacao_nome
        
        validacao_cpf = validar_cpf(cpf)
        if validacao_cpf != True:
            return validacao_cpf
        
        validacao_senha = validar_senha(senha)
        if validacao_senha != True:
            return validacao_senha

        from models import Usuarios 

        if Usuarios.query.filter_by(cpf=cpf).first():
            return jsonify({'error': 'Usuário com este CPF já existe'}), 409

        senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

        novo_usuario = Usuarios(nome=nome, cpf=cpf, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({
            'message': 'Usuário criado com sucesso',
            'usuario': {
                'id': novo_usuario.id,
                'nome': novo_usuario.nome,
                'cpf': novo_usuario.cpf
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500