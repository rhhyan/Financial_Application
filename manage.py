from app import app, db
from flask_migrate import Migrate
from flask_script import Manager

# Configuração do Flask-Migrate
migrate = Migrate(app, db)

# Inicializa o Flask-Script
manager = Manager(app)

if __name__ == '__main__':
    manager.run()