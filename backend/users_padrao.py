from models import Root, Usuarios, Admin
from config import db, bcrypt, app
from flask import jsonify

def criar_users_padrao():
    def criar_root_padrao():
        try:
            if not Root.query.first():
                senha_hash = bcrypt.generate_password_hash('root123').decode('utf-8')
                root = Root(nome='root', cpf='00000000000', senha=senha_hash)  # CPF válido para testes
                db.session.add(root)
                db.session.commit()
                jsonify("✅ Usuário root padrão criado:")
                jsonify("   Nome: root")
                jsonify("   CPF: 00000000000") 
                jsonify("   Senha: root123")
                jsonify("⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
                return True
            else:
                jsonify("ℹ️  Usuário root já existe no banco de dados")
                return False
        except Exception as e:
            jsonify(f"❌ Erro ao criar usuário root: {str(e)}")
            db.session.rollback()
            return False
        
    def criar_usuario_padrao():
        try:
            if not Usuarios.query.first():
                senha_hash = bcrypt.generate_password_hash('user123').decode('utf-8')
                usuario = Usuarios(nome='user', cpf='11111111111', senha=senha_hash)  # CPF válido para testes
                db.session.add(usuario)
                db.session.commit()
                jsonify("✅ Usuário padrão criado:")
                jsonify("   Nome: usuario")
                jsonify("   CPF: 11122233344") 
                jsonify("   Senha: user123")
                jsonify("⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
                return True
            else:
                jsonify("ℹ️  Usuário padrão já existe no banco de dados")
                return False
        except Exception as e:
            jsonify(f"❌ Erro ao criar usuário padrão: {str(e)}")
            db.session.rollback()
            return False
        
    def criar_admin_padrao():
        try:
            if not Admin.query.first():
                senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
                admin = Admin(nome='admin', cpf='22222222222', senha=senha_hash)
                db.session.add(admin)
                db.session.commit()
                jsonify("✅ Usuário admin padrão criado:")
                jsonify("   Nome: admin")
                jsonify("   CPF: 222.222.222-22") 
                jsonify("   Senha: admin123")
                jsonify("⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
                return True
            else:
                jsonify("ℹ️  Usuário admin já existe no banco de dados")
                return False
        except Exception as e:
            jsonify(f"❌ Erro ao criar usuário admin: {str(e)}")
            db.session.rollback()
            return False