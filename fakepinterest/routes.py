# Importa a função render_template da biblioteca Flask para renderizar templates HTML
from flask import render_template, url_for, redirect, flash, send_from_directory
# Importa a instância do aplicativo Flask a partir do módulo atual
from . import app, database, bcrypt 
# Importa o decorador login_required da biblioteca Flask-Login para proteger rotas que exigem autenticação
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.models import Usuario, Foto
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


# Criar as rotas do site (os links)

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    # Renderiza o template "homepage.html" e passa o formulário como argumento
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)        

# Define a rota para a página de criação de conta
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criar_conta = FormCriarConta()
    
    if form_criar_conta.validate_on_submit():
        # Verifica se o email ou username já existem
        if Usuario.query.filter_by(email=form_criar_conta.email.data).first() or \
           Usuario.query.filter_by(username=form_criar_conta.username.data).first():
            flash('Email ou nome de usuário já estão em uso. Tente outro.', 'error')
            return redirect(url_for("criarconta"))
        
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, 
                          senha=senha, 
                          email=form_criar_conta.email.data)
        
        try:
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario, remember=True)
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for("perfil", id_usuario=usuario.id))
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao persistir: {e}")
            flash('Houve um erro ao criar a conta. Tente novamente.', 'error')

    return render_template("criarconta.html", form=form_criar_conta)



# Define a rota para a página de perfil do usuário
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    form_foto = FormFoto()  # Sempre cria o formulário

    if int(id_usuario) == current_user.id:
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)

            # Salva no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            flash('Foto enviada com sucesso!', 'success')

    # Renderiza o template e passa o formulário, mesmo se o usuário não estiver vendo seu próprio perfil
    return render_template("perfil.html", usuario=current_user, form=form_foto)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()#[:100] caso queria as 100 primeiras fotos, por exemplo.
    return render_template("feed.html", fotos=fotos)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/deletar_foto/<int:foto_id>", methods=["POST"])
@login_required
def deletar_foto(foto_id):
    foto = Foto.query.get_or_404(foto_id)  # Busca a foto ou retorna 404 se não existir
    if foto.id_usuario == current_user.id:  # Verifica se o usuário é o dono da foto
        database.session.delete(foto)  # Deleta a foto
        database.session.commit()
        flash('Foto deletada com sucesso!', 'success')
    else:
        flash('Você não tem permissão para deletar esta foto.', 'error')
    return redirect(url_for('perfil', id_usuario=current_user.id))  # Redireciona para o perfil