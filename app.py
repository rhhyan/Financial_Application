from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Criando a instância do Flask
app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Usando SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Definindo os modelos
class DespesaReceita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<DespesaReceita {self.id} - {self.descricao}>'

# Criando o banco de dados e tabelas
with app.app_context():
    db.create_all()

# Rota para a página inicial
@app.route('/')
def index():
    despesas_receitas = DespesaReceita.query.all()  # Obtém todas as despesas e receitas
    return render_template('index.html', despesas_receitas=despesas_receitas)

# Rota para adicionar uma nova despesa ou receita
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        categoria = request.form['categoria']
        tipo = request.form['tipo']
        usuario_id = request.form['usuario_id']
        
        nova_despesa_receita = DespesaReceita(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            tipo=tipo,
            usuario_id=usuario_id
        )
        
        db.session.add(nova_despesa_receita)
        db.session.commit()
        
        return redirect(url_for('index'))  # Redireciona de volta para a página inicial

    return render_template('add.html')  # Página para adicionar uma nova despesa ou receita

# Rota para editar uma despesa ou receita
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    despesa_receita = DespesaReceita.query.get_or_404(id)  # Obtém o item pelo ID
    
    if request.method == 'POST':
        despesa_receita.descricao = request.form['descricao']
        despesa_receita.valor = request.form['valor']
        despesa_receita.categoria = request.form['categoria']
        despesa_receita.tipo = request.form['tipo']
        despesa_receita.usuario_id = request.form['usuario_id']
        
        db.session.commit()  # Salva as mudanças no banco de dados
        
        return redirect(url_for('index'))  # Redireciona para a página inicial

    return render_template('edit.html', despesa_receita=despesa_receita)

# Rota para excluir uma despesa ou receita
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    despesa_receita = DespesaReceita.query.get_or_404(id)  # Obtém o item pelo ID
    db.session.delete(despesa_receita)  # Deleta o item
    db.session.commit()  # Salva a exclusão no banco de dados
    
    return redirect(url_for('index'))  # Redireciona para a página inicial

"""Rodando"""
if __name__ == "__main__":
    app.run(debug=True)
