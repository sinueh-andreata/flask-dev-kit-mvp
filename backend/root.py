from flask import jsonify, request, session, render_template, redirect, url_for
from config import app, db, bcrypt
from models import Root
from login import root_required

@app.route('/login/root', methods=['GET', 'POST'])
def login_root():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            senha = request.form.get('senha')
            
            if not nome or not senha:
                return jsonify({'error': 'Nome e senha são obrigatórios'}), 400
            
            root = Root.query.filter_by(nome=nome).first()
            if root and bcrypt.check_password_hash(root.senha, senha):
                session['cpf'] = root.cpf
                session['tipo'] = 'root'
                return jsonify({'message': 'Login feito com sucesso'}), 200
            else:
                return jsonify({'error': 'Login ou senha inválidos'}), 401
        except Exception as e:
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return render_template('login.html')

@app.route('/logout/root')
@root_required
def logout_root():
    try:
        if 'cpf' in session:
            session.pop('cpf', None)
            session.pop('tipo', None)  # Remove tipo também
            return jsonify({'message': 'Logout feito com sucesso'}), 200
        else:
            return jsonify({'error': 'Nenhuma sessão ativa encontrada'}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno ao fazer logout'}), 500

def criar_root_padrao():
    """Cria usuário root padrão se não existir"""
    try:
        if not Root.query.first():
            senha_hash = bcrypt.generate_password_hash('root123').decode('utf-8')
            root = Root(nome='root', cpf='00000000000', senha=senha_hash)  # CPF válido para testes
            db.session.add(root)
            db.session.commit()
            print("✅ Usuário root padrão criado:")
            print("   Nome: root")
            print("   CPF: 00000000000") 
            print("   Senha: root123")
            print("⚠️  ALTERE A SENHA APÓS O PRIMEIRO LOGIN!")
            return True
        else:
            print("ℹ️  Usuário root já existe no banco de dados")
            return False
    except Exception as e:
        print(f"❌ Erro ao criar usuário root: {str(e)}")
        db.session.rollback()
        return False