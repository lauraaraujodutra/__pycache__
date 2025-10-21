# --- AULA 1: As Ferramentas (Importações) ---
# Para construir nossa interface gráfica, precisamos de "peças".
# Cada 'import' traz um conjunto de ferramentas ou um módulo específico que criamos.

import tkinter as tk  # Importa a biblioteca principal do Tkinter. Nós a chamamos de 'tk' para ficar mais curto. É a base de tudo.
#from tkinter import ttk  # 'ttk' é uma versão mais moderna dos componentes do Tkinter. Deixa os botões e janelas mais bonitos.

#mudança aqui
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from db import ensuredb  # Do nosso arquivo 'db.py', trazemos a função que verifica se o banco de dados existe e o cria se necessário.
from utils import centralizarjanela  # Do nosso arquivo 'utils.py', trazemos a função que centraliza a janela na tela.
from login import showlogin  # Do 'login.py', importamos a função que sabe como desenhar a tela de login.
from comidas import showcomidas  # Do 'comidas.py', a função que desenha a tela de cadastro de comidas.
from estoque import showgestaoestoque  # Do 'estoque.py', a função que desenha a tela de controle de estoque.

# --- AULA 2: A Planta da Casa (A Classe Principal) ---
# Uma 'class' é como uma planta para construir um objeto.
# Nossa classe 'App' é a planta para construir a janela principal do nosso programa.
# Ela 'herda' de 'tk.Tk', o que significa que ela já nasce sabendo tudo que uma janela normal do Tkinter sabe fazer.

class App(tk.Tk):
    """Classe principal - Controle de Estoque de Comidas Nordestinas."""

    # O método '__init__' é o "construtor". É o que acontece assim que a janela é criada.
    def __init__(self):
        super().__init__()  # Este comando inicializa a "parte janela" do nosso objeto. É como ligar a ignição do carro.
        self.title("Controle de Estoque de Comidas Nordestinas")  # Define o texto que aparece na barra de título da janela.
        
        ensuredb()  # Chama a função que importamos para garantir que o banco de dados está pronto para ser usado.
        
        # 'self' se refere ao próprio objeto (a janela). Aqui, criamos uma "gaveta" chamada 'currentuser'.
        # Ela começa vazia (None) e vai guardar as informações de quem fizer o login.
        self.currentuser = None
        
        # No início, queremos uma janela pequena para o login.
        centralizarjanela(self, 400, 250)  # Centraliza a janela com 400px de largura e 250px de altura.
        
        # A primeira coisa que o usuário deve ver é a tela de login.
        showlogin(self)  # Chama a função do 'login.py' para desenhar a tela de login dentro da nossa janela ('self').

    # --- AULA 3: A Tela Principal (Método showmain) ---
    # Este método é responsável por mostrar o menu principal depois que o login dá certo.
    def showmain(self):
        """Exibe a tela principal do sistema após o login."""
        
        # Antes de desenhar a tela nova, precisamos limpar a antiga (a de login).
        # Este 'for' passa por todos os componentes ('widgets') que estão na janela e os destrói.
        for w in self.winfo_children():
            w.destroy()
            
        # A tela principal é maior. Vamos reajustar o tamanho e centralizar de novo.
        centralizarjanela(self, 1000, 550)

        # --- Construindo o Menu Superior ---
        # Um 'Frame' é como um container, uma moldura para organizar outros componentes.
        top = ttk.Frame(self, padding=2)
        top.pack(fill="x")  # '.pack()' é um jeito de posicionar o componente. 'fill="x"' faz ele ocupar toda a largura.
        
        # Mostra o nome do usuário que logou.
        # Usamos um f-string para formatar o texto.
        # 'self.currentuser.get(...)' pega o nome do dicionário do usuário. O '' é um valor padrão caso não encontre.
        ttk.Label(top, text=f"Usuário logado: {self.currentuser.get('nome_completo','')}").pack(side="left")
        
        # Botão para sair. 'command' diz o que fazer quando clicado.
        # 'lambda: showlogin(self)' cria uma mini-função que chama a tela de login de novo (efetivamente um logout).
        ttk.Button(top, text="Sair", command=lambda: showlogin(self)).pack(side="right")
        
        # Botão para ir para a tela de comidas.
        ttk.Button(top, text="Cadastro de Comidas", command=lambda: showcomidas(self)).pack(side="right", padx=6)
        
        # Botão para ir para a tela de estoque.
        ttk.Button(top, text="Gestão de Estoque", command=lambda: showgestaoestoque(self)).pack(side="right", padx=6)

        # --- Construindo a Mensagem de Boas-Vindas ---
        center = ttk.Frame(self, padding=40)
        center.pack(expand=True) # 'expand=True' faz este frame ocupar o espaço que sobrar.
        
        # Criamos uma mensagem de texto com várias linhas.
        #ttk.Label(text=f"Olá, {self.currentuser.get('nome_completo','')}")
        msg = (
            f"Olá, {self.currentuser.get('nome_completo','')}!\n"
            "Bem-vindo ao sistema de controle de estoque de Comidas Nordestinas.\n\n"
            "Aqui você pode:\n"
            " ** Cadastrar novos pratos e comidas típicas\n"
            " ** Consultar e editar o estoque\n"
            " ** Registrar entradas e saídas"
            "\n\nEscolha um botão na barra de opções acima para começar."
        )
        # Um 'Label' é usado para mostrar texto. Configuramos a fonte, a cor (fg = foreground) e o alinhamento.
        tk.Label(center, text=msg, font=("TkDefaultFont", 18),justify="left").pack()

# --- AULA 4: O Ponto de Partida ---
# Esta é uma construção padrão em Python. O código dentro deste 'if' só roda
# quando você executa este arquivo diretamente (ex: 'python main.py').
if __name__ == "__main__":
    # 1. Cria a nossa janela principal usando a planta ('class App').
    app = App()
    
    # 2. Inicia o "loop principal" da interface. Isso faz a janela ficar aberta,
    # esperando por cliques de mouse, digitação, etc. Sem isso, o programa fecharia instantaneamente.
    app.mainloop()
