from flask import jsonify, request
from config import app, db, bcrypt, limiter
from backend.auth.usuarios_login import login_admin_required
from validadores import validar_cpf, validar_senha, validar_nome
from models import Usuarios

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
    

@app.route('/usuarios', methods=['GET'])
@login_admin_required
def listar_usuarios():
    try:
        usuarios = Usuarios.query.all()
        lista_usuarios = [usuario.json().json for usuario in usuarios]
        return jsonify(lista_usuarios), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao listar usuários'}), 500
    

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
@login_admin_required
def obter_usuario(usuario_id):
    try:
        usuario = Usuarios.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return usuario.json(), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao obter usuário'}), 500
    

@app.route('/usuario/<int:usuario_id>', methods=['PUT'])
@login_admin_required
def alterar_usuario(usuario_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON inválido ou vazio'}), 400
        
        usuario = Usuarios.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        nome = data.get('nome')
        cpf = data.get('cpf')
        senha = data.get('senha')

        if nome:
            validacao_nome = validar_nome(nome)
            if validacao_nome != True:
                return validacao_nome
            usuario.nome = nome
        
        if cpf:
            validacao_cpf = validar_cpf(cpf)
            if validacao_cpf != True:
                return validacao_cpf
            if Usuarios.query.filter(Usuarios.cpf == cpf, Usuarios.usuario_id != usuario_id).first():
                return jsonify({'error': 'Outro usuário com este CPF já existe'}), 409
            usuario.cpf = cpf
        
        if senha:
            validacao_senha = validar_senha(senha)
            if validacao_senha != True:
                return validacao_senha
            usuario.senha = bcrypt.generate_password_hash(senha).decode('utf-8')
        
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso', 'usuario': usuario.json().json}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar usuário'}), 500    
    

@app.route('/usuario/<int:usuario_id>', methods=['DELETE'])
@login_admin_required
def delete_usuario(usuario_id):
    try:
        usuario = Usuarios.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar usuário'}), 500