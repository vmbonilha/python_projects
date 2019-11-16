from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Cliente, Usuario
from dao import ClienteDao, UsuarioDao
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'Fadergs'

app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "totvs@123"
app.config['MYSQL_DB'] = "clientes"
app.config['MYSQL_PORT'] = 3306
db=MySQL(app)

cliente_dao = ClienteDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista=cliente_dao.listar()
    return render_template('lista.html', titulo='Clientes', clientes=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Cliente')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    ativo = request.form['ativo']
    cliente = Cliente(nome, telefone, endereco, ativo)
    cliente_dao.salvar(cliente)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, )

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' Logado com sucesso')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Senha errada')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('login'))

app.run(debug=True)