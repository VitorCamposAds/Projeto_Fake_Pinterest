from . import database

# Criar todas as tabelas
with app.app_context():
    database.create_all()
