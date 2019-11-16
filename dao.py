from models import Cliente, Usuario

SQL_DELETA_Cliente = 'delete from cliente where id = %s'
SQL_Cliente_POR_ID = 'SELECT id, nome, telefone, endereco, ativo from cliente where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_Cliente = 'UPDATE cliente SET nome=%s, telefone=%s, endereco=%s, ativo=%s where id = %s'
SQL_BUSCA_ClienteS = 'SELECT id, nome, telefone, endereco, ativo from cliente'
SQL_CRIA_Cliente = 'INSERT into cliente (nome, telefone, endereco, ativo) values (%s, %s, %s, %s)'


class ClienteDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, Cliente):
        cursor = self.__db.connection.cursor()

        if (Cliente.id):
            cursor.execute(SQL_ATUALIZA_Cliente, (Cliente.nome, Cliente.telefone, Cliente.endereco, Cliente.ativo, Cliente.id))
        else:
            cursor.execute(SQL_CRIA_Cliente, (Cliente.nome, Cliente.telefone, Cliente.endereco, Cliente.ativo))
            Cliente.id = cursor.lastrowid
        self.__db.connection.commit()
        return Cliente

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_ClienteS)
        Clientes = traduz_Clientes(cursor.fetchall())
        return Clientes

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_Cliente_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Cliente(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_Cliente, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_Clientes(Clientes):
    def cria_Cliente_com_tupla(tupla):
        return Cliente(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])
    return list(map(cria_Cliente_com_tupla, Clientes))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
