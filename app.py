from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

# Criação da instância da aplicação
app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeiro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criação do objeto db
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#rota do front
@app.route('/')
def index():
    return render_template('index.html')

# Modelo do Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
# Definição do modelo Transacao
class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'receita' ou 'despesa'
    descricao = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref='transacoes')

    def __repr__(self):
        return f'<Transacao {self.valor} - {self.tipo}>'

# Criando o banco de dados (se necessário)
with app.app_context():
    db.create_all()

# Rota para registrar uma transação
@app.route('/registrar_transacao', methods=['POST'])
def registrar_transacao():
    data = request.get_json()
    novo_registro = Transacao(
        valor=data['valor'],
        data=datetime.strptime(data['data'], '%Y-%m-%d'),
        categoria=data['categoria'],
        tipo=data['tipo'],
        descricao=data['descricao'],
        usuario_id=data['usuario_id']
    )
    db.session.add(novo_registro)
    db.session.commit()
    return jsonify({'message': 'Transação registrada com sucesso!'}), 201

# Rota para exibir o saldo
@app.route('/saldo', methods=['GET'])
def obter_saldo():
    usuario_id = request.args.get('usuario_id')
    receitas = Transacao.query.filter_by(usuario_id=usuario_id, tipo='receita').all()
    despesas = Transacao.query.filter_by(usuario_id=usuario_id, tipo='despesa').all()

    saldo = sum([t.valor for t in receitas]) - sum([t.valor for t in despesas])

    return jsonify({'saldo': saldo})

# Rota para iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
