import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='totvs@123', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `clientes`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `clientes` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `clientes`;
    CREATE TABLE `cliente` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `telefone` int(12) COLLATE utf8_bin NOT NULL,
      `endereco` varchar(30) NOT NULL,
      `ativo` boolean,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO clientes.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('vinicius', 'Vinicius Bonilha', 'vinicius'),
            ('juliana', 'Juliana Martins', 'juliana'),
            ('ellen', 'Ellen Bonilha', 'ellen'),
      ])

cursor.execute('select * from clientes.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo clientes
cursor.executemany(
      'INSERT INTO clientes.cliente (nome, telefone, endereco, ativo) VALUES (%s, %s, %s, %s)',
      [
            ('Steve Rogers', '985393982', 'New York', True),
            ('Bruce Banner', '985393982', 'New York', True),
            ('Tony Stark', '985393982', 'New York', False),
            ('James Rhodes', '985393982', 'New York', True),
            ('Scott Lang', '985393982', 'New York', True),
            ('Tchalla', '985393982', 'New York', True),
            ('Peter Parker', '985393982', 'New York', True),
            
      ])

cursor.execute('select * from clientes.cliente')
print(' -------------  Clientes:  -------------')
for cliente in cursor.fetchall():
    print(cliente[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()