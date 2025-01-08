import sqlite3

# conectar ao banco de dados ou criar um novo banco de dados

con = sqlite3.connect('dados.db') #salvar em dados.db

# criar tabela de livros
con.execute('CREATE TABLE livros(\
            id INTEGER PRIMARY KEY,\
            titulo TEXT,\
            autor TEXT,\
            editora TEXT,\
            ano_publicacao INTEGER,\
            isbn TEXT)')

# criando tabela usuarios
con.execute('CREATE TABLE usuarios(\
            id INTEGER PRIMARY KEY,\
            nome TEXT,\
            sobrenome TEXT,\
            email TEXT,\
            telefone TEXT)' )

# criando tabela emprestimo
con.execute('CREATE TABLE emprestimos(\
            id INTEGER PRIMARY KEY,\
            id_livro INTEGER,\
            id_usuario INTEGER,\
            data_emprestimo TEXT,\
            data_devolucao TEXT,\
            FOREIGN KEY(id_livro) REFERENCES livros(id),\
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id))')