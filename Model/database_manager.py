import sqlite3

class DatabaseManager:
    def __init__(self):
        self.__database_name = 'dados.db'

    def _connect(self):
        return sqlite3.connect(self.__database_name)

    def _insert_book(self, titulo, autor, editora, ano_publicacao, isbn):
        conn = self._connect()
        conn.execute("INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn)\
                    VALUES (?, ?, ?, ?, ?)", (titulo, autor, editora, ano_publicacao, isbn))
        conn.commit()
        conn.close()

    def _insert_user(self, nome, sobrenome, email, telefone):
        conn = self._connect()
        conn.execute("INSERT INTO usuarios(nome, sobrenome, email, telefone)\
                     VALUES(?, ?, ?, ?)", (nome, sobrenome, email, telefone))
        conn.commit()
        conn.close()

    def _get_users(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios")
        users = c.fetchall()
        conn.close()
        return users

    def _exibir_livros(self):
        conn = self._connect()
        livros = conn.execute("SELECT * FROM livros").fetchall()
        conn.close()
        return livros

    def _insert_loan(self, id_livro, id_usuario, data_emprestimo, data_devolucao):
        conn = self._connect()
        conn.execute("INSERT INTO emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao)\
                     VALUES(?, ?, ?, ?)", (id_livro, id_usuario, data_emprestimo, data_devolucao))
        conn.commit()
        conn.close()

    def _get_books_on_loan(self):
        conn = self._connect()
        result = conn.execute("SELECT emprestimos.id, livros.titulo, usuarios.nome, usuarios.sobrenome, emprestimos.data_emprestimo, emprestimos.data_devolucao \
                               FROM livros \
                               INNER JOIN emprestimos ON livros.id = emprestimos.id_livro \
                               INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario \
                               WHERE emprestimos.data_devolucao IS NULL").fetchall()
        conn.close()
        return result

    def _update_loan_return_data(self, id_emprestimo, data_devolucao):
        conn = self._connect()
        conn.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (data_devolucao, id_emprestimo))
        conn.commit()
        conn.close()

    def _check_user_exists(self, user_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        return result is not None

    def _check_book_exists(self, book_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT id FROM livros WHERE id = ?", (book_id,))
        result = c.fetchone()
        conn.close()
        return result is not None

    def _check_loan_exists(self, loan_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT id FROM emprestimos WHERE id = ?", (loan_id,))
        result = c.fetchone()
        conn.close()
        return result is not None

# Exemplo de uso
# db_manager = DatabaseManager('dados.db')
# db_manager._insert_book("Cartomante", "Machado de Assis", "Saraiva", "1969", "123456")
# db_manager._insert_user("Joao", "Reis", "joao@gmail.com", "40028922")
# db_manager._insert_loan(1, 1, "2024-01-01", None)
# livros_emprestados = db_manager._get_books_on_loan()
# print(livros_emprestados)
# db_manager._exibir_livros()
# db_manager._update_loan_return_data(2, "2025-01-11")
