from fakepinterest import app, database

if __name__ == "__main__":
    with app.app_context():
        database.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=False)

