from flask import render_template, request, redirect, url_for
from models import db, DespesaReceita

# Função para registrar as rotas
def register_routes(app):
    
    # Página inicial - Exibe as despesas/receitas
    @app.route('/')
    def home():
        despesas_receitas = DespesaReceita.query.all()
        return render_template('home.html', despesas_receitas=despesas_receitas)
    
    # Página para adicionar uma despesa/receita
    @app.route('/add_despesa', methods=['GET', 'POST'])
    def add_despesa():
        if request.method == 'POST':
            descricao = request.form['descricao']
            valor = request.form['valor']
            categoria = request.form['categoria']
            tipo = request.form['tipo']  # 'despesa' ou 'receita'
            usuario_id = request.form['usuario_id']
            
            # Criando um novo objeto DespesaReceita
            nova_despesa = DespesaReceita(descricao=descricao, valor=valor, categoria=categoria, tipo=tipo, usuario_id=usuario_id)
            db.session.add(nova_despesa)
            db.session.commit()
            
            return redirect(url_for('home'))
        
        return render_template('add_despesa.html')