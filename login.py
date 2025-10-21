# --- Bloco de Importações ---
# Importa as ferramentas necessárias para construir a tela e suas funcionalidades.

# Importa a biblioteca principal do tkinter e a renomeia para 'tk' por convenção.
# O tkinter é usado para criar todos os elementos visuais, como janelas, botões e textos.
import tkinter as tk

# Do tkinter, importa duas partes específicas:
# 'ttk': um conjunto de widgets (elementos gráficos) com aparência mais moderna e nativa do sistema operacional.
# 'messagebox': um módulo para exibir caixas de diálogo, como alertas de erro ou avisos.
from tkinter import ttk, messagebox

# Do nosso arquivo 'db.py', importa a função 'getconnection'.
# Essa função é a chave para abrir uma conexão com o banco de dados SQLite.
from db import getconnection

# Do nosso arquivo 'utils.py', importa a função 'centralizarjanela'.
# É uma função auxiliar que usamos para posicionar qualquer janela no centro da tela do computador.
from utils import centralizarjanela


# --- Definição da Função Principal ---
# Esta função é responsável por desenhar e controlar toda a tela de login.
# Ela recebe 'app' como argumento, que é a janela principal da nossa aplicação.
def showlogin(app):
    """Exibe a tela de login do sistema."""

    # --- Preparação da Janela ---
    # Antes de desenhar a tela de login, limpamos qualquer conteúdo que possa existir na janela principal.
    # O laço 'for' percorre todos os widgets filhos ('winfo_children') da janela 'app'.
    for w in app.winfo_children():
        # 'destroy()' remove o widget da tela, garantindo uma tela limpa.
        w.destroy()

    # Chama nossa função utilitária para centralizar a janela 'app'.
    # Definimos que a janela de login terá 400 pixels de largura e 250 de altura.
    centralizarjanela(app, 400, 250)

    # --- Criação do Contêiner Principal ---
    # Cria um 'Frame', que é como um painel ou uma área para organizar outros widgets.
    # 'padding=20' adiciona uma margem interna de 20 pixels para que os elementos não fiquem colados nas bordas.
    frm = ttk.Frame(app, padding=20)

    #frm = ttkb.Window(themename="darkly")





    # 'pack(expand=True)' adiciona o frame à janela principal e o faz ocupar o espaço disponível.
    frm.pack(expand=True)

    # --- Widgets da Tela de Login ---
    # Aqui começamos a adicionar os elementos visuais dentro do 'frm' (nosso painel).

    

    # Cria um rótulo (Label) com o texto "Login".
    # Aumentamos a fonte para 16 para dar destaque ao título.
    # '.grid(...)' organiza os widgets em um sistema de linhas e colunas.
    # 'columnspan=2' faz o título ocupar duas colunas, centralizando-o sobre os campos de entrada.
    # 'pady=10' adiciona um espaçamento vertical de 10 pixels.
    ttk.Label(frm, text="Login", font=("TkDefaultFont", 20), foreground="#A0522D").grid(column=0, row=0, columnspan=2, pady=10)

    # Cria o rótulo "Usuário".
    # 'sticky="e"' alinha o texto à direita (leste, 'east') dentro da sua célula na grade.
    ttk.Label(frm, text="Usuário").grid(column=0, row=1, sticky="e")

    # Cria a caixa de entrada de texto (Entry) para o nome de usuário.
    # 'width=25' define a largura do campo em caracteres.
    userent = ttk.Entry(frm, width=25)
    userent.grid(column=1, row=1) # Posiciona na coluna 1, linha 1.

    # Cria o rótulo "Senha", também alinhado à direita.
    ttk.Label(frm, text="Senha").grid(column=0, row=2, sticky="e")

    # Cria a caixa de entrada para a senha.
    # 'show="*"' faz com que qualquer caractere digitado seja exibido como um asterisco, para privacidade.
    pwdent = ttk.Entry(frm, show="*", width=25)
    pwdent.grid(column=1, row=2) # Posiciona na coluna 1, linha 2.

    # --- Lógica do Login ---
    # Define uma função interna que será executada quando o botão "Entrar" for clicado.
    def attempt_login():
        # Pega o texto digitado no campo de usuário e remove espaços em branco do início e do fim com '.strip()'.
        username = userent.get().strip()
        # Faz o mesmo para o campo de senha.
        password = pwdent.get().strip()

        # Validação: verifica se algum dos campos está vazio.
        if not username or not password:
            # Se estiverem, exibe uma caixa de aviso ao usuário.
            messagebox.showwarning("Falha", "Preencha usuário e senha.")
            # 'return' interrompe a execução da função aqui.
            return

        # 'with' garante que a conexão com o banco de dados será fechada automaticamente, mesmo se ocorrer um erro.
        with getconnection() as conn:
            # Executa uma consulta SQL para buscar um usuário na tabela 'usuarios'.
            # A consulta procura uma linha onde a coluna 'usuario' E a coluna 'senha' correspondam aos valores digitados.
            # Usar '?' previne um tipo de ataque chamado injeção de SQL.
            cur = conn.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
                (username, password)
            )
            # 'fetchone()' pega a primeira (e única, esperamos) linha que corresponde à consulta.
            row = cur.fetchone()

        # Verifica se 'row' contém algum dado. Se for 'None', significa que nenhum usuário foi encontrado.
        if row:
            # Se encontrou, armazena os dados do usuário (convertidos para um dicionário) na variável 'currentuser' da aplicação.
            app.currentuser = dict(row)
            # Chama a função 'showmain()' da aplicação principal para navegar para a próxima tela.
            app.showmain()
        else:
            # Se não encontrou, exibe uma mensagem de erro.
            messagebox.showerror("Falha", "Usuário ou senha inválidos.")

    # --- Botão de Ação ---
    # Cria o botão "Entrar".
    # 'command=attempt_login' define que a função 'attempt_login' será chamada quando o botão for clicado.
    ttk.Button(frm, text="Entrar", command=attempt_login).grid(column=0, row=3, columnspan=2, pady=10)
