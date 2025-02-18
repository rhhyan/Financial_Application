class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'