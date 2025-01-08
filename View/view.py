from tkinter .ttk import *
from tkinter import *
from PIL import Image, ImageTk
from tkinter import Tk, ttk
from datetime import datetime, date, timedelta
import re
from tkinter import messagebox, END
# importando as funcoes da view
#from .model import DatabaseManager
from tkinter import Tk, Frame, Label, Button, NSEW, FALSE
from tkinter.ttk import Style
from PIL import Image, ImageTk
#from Model.database_manager import DatabaseManager
import sys
import os

# Adiciona o diretório principal ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.database_manager import DatabaseManager




class Controller:
    """Classe para controlar as ações do sistema."""

    def __init__(self, frame_direita):
        self.__frame_direita = frame_direita

    def control(self, action):
        for widget in self.__frame_direita.winfo_children():
            widget.destroy()

        if action == 'novo_usuario':
            usuario = Usuario()
            usuario.cadastrar_usuario(self.__frame_direita)
        elif action == 'ver_usuarios':
            usuario = Usuario()
            usuario.ver_usuarios(self.__frame_direita)
        elif action == 'novo_livro':
            livro = Livro()
            livro.cadastrar_livro(self.__frame_direita)
        elif action == 'ver_livros':
            livro = Livro()
            livro.ver_livros(self.__frame_direita)
        elif action == 'emprestimo':
            emprestimo = Emprestimo()
            emprestimo.emprestar_livro(self.__frame_direita)
        elif action == 'retorno':
            devolucao = Devolucao()
            devolucao.devolver_livro(self.__frame_direita)
        elif action == 'ver_livros_emprestados':
            emprestimo = Emprestimo()
            emprestimo.ver_livros_emprestados(self.__frame_direita)

class App:
    """Classe principal da aplicação."""

    def __init__(self):
        self.__janela = Tk()
        self.__configurar_janela()
        self.__criar_frames()
        self.__controller = Controller(self.__frame_direita)
        self.__criar_botoes()

    def __configurar_janela(self):
        """Configurações internas da janela."""
        self.__janela.title("Sistema de Gerenciamento de Livros")
        self.__janela.geometry('1150x393')
        self.__janela.configure(background="#FFFFFF")
        self.__janela.resizable(width=FALSE, height=FALSE)

        self.__style = Style(self.__janela)
        self.__style.theme_use("clam")

    def __criar_frames(self):
        """Cria os frames da interface gráfica."""
        self.__frame_cima = Frame(self.__janela, width=1150, height=50, bg="#E9A178", relief="flat")
        self.__frame_cima.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.__frame_esquerda = Frame(self.__janela, width=150, height=345, bg="#403d3d", relief="solid")
        self.__frame_esquerda.grid(row=1, column=0, sticky=NSEW)

        self.__frame_direita = Frame(self.__janela, width=890, height=345, bg="#FFFFFF", relief="raised")
        self.__frame_direita.grid(row=1, column=1, sticky=NSEW)

        self.__adicionar_logo()

    def __adicionar_logo(self):
        """Adiciona o logo ao frame superior."""
        app_img = Image.open('images/icons8-books-100.png').resize((40, 40))
        app_img = ImageTk.PhotoImage(app_img)

        app_logo = Label(self.__frame_cima, image=app_img, compound='left', padx=5, anchor='nw',
                         bg="#E9A178", fg="#FFFFFF")
        app_logo.image = app_img  # Previne o garbage collector de remover a imagem
        app_logo.place(x=5, y=0)

        app_label = Label(self.__frame_cima, text="Sistema de Gerenciamento de Livros", compound='left', padx=5,
                          anchor='nw', font=('Verdana 15 bold'), bg='#E9A178', fg="#FFFFFF")
        app_label.place(x=50, y=7)

        app_linha = Label(self.__frame_cima, width=1150, height=1, padx=5, anchor='nw', font=('Verdana 1'),
                          bg='#38576b', fg="#FFFFFF")
        app_linha.place(x=0, y=47)

    def __criar_botoes(self):
        """Adiciona os botões ao menu esquerdo."""
        botoes = [
            ('images/icons8-add-100.png', " Novo usuário", 'novo_usuario'),
            ('images/icons8-add-100.png', " Novo livro", 'novo_livro'),
            ('images/icons8-books-100.png', " Exibir todos os livros", 'ver_livros'),
            ('images/icons8-user-100.png', " Exibir todos os usuários", 'ver_usuarios'),
            ('images/icons8-add-100.png', " Realizar um empréstimo", 'emprestimo'),
            ('images/icons8-update-100.png', " Devolução de um empréstimo", 'retorno'),
            ('images/icons8-shopping-cart-100.png', " Livros emprestados no momento", 'ver_livros_emprestados')
        ]

        for i, (imagem, texto, comando) in enumerate(botoes):
            self.__adicionar_botao(imagem, texto, comando, i)

    def __adicionar_botao(self, imagem, texto, comando, linha):
        """Adiciona um botão ao menu esquerdo."""
        img = Image.open(imagem).resize((18, 18))
        img = ImageTk.PhotoImage(img)

        botao = Button(self.__frame_esquerda, command=lambda: self.__controller.control(comando),
                       image=img, compound='left', anchor='nw', text=texto, bg="#403d3d", fg="#FFFFFF",
                       font=('Ivy 11'), overrelief='ridge', relief='groove')
        botao.image = img
        botao.grid(row=linha, column=0, sticky=NSEW, padx=5, pady=6)

    def run(self):
        """Inicia o loop principal da aplicação."""
        self.__janela.mainloop()

    


# Classe Usuario
class Usuario(DatabaseManager):
    
    def __init__(self):
        super().__init__()
        self.__first_name = None
        self.__last_name = None
        self.__email = None
        self.__phone = None


    def __set_dados(self, first_name, last_name, email, phone):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone = phone

    def __get_dados(self):
        return {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "email": self.__email,
            "phone": self.__phone,
        }

    def __validar_dados(self):
        # Validação do primeiro nome e sobrenome
        if not self.__first_name.isalpha() or len(self.__first_name) < 2:
            return "O primeiro nome deve conter apenas letras e ter pelo menos 2 caracteres."
        if not self.__last_name.isalpha() or len(self.__last_name) < 2:
            return "O sobrenome deve conter apenas letras e ter pelo menos 2 caracteres."

        # Validação do e-mail
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.__email):
            return "O e-mail informado não é válido."

        # Validação do telefone
        if not self.__phone.isdigit() or len(self.__phone) < 10 or len(self.__phone) > 15:
            return "O número de telefone deve conter apenas dígitos e ter entre 10 e 15 caracteres."

        return None

    def cadastrar_usuario(self, frame_direita):
        def add_usuario():
            self.__set_dados(e_p_nome.get().strip(), e_sobrenome.get().strip(), e_email.get().strip(), e_numero.get().strip())

            # Validação dos dados
            mensagem_erro = self.__validar_dados()
            if mensagem_erro:
                messagebox.showerror('Erro', mensagem_erro)
                return

            # Inserir no banco de dados
            self._insert_user(self.__first_name, self.__last_name, self.__email, self.__phone)
            messagebox.showinfo('Cadastrado', 'Usuário inserido com sucesso!')
            
            # Limpar campos
            for entrada in [e_p_nome, e_sobrenome, e_email, e_numero]:
                entrada.delete(0, END)

        # Construção do layout
        self.__estilizar_formulario(frame_direita)
        e_p_nome, e_sobrenome, e_email, e_numero = self.__criar_campos_usuario(frame_direita)
        Button(frame_direita, text="Salvar", command=add_usuario, bg="#38576b", fg="#FFFFFF").grid(row=7, column=1, pady=12)

    # Métodos privados para estilização
    def __estilizar_formulario(self, frame_direita):
        app_ = Label(frame_direita, text="Cadastrar Usuário", width=50, compound=LEFT, padx=5, pady=10, font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d")
        app_.grid(row=0, column=0, columnspan=4, sticky=NSEW)
        app_linha = Label(frame_direita, width=770, height=1, anchor=NW, font=('Verdana 1'), bg='#38576b', fg="#FFFFFF")
        app_linha.grid(row=1, column=0, columnspan=4, sticky=NSEW)

    def __criar_campos_usuario(self, frame_direita):
        l_p_nome = Label(frame_direita, text="Primeiro nome*", anchor=NW, font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d")
        l_p_nome.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)
        e_p_nome = Entry(frame_direita, width=25, justify='left', relief='solid')
        e_p_nome.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)

        l_sobrenome = Label(frame_direita, text="Sobrenome*", anchor=NW, font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d")
        l_sobrenome.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)
        e_sobrenome = Entry(frame_direita, width=25, justify='left', relief='solid')
        e_sobrenome.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

        l_email = Label(frame_direita, text="E-mail*", anchor=NW, font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d")
        l_email.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)
        e_email = Entry(frame_direita, width=25, justify='left', relief='solid')
        e_email.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

        l_numero = Label(frame_direita, text="Número de telefone*", anchor=NW, font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d")
        l_numero.grid(row=5, column=0, padx=5, pady=5, sticky=NSEW)
        e_numero = Entry(frame_direita, width=25, justify='left', relief='solid')
        e_numero.grid(row=5, column=1, padx=5, pady=5, sticky=NSEW)

        return e_p_nome, e_sobrenome, e_email, e_numero


    def ver_usuarios(self, frame_direita):
        # Título
        app_ = Label(frame_direita, text="Usuários cadastrados", width=50, compound=LEFT, padx=5, pady=10, 
                    font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d")
        app_.grid(row=0, column=0, columnspan=4, sticky=NSEW)
        app_linha = Label(frame_direita, width=400, height=1, anchor=NW, font=('Verdana 1'), 
                        bg='#38576b', fg="#FFFFFF")
        app_linha.grid(row=1, column=0, columnspan=4, sticky=NSEW)

        # Obter dados
        try:
            dados = self._get_users()  # Deve retornar uma lista de usuários no formato adequado.
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter os dados dos usuários: {e}")
            return

        # Cabeçalho da tabela
        list_header = ['ID', 'Nome', 'Sobrenome', 'Email', 'Telefone']
        global tree

        # Criar Treeview com scrollbars
        tree = ttk.Treeview(frame_direita, selectmode="extended", columns=list_header, show="headings")
        vsb = ttk.Scrollbar(frame_direita, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_direita, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar Treeview e scrollbars
        tree.grid(column=0, row=2, sticky='nsew')
        vsb.grid(column=1, row=2, sticky='ns')
        hsb.grid(column=0, row=3, sticky='ew')
        frame_direita.grid_rowconfigure(0, weight=12)

        # Configuração das colunas
        hd = ["nw", "nw", "nw", "nw", "nw"]
        h = [33, 150, 160, 210, 200]  # Larguras das colunas
        for i, col in enumerate(list_header):
            tree.heading(col, text=col, anchor='nw')
            tree.column(col, width=h[i], anchor=hd[i])

        # Inserir dados na tabela
        for item in dados:
            tree.insert('', 'end', values=item)


# Classe Livro

from tkinter import Label, Entry, Button, messagebox, ttk
from datetime import datetime

class Livro(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.__title = None
        self.__author = None
        self.__publisher = None
        self.__year = None
        self.__isbn = None

    def __set_dados(self, title, author, publisher, year, isbn):
        self.__title = title
        self.__author = author
        self.__publisher = publisher
        self.__year = year
        self.__isbn = isbn

    def __get_dados(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "publisher": self.__publisher,
            "year": self.__year,
            "isbn": self.__isbn,
        }

    def cadastrar_livro(self, frame_direita):
        def add_livro():
            title = e_titulo.get().strip()
            author = e_autor.get().strip()
            publisher = e_editora.get().strip()
            year = e_ano.get().strip()
            isbn = e_isbn.get().strip()

            if any(campo == '' for campo in [title, author, publisher, year, isbn]):
                messagebox.showerror('Erro', 'Preencha todos os campos!')
                return

            if not self.__validar_titulo_e_autor(title):
                messagebox.showerror('Erro', 'O título deve conter apenas letras e espaços.')
                return

            if not self.__validar_titulo_e_autor(author):
                messagebox.showerror('Erro', 'O autor deve conter apenas letras e espaços.')
                return

            if not self.__validar_ano(year):
                messagebox.showerror('Erro', 'Ano de publicação inválido. Deve ser numérico e não estar no futuro.')
                return

            self.__set_dados(title, author, publisher, year, isbn)
            self._insert_book(title, author, publisher, year, isbn)  # Chamando o método protegido da classe base
            messagebox.showinfo('Cadastrado', 'Livro inserido com sucesso!')
            
            for entrada in [e_titulo, e_autor, e_editora, e_ano, e_isbn]:
                entrada.delete(0, END)

        self.__estilizar_cadastro_livro(frame_direita, add_livro)

    def ver_livros(self, frame_direita):
        self.__estilizar_ver_livros(frame_direita)

    def __validar_titulo_e_autor(self, texto):
        """Verifica se o título ou autor contém apenas letras e espaços."""
        return texto.replace(' ', '').isalpha()

    def __validar_ano(self, ano):
        """Valida se o ano é um número válido e não está no futuro."""
        try:
            ano_int = int(ano)
            ano_atual = datetime.now().year
            return 0 < ano_int <= ano_atual
        except ValueError:
            return False

    def __estilizar_cadastro_livro(self, frame_direita, add_livro):
        Label(frame_direita, text="Inserir um novo livro", width=50, compound='left', padx=5, pady=10,
              font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d").grid(row=0, column=0, columnspan=3, sticky='nsew')
        Label(frame_direita, width=770, height=1, anchor='nw', font=('Verdana 1'), bg='#38576b', fg="#FFFFFF").grid(row=1, column=0, columnspan=3, sticky='nsew')

        labels = ["Título do Livro*", "Autor do Livro*", "Editora do Livro*", "Ano de publicação do Livro*", "ISBN do Livro*"]
        entries = []
        for i, label_text in enumerate(labels):
            Label(frame_direita, text=label_text, anchor='nw', font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d").grid(row=2 + i, column=0, padx=5, pady=5, sticky='nsew')
            entry = Entry(frame_direita, width=25, justify='left', relief='solid')
            entry.grid(row=2 + i, column=1, padx=5, pady=5, sticky='nsew')
            entries.append(entry)

        global e_titulo, e_autor, e_editora, e_ano, e_isbn
        e_titulo, e_autor, e_editora, e_ano, e_isbn = entries

        Button(frame_direita, text="Salvar", command=add_livro, bg="#38576b", fg="white").grid(row=7, column=1, pady=12)

    def __estilizar_ver_livros(self, frame_direita):
        Label(frame_direita, text="Livros cadastrados", width=50, compound='left', padx=5, pady=10,
              font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d").grid(row=0, column=0, columnspan=4, sticky='nsew')
        Label(frame_direita, width=400, height=1, anchor='nw', font=('Verdana 1'), bg='#38576b', fg="#FFFFFF").grid(row=1, column=0, columnspan=4, sticky='nsew')

        dados = self._exibir_livros()  # Chamando o método protegido da classe base
        list_header = ['ID', 'Título', 'Autor', 'Editora', 'Ano', 'ISBN']

        tree = ttk.Treeview(frame_direita, selectmode="extended", columns=list_header, show="headings")
        vsb = ttk.Scrollbar(frame_direita, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_direita, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(column=0, row=2, sticky='nsew')
        vsb.grid(column=1, row=2, sticky='ns')
        hsb.grid(column=0, row=3, sticky='ew')
        frame_direita.grid_rowconfigure(0, weight=12)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw"]
        h = [33, 200, 170, 150, 100, 100]

        for n, col in enumerate(list_header):
            tree.heading(col, text=col, anchor='nw')
            tree.column(col, width=h[n], anchor=hd[n])

        for item in dados:
            tree.insert('', 'end', values=item)




# Classe Emprestimo
class Emprestimo(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.__user_id = None
        self.__book_id = None
        self.__date_loan = datetime.today().date().strftime('%d-%m-%Y')
        self.__date_return = (datetime.today().date() + timedelta(days=7)).strftime('%d-%m-%Y')

    def __set_dados(self, user_id, book_id):
        self.__user_id = user_id
        self.__book_id = book_id

    def __get_dados(self):
        return {
            "user_id": self.__user_id,
            "book_id": self.__book_id,
            "date_loan": self.__date_loan,
            "date_return": self.__date_return
        }

    def __validar_dados(self, user_id, book_id):
        if not user_id or not book_id:
            return "Todos os campos são obrigatórios."

        if not user_id.isdigit() or not book_id.isdigit():
            return "Os IDs devem conter apenas números."

        if int(user_id) <= 0 or int(book_id) <= 0:
            return "Os IDs devem ser números positivos."

        # Verifica se o usuário existe no banco
        if not self._check_user_exists(user_id):
            return f"O usuário com ID {user_id} não foi encontrado."

        # Verifica se o livro existe no banco
        if not self._check_book_exists(book_id):
            return f"O livro com ID {book_id} não foi encontrado."

        return None

    def emprestar_livro(self, frame_direita):
        def add_emprestimo():
            user_id = e_usuario.get()
            book_id = e_livro.get()

            erro = self.__validar_dados(user_id, book_id)
            if erro:
                messagebox.showerror('Erro', erro)
                return

            self.__set_dados(user_id, book_id)

            try:
                self._insert_loan(self.__book_id, self.__user_id, self.__date_loan, None)
                messagebox.showinfo('Sucesso', 'Livro emprestado com sucesso!')
                for entrada in [e_usuario, e_livro]:
                    entrada.delete(0, END)
            except Exception as e:
                messagebox.showerror('Erro', f'Ocorreu um erro ao registrar o empréstimo: {e}')

        self.__estilizar_emprestar_livro(frame_direita, add_emprestimo)

    def ver_livros_emprestados(self, frame_direita):
        self.__estilizar_ver_livros_emprestados(frame_direita)

    def __estilizar_emprestar_livro(self, frame_direita, add_emprestimo):
        Label(frame_direita, text="Realizar um empréstimo", width=50, compound='left', padx=5, pady=10,
              font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d").grid(row=0, column=0, columnspan=3, sticky='nsew')
        Label(frame_direita, width=770, height=1, anchor='nw', font=('Verdana 1'), bg='#38576b', fg="#FFFFFF").grid(row=1, column=0, columnspan=3, sticky='nsew')

        labels = ["Digite o ID do usuário*", "Digite o ID do livro*"]
        entries = []
        for i, label_text in enumerate(labels):
            Label(frame_direita, text=label_text, anchor='nw', font=('Ivy 10'), bg="#FFFFFF", fg="#403d3d").grid(row=2 + i, column=0, padx=5, pady=5, sticky='nsew')
            entry = Entry(frame_direita, width=25, justify='left', relief='solid')
            entry.grid(row=2 + i, column=1, padx=5, pady=5, sticky='nsew')
            entries.append(entry)

        global e_usuario, e_livro
        e_usuario, e_livro = entries

        Button(frame_direita, text="Salvar", command=add_emprestimo, bg="#38576b", fg="white").grid(row=4, column=1, pady=12)

    def __estilizar_ver_livros_emprestados(self, frame_direita):
        Label(frame_direita, text="Livros emprestados no momento", width=50, compound='left', padx=5, pady=10,
              font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d").grid(row=0, column=0, columnspan=4, sticky='nsew')
        Label(frame_direita, width=400, height=1, anchor='nw', font=('Verdana 1'), bg='#38576b', fg="#FFFFFF").grid(row=1, column=0, columnspan=4, sticky='nsew')

        dados = self._get_books_on_loan()
        list_header = ['ID', 'Título', 'Nome do usuário', 'D. Empréstimo', 'D. Devolução']

        tree = ttk.Treeview(frame_direita, selectmode="extended", columns=list_header, show="headings")
        vsb = ttk.Scrollbar(frame_direita, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame_direita, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(column=0, row=2, sticky='nsew')
        vsb.grid(column=1, row=2, sticky='ns')
        hsb.grid(column=0, row=3, sticky='ew')
        frame_direita.grid_rowconfigure(0, weight=12)

        hd = ["nw", "nw", "nw", "nw", "nw"]
        h = [33, 200, 200, 160, 160]

        for n, col in enumerate(list_header):
            tree.heading(col, text=col, anchor='nw')
            tree.column(col, width=h[n], anchor=hd[n])

        for book in dados:
            tree.insert('', 'end', values=[book[0], book[1], f"{book[2]} {book[3]}", book[4], book[5]])



# Classe Devolucao

class Devolucao(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.__loan_id = None
        self.__return_date = None

    def __set_dados(self, loan_id, return_date):
        self.__loan_id = loan_id
        self.__return_date = return_date

    def __get_dados(self):
        return {
            "loan_id": self.__loan_id,
            "return_date": self.__return_date
        }

    def devolver_livro(self, frame_direita):
        def add_devolucao():
            loan_id = e_id_emprestimo.get()
            return_date = e_data_retorno.get()

            if not loan_id or not return_date:
                messagebox.showerror('Erro', 'Preencha todos os campos obrigatórios!')
                return

            # Verificar se o ID do empréstimo existe
            if not self._check_loan_exists(loan_id):
                messagebox.showerror('Erro', f"Empréstimo com ID {loan_id} não encontrado.")
                return

            # Validar formato da data
            if not self.__validar_data(return_date):
                messagebox.showerror('Erro', 'A data deve estar no formato DD-MM-AAAA.')
                return

            try:
                self.__set_dados(loan_id, return_date)
                self._update_loan_return_data(loan_id, return_date)
                messagebox.showinfo('Devolução', 'Livro devolvido com sucesso!')
                for entry in [e_id_emprestimo, e_data_retorno]:
                    entry.delete(0, END)
            except Exception as e:
                messagebox.showerror('Erro', f"Ocorreu um erro ao registrar a devolução: {e}")

        self.__estilizar_devolucao(frame_direita, add_devolucao)

    def __validar_data(self, data):
        # Verifica se a data está no formato DD-MM-AAAA
        try:
            datetime.strptime(data, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def __estilizar_devolucao(self, frame_direita, add_devolucao):
        Label(frame_direita, text="Devolver um livro", width=50, compound=LEFT, padx=5, pady=10, 
              font=('Verdana 12'), bg="#FFFFFF", fg="#403d3d").grid(row=0, column=0, columnspan=3, sticky=NSEW)
        Label(frame_direita, width=770, height=1, anchor=NW, font=('Verdana 1'), bg='#38576b', 
              fg="#FFFFFF").grid(row=1, column=0, columnspan=3, sticky=NSEW)

        labels = ["Digite o ID do empréstimo*", "Atualizar data de devolução (DD-MM-AAAA)*"]
        global e_id_emprestimo, e_data_retorno
        entries = []

        for i, label_text in enumerate(labels):
            Label(frame_direita, text=label_text, anchor=NW, font=('Ivy 10'), bg="#FFFFFF", 
                  fg="#403d3d").grid(row=2 + i, column=0, padx=5, pady=5, sticky=NSEW)
            entry = Entry(frame_direita, width=25, justify='left', relief='solid')
            entry.grid(row=2 + i, column=1, padx=5, pady=5, sticky=NSEW)
            entries.append(entry)

        e_id_emprestimo, e_data_retorno = entries

        Button(frame_direita, text="Salvar", command=add_devolucao, bg="#38576b", 
               fg="#FFFFFF").grid(row=4, column=1, pady=10)

# Iniciando o loop principal
