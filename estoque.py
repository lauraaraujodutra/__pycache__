# --- Bloco de Importações ---
# Importa as ferramentas necessárias para construir a tela e suas funcionalidades.

# Importa a biblioteca principal do tkinter para a criação de janelas e widgets.
import tkinter as tk
# Do tkinter, importa os widgets 'ttk' (com estilo moderno) e o 'messagebox' para exibir alertas.
from tkinter import ttk, messagebox
# Importa o módulo 'datetime' para trabalhar com datas, como pegar a data atual.
import datetime

# Do nosso arquivo 'db.py', importa a função para obter uma conexão com o banco de dados.
from db import getconnection
# Do nosso arquivo 'utils.py', importa a função para centralizar janelas na tela.
from utils import centralizarjanela


# --- Função Principal da Tela de Estoque ---
# Esta função constrói e controla a tela de "Gestão de Estoque".
def showgestaoestoque(app):
    """Exibe a tela de gestão de estoque."""

    # --- Preparação da Janela ---
    # Limpa a janela principal de qualquer widget existente antes de desenhar a nova tela.
    for w in app.winfo_children():
        w.destroy()

    # Cria um painel (Frame) no topo para o botão de navegação.
    # 'padding=8' adiciona um espaçamento interno para não ficar colado nas bordas.
    top = ttk.Frame(app, padding=8)
    # '.pack(fill="x")' faz o painel ocupar toda a largura da janela.
    top.pack(fill="x")

    # Cria o botão "Voltar" que, ao ser clicado, chama a função 'app.showmain' para retornar ao menu.
    ttk.Button(top, text="Voltar", command=app.showmain).pack(side="left")

    # --- Configuração da Tabela (Treeview) ---
    # Define os identificadores internos para cada coluna da tabela.
    cols = ("id", "nome", "quantidade", "estoque_minimo")
    # Cria um dicionário para mapear os identificadores aos títulos que o usuário verá.
    headers = {"id": "ID", "nome": "Nome", "quantidade": "Quantidade", "estoque_minimo": "Estoque Mínimo"}
    # Cria um dicionário para definir a largura em pixels de cada coluna.
    colwidths = {"id": 60, "nome": 250, "quantidade": 120, "estoque_minimo": 150}

    # Cria o widget 'Treeview', que funciona como uma tabela.
    # 'columns=cols' define quais colunas ele terá. 'show="headings"' oculta a primeira coluna fantasma.
    tree = ttk.Treeview(app, columns=cols, show="headings")
    # Laço para configurar cada coluna individualmente.
    for c in cols:
        # Define o texto do cabeçalho de cada coluna usando o dicionário 'headers'.
        tree.heading(c, text=headers[c])
        # Define a largura e o alinhamento do conteúdo de cada coluna. 'anchor="center"' centraliza o texto.
        tree.column(c, width=colwidths[c], anchor="center")

    # Adiciona a tabela à janela, permitindo que ela se expanda ('expand=True') e preencha o espaço ('fill="both"').
    tree.pack(expand=True, fill="both", padx=10, pady=8)

    # --- Carregamento dos Dados ---
    # Função interna para buscar os dados no banco e preencher a tabela.
    def loadcomidasordenadas():
        # Limpa todas as linhas existentes na tabela antes de carregar os novos dados.
        for it in tree.get_children():
            tree.delete(it)

        # Abre uma conexão segura com o banco de dados.
        with getconnection() as conn:
            # Executa uma consulta SQL para selecionar os campos necessários da tabela 'comidas'.
            cur = conn.execute("SELECT id, nome, quantidade, estoque_minimo FROM comidas")
            # Converte o resultado da consulta em uma lista de dicionários para facilitar a manipulação.
            rows = [dict(r) for r in cur.fetchall()]

        # Ordena a lista de comidas em ordem alfabética pelo nome, ignorando maiúsculas/minúsculas.
        for r in sorted(rows, key=lambda r: r["nome"].lower()):
            # Lógica para destacar produtos com estoque baixo.
            # Se a quantidade atual for menor ou igual ao estoque mínimo, a 'tag' será "baixo".
            tag = "baixo" if r["quantidade"] <= r["estoque_minimo"] else ""
            # Insere uma nova linha na tabela com os valores da comida.
            # A 'tag' definida acima é associada a esta linha.
            tree.insert("", "end", values=(r["id"], r["nome"], r["quantidade"], r["estoque_minimo"]), tags=(tag,))

        # Configura o estilo da tag "baixo": fundo vermelho e texto branco para chamar a atenção.
        tree.tag_configure("baixo", background="red", foreground="white")

    # Chama a função para carregar os dados na tabela assim que a tela é criada.
    loadcomidasordenadas()

    # --- Botões de Ação ---
    # Cria um painel na parte inferior da tela para os botões de ação.
    btns = ttk.Frame(app, padding=6)
    btns.pack(fill="x")

    # Botão para abrir a janela de registro de movimentação.
    # 'lambda' é usado para passar argumentos para a função chamada pelo botão.
    ttk.Button(btns, text="Registrar Movimentação", command=lambda: registrarmovimentacao(app, tree)).pack(side="left", padx=6)
    # Botão para abrir o histórico do item selecionado.
    ttk.Button(btns, text="Ver Histórico", command=lambda: verhistorico(tree)).pack(side="left", padx=6)

# --- Função para Registrar Movimentação ---
# Abre uma nova janela (formulário) para registrar entrada ou saída de um item.
def registrarmovimentacao(app, tree):
    # Obtém o item atualmente selecionado na tabela.
    sel = tree.selection()
    # Se nenhuma linha estiver selecionada, exibe um aviso e encerra a função.
    if not sel:
        messagebox.showinfo("Atenção", "Selecione uma comida para movimentar.")
        return

    # Pega o ID da comida, que está no primeiro valor ('values'[0]) da linha selecionada.
    cid = tree.item(sel[0])["values"][0]

    # Cria uma nova janela do tipo 'Toplevel', que fica acima da janela principal.
    win = tk.Toplevel(app)
    win.title("Registrar Movimentação")
    centralizarjanela(win, 400, 300)

    # --- Formulário de Movimentação ---
    # Rótulo "Tipo". 'sticky="e"' alinha o texto à direita.
    ttk.Label(win, text="Tipo").grid(column=0, row=0, sticky="e", padx=6, pady=4)
    # Caixa de seleção (Combobox) para escolher entre "entrada" e "saída". 'state="readonly"' impede digitação.
    tipocb = ttk.Combobox(win, values=["entrada", "saída"], state="readonly")
    tipocb.grid(column=1, row=0, padx=6, pady=4)
    tipocb.current(0)  # Deixa "entrada" como opção padrão.

    # Rótulo e campo de entrada para a "Quantidade".
    ttk.Label(win, text="Quantidade").grid(column=0, row=1, sticky="e", padx=6, pady=4)
    qtdent = ttk.Entry(win, width=20)
    qtdent.grid(column=1, row=1, padx=6, pady=4)

    # Rótulo e campo para a "Data".
    ttk.Label(win, text="Data (DD/MM/AAAA)").grid(column=0, row=2, sticky="e", padx=6, pady=4)
    dataent = ttk.Entry(win, width=20)
    dataent.grid(column=1, row=2, padx=6, pady=4)
    # Preenche o campo de data automaticamente com a data de hoje no formato brasileiro.
    dataent.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

    # Rótulo e campo para "Observação".
    ttk.Label(win, text="Observação").grid(column=0, row=3, sticky="e", padx=6, pady=4)
    noteent = ttk.Entry(win, width=40)
    noteent.grid(column=1, row=3, padx=6, pady=4)

    # --- Lógica para Salvar ---
    # Função interna que será chamada pelo botão "Salvar".
    def salvarmov():
        tipo = tipocb.get()
        # 'try-except' para validar a quantidade. Se o texto não puder ser convertido para inteiro, mostra um erro.
        try:
            qtd = int(qtdent.get())
        except:
            messagebox.showwarning("Validação", "Quantidade inválida.")
            return

        # 'try-except' para validar a data. Se o formato não for DD/MM/AAAA, mostra um erro.
        datatxt = dataent.get().strip()
        try:
            # Converte a data do formato brasileiro para o formato ISO (YYYY-MM-DD) para salvar no banco.
            dataiso = datetime.datetime.strptime(datatxt, "%d/%m/%Y").date().isoformat()
        except:
            messagebox.showwarning("Validação", "Data inválida. Use DD/MM/AAAA.")
            return

        # Abre a conexão com o banco para realizar as transações.
        with getconnection() as conn:
            # Busca os dados atuais da comida que está sendo movimentada.
            comida = conn.execute("SELECT * FROM comidas WHERE id=?", (cid,)).fetchone()
            if not comida:
                messagebox.showerror("Erro", "Comida não encontrada.")
                return

            # Calcula a nova quantidade em estoque. Soma se for "entrada", subtrai se for "saída".
            newq = comida["quantidade"] + qtd if tipo == "entrada" else comida["quantidade"] - qtd

            # Impede que o estoque fique negativo.
            if newq < 0:
                messagebox.showerror("Erro", "Quantidade insuficiente para esta saída.")
                return

            # 1ª Transação: Atualiza a quantidade na tabela 'comidas'.
            conn.execute("UPDATE comidas SET quantidade=? WHERE id=?", (newq, cid))

            # 2ª Transação: Insere um registro na tabela 'movimentacoes' para criar um histórico.
            conn.execute(
                "INSERT INTO movimentacoes (comida_id, usuario_id, tipo, quantidade, data, observacao) VALUES (?, ?, ?, ?, ?, ?)",
                (cid, app.currentuser["id"], tipo, qtd, dataiso, noteent.get().strip())
            )

            # Após a movimentação, verifica se o estoque ficou abaixo do mínimo e alerta o usuário.
            if newq <= comida["estoque_minimo"]:
                messagebox.showwarning("Estoque baixo", f"A comida '{comida['nome']}' está com quantidade {newq} (mínimo: {comida['estoque_minimo']}).")

        win.destroy()  # Fecha a janela do formulário.
        showgestaoestoque(app)  # Recarrega a tela de estoque para mostrar o valor atualizado.
        messagebox.showinfo("Sucesso", "Movimentação registrada.")  # Confirma o sucesso da operação.

    # Cria o botão "Salvar" no formulário de movimentação.
    ttk.Button(win, text="Salvar", command=salvarmov).grid(column=0, row=4, columnspan=2, pady=10)


# --- Função para Ver Histórico ---
# Abre uma nova janela para mostrar o histórico de movimentações de um item.
def verhistorico(tree):
    # Verifica se um item está selecionado na tabela.
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Atenção", "Selecione uma comida para ver o histórico.")
        return

    # Pega o ID da comida selecionada.
    cid = tree.item(sel[0])["values"][0]

    # Cria uma nova janela 'Toplevel' para exibir o histórico.
    win = tk.Toplevel()
    win.title("Histórico de Movimentações")
    centralizarjanela(win, 700, 400)

    # --- Tabela de Histórico ---
    # Define as colunas para a tabela de histórico.
    cols = ("id", "tipo", "quantidade", "data", "usuario", "observacao")
    tv = ttk.Treeview(win, columns=cols, show="headings")
    headers = {"id": "ID", "tipo": "Tipo", "quantidade": "Quantidade", "data": "Data", "usuario": "Usuário", "observacao": "Observação"}
    # Configura o cabeçalho e a largura de cada coluna.
    for c in cols:
        tv.heading(c, text=headers[c])
        tv.column(c, width=120, anchor="center")
    tv.pack(expand=True, fill="both", padx=10, pady=8)

    # --- Carregamento do Histórico ---
    # Abre a conexão para buscar os dados.
    with getconnection() as conn:
        # Consulta SQL avançada que junta ('JOIN') as tabelas 'movimentacoes' e 'usuarios'.
        # Isso é feito para que possamos mostrar o nome do usuário em vez do seu ID.
        # 'ORDER BY m.data DESC' mostra as movimentações mais recentes primeiro.
        cur = conn.execute("""
            SELECT m.id, m.tipo, m.quantidade, m.data, u.usuario AS usuario, m.observacao
            FROM movimentacoes m
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.comida_id = ?
            ORDER BY m.data DESC
        """, (cid,))
        # Percorre cada linha do resultado da consulta.
        for r in cur.fetchall():
            # Tenta formatar a data do formato do banco (YYYY-MM-DD) para o brasileiro (DD/MM/YYYY).
            try:
                databr = datetime.datetime.fromisoformat(r["data"]).strftime("%d/%m/%Y")
            except:
                databr = r["data"]  # Se falhar, mostra a data como está.
            # Insere a linha formatada na tabela de histórico.
            tv.insert("", "end", values=(r["id"], r["tipo"], r["quantidade"], databr, r["usuario"], r["observacao"]))
