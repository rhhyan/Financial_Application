from flask_sqlalchemy import SQLAlchemy

# Inicializando o banco de dados
db = SQLAlchemy()

class DespesaReceita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<DespesaReceita {self.id} - {self.descricao}>'