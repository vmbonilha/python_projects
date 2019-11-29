from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify, make_response
import flask_excel as excel
from models import Cliente, Usuario
from dao import ClienteDao, UsuarioDao
from flask_mysqldb import MySQL
import os
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'Fadergs'

app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "totvs@123"
app.config['MYSQL_DB'] = "clientes"
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    cliente = cliente_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Cliente', cliente=cliente)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    rg = request.form['rg']
    milhas = request.form['milhas']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    ativo = request.form['ativo']
    cliente = Cliente(nome, cpf, rg, milhas, telefone, endereco, ativo, id=request.form['id'])
    cliente_dao.salvar(cliente)
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    rg = request.form['rg']
    milhas = request.form['milhas']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    ativo = request.form['ativo']
    cliente = Cliente(nome, cpf, rg, milhas, telefone, endereco, ativo)
    cliente_dao.salvar(cliente)
    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    file.save(f'{upload_path}/capa{cliente.id}.jpg')
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

@app.route('/deletar/<int:id>')
def deletar(id):
    cliente_dao.deletar(id)
    flash('O Cliente foi delatado com sucesso!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado')
    return redirect(url_for('login'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)
    
@app.route('/export', methods=['GET'])
def export():
    si = StringIO()
    cw = csv.writer(si)
    lista = cliente_dao.listar()
    for cliente in lista:
        cw.writerow([cliente.id, cliente.nome, cliente.cpf, cliente.telefone, cliente.endereco, cliente.ativo])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=clientes.csv'
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == "__main__":
    excel.init_excel(app)
app.run(debug=True)