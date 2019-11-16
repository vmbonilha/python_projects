from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)

app.secret_key = 'Fadergs'

class Cliente:
    def __init__(self, nome, telefone, endereco, habilitado):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.habilitado = habilitado

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('vinicius', 'vinicius bonilha', '1234')
usuario2 = Usuario('juliana', 'Juliana Martins', '12345')

usuarios = {usuario1.id: usuario1, usuario2: usuario2}

vinicius = Cliente('Vinicius', '444','av terra nova', 'True')
juliana = Cliente('Juliana', '555','av terra nova', 'True')
ellen = Cliente('Ellen', '666','av terra nova', 'True')
lista = [vinicius,juliana,ellen]

@app.route('/')
def index():
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
    habilitado = request.form['habilitado']
    cliente = Cliente(nome, telefone, endereco, habilitado)
    lista.append(cliente)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, )

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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