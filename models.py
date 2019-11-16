
class Cliente:
    def __init__(self, nome, telefone, endereco, ativo, id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.ativo = ativo

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha