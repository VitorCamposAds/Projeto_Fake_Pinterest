from fakepinterest import database

# Importar os modelos que você deseja criar
from fakepinterest.models import Usuario, Foto

def criar_tabelas():
    with database.app.app_context():
        database.create_all()  # Cria todas as tabelas

if __name__ == "__main__":
    criar_tabelas()
