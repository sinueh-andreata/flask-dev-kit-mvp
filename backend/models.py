from flask import jsonify
from config import app, db
from sqlalchemy.dialects.mysql import MEDIUMBLOB
import datetime

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def json(self):
        return jsonify({
            'usuario_id': self.usuario_id,
            'nome': self.nome,
            'cpf': self.cpf,
            'senha': self.senha
        })
    

class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def json(self):
        return jsonify({
            'admin_id': self.admin_id,
            'nome': self.nome,
            'cpf': self.cpf,
            'senha': self.senha
        })


class Produto(db.Model):
    __tablename__ = 'produtos'

    produto_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    preco = db.Column(db.Integer, nullable=False)
    imagem = db.Column(MEDIUMBLOB, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def json(self):
        return jsonify({
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'data_criação': self.data_criacao
        })
    

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    pedido_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total = db.Column(db.Integer, nullable=False)

    def json(self):
        return jsonify({
            'pedido_id': self.pedido_id,
            'usuario_id': self.usuario_id,
            'data_pedido': self.data_pedido,
            'total': self.total
        })
    
