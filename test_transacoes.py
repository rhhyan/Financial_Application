import unittest
from app import app, db, Transacao  # Importando a aplicação e o modelo

class TestTransacoesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura o ambiente de testes"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando banco em memória para testes
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def setUp(self):
        """Cria a tabela antes de cada teste"""
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Deleta os dados após cada teste"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registrar_transacao(self):
        """Testa a rota de registrar transação"""
        response = self.client.post('/registrar_transacao', json={
            'valor': 100,
            'data': '2025-02-17',
            'categoria': 'Alimentação',
            'tipo': 'receita',
            'descricao': 'Salário',
            'usuario_id': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Transação registrada com sucesso!', response.get_json()['message'])

    def test_obter_saldo(self):
        """Testa a rota de obter saldo"""
        # Registrando transações
        self.client.post('/registrar_transacao', json={
            'valor': 100,
            'data': '2025-02-17',
            'categoria': 'Alimentação',
            'tipo': 'receita',
            'descricao': 'Salário',
            'usuario_id': 1
        })
        self.client.post('/registrar_transacao', json={
            'valor': 50,
            'data': '2025-02-17',
            'categoria': 'Lazer',
            'tipo': 'despesa',
            'descricao': 'Cinema',
            'usuario_id': 1
        })

        response = self.client.get('/saldo?usuario_id=1')
        saldo = response.get_json()['saldo']
        self.assertEqual(saldo, 50)

if __name__ == '__main__':
    unittest.main()