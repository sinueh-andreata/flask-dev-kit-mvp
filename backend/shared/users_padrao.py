from models.models import Root, Usuarios, Admin
from core.config import db, bcrypt, app
from flask import jsonify

def criar_users_padrao():

    criar_root_padrao()
    
    criar_usuario_padrao()
    
    criar_admin_padrao()

def criar_root_padrao():
    try:
        if not Root.query.first():
            senha_hash = bcrypt.generate_password_hash('root123').decode('utf-8')
            root = Root(nome='root', cpf='00000000000', senha=senha_hash)
            db.session.add(root)
            db.session.commit()
            return True
        else:
            return jsonify({'message': 'Usuário root já existe no banco de dados'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar usuário root: ' + str(e)}), 500

def criar_usuario_padrao():
    try:
        if not Usuarios.query.first():
            senha_hash = bcrypt.generate_password_hash('user123').decode('utf-8')
            usuario = Usuarios(nome='user', cpf='11111111111', senha=senha_hash)
            db.session.add(usuario)
            db.session.commit()
            return True
        else:
            return jsonify({'message': 'Usuário padrão já existe no banco de dados'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar usuário padrão: ' + str(e)}), 500
    
def criar_admin_padrao():
    try:
        if not Admin.query.first():
            senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = Admin(nome='admin', cpf='22222222222', senha=senha_hash)
            db.session.add(admin)
            db.session.commit()

            return True
        else:
            return jsonify({'message': 'Usuário admin já existe no banco de dados'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar usuário admin: ' + str(e)}), 500