from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, END
from tkinter import Tk, Frame, Label, Button, NSEW, FALSE
from tkinter.ttk import Style
from PIL import Image, ImageTk
import sys
import os
# Adiciona o diretório principal ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# importando as funcoes da view
from view.view import Usuario, Livro, Emprestimo, Devolucao

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
        app_img = Image.open('template/images/icons8-books-100.png').resize((40, 40))
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
            ('template/images/icons8-add-100.png', " Novo usuário", 'novo_usuario'),
            ('template/images/icons8-add-100.png', " Novo livro", 'novo_livro'),
            ('template/images/icons8-books-100.png', " Exibir todos os livros", 'ver_livros'),
            ('template/images/icons8-user-100.png', " Exibir todos os usuários", 'ver_usuarios'),
            ('template/images/icons8-add-100.png', " Realizar um empréstimo", 'emprestimo'),
            ('template/images/icons8-update-100.png', " Devolução de um empréstimo", 'retorno'),
            ('template/images/icons8-shopping-cart-100.png', " Livros emprestados no momento", 'ver_livros_emprestados')
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

