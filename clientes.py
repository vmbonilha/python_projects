from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class Cliente:
    def __init__(self, nome, telefone, endereco, habilitado):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.habilitado = habilitado

vinicius = Cliente('Vinicius', '444','av terra nova', 'True')
juliana = Cliente('Juliana', '444','av terra nova', 'True')
ellen = Cliente('Ellen', '444','av terra nova', 'True')
lista = [vinicius,juliana,ellen]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Clientes', clientes=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Cliente')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    habilitado = request.form['habilitado']
    cliente = Cliente(nome, telefone, endereco, habilitado)
    lista.append(cliente)
    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'teste' == request.form['senha']:
        return redirect('/')
    else:
        return redirect('/login')

app.run(debug=True)