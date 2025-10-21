# --- Bloco de Importações ---
# Importa as ferramentas necessárias para a interface gráfica e funcionalidades.

# Importa a biblioteca principal do tkinter para criar janelas e widgets.
import tkinter as tk
# Do tkinter, importa os widgets 'ttk' (com estilo moderno) e o 'messagebox' para exibir alertas.
from tkinter import ttk, messagebox

# Do nosso arquivo 'db.py', importa a função para obter uma conexão com o banco de dados.
from db import getconnection
# Do nosso arquivo 'utils.py', importa a função para centralizar janelas na tela.
from utils import centralizarjanela


# --- Função Principal da Tela de Comidas ---
# Esta função constrói e controla toda a tela de "Cadastro de Comidas".
def showcomidas(app):
    """Exibe a tela de gestão de comidas."""

    # --- Preparação da Janela ---
    # Limpa a janela principal de qualquer widget existente para desenhar a nova tela.
    for w in app.winfo_children():
        w.destroy()

    # --- Widgets do Topo (Navegação) ---
    # Cria um painel (Frame) no topo para os botões principais.
    top = ttk.Frame(app, padding=8)
    top.pack(fill="x")  # Ocupa toda a largura da janela.
    # Botão "Voltar" que chama a função 'app.showmain' para retornar ao menu.
    ttk.Button(top, text="Voltar", command=app.showmain).pack(side="left")
    # Botão "Nova Comida" que abre o formulário de cadastro.
    ttk.Button(top, text="Nova Comida", command=lambda: comidanova(app)).pack(side="right")

    # --- Widgets de Busca ---
    # Cria um painel específico para a funcionalidade de busca.
    searchframe = ttk.Frame(app, padding=6)
    searchframe.pack(fill="x")

    # Rótulo "Buscar".
    ttk.Label(searchframe, text="Buscar").pack(side="left")
    # Cria uma variável especial do tkinter ('StringVar') para vincular ao campo de texto.
    # Qualquer alteração na variável reflete no campo, e vice-versa.
    searchvar = tk.StringVar()
    # Cria o campo de entrada de texto para a busca.
    searchentry = ttk.Entry(searchframe, textvariable=searchvar, width=40)
    searchentry.pack(side="left", padx=6)
    # Botão "Buscar" que chama a função de carregar a lista, passando o termo digitado.
    ttk.Button(searchframe, text="Buscar", command=lambda: loadcomidastree(searchvar.get().strip())).pack(side="left", padx=4)
    # Botão "Limpar" que apaga o termo de busca e recarrega a lista completa.
    ttk.Button(searchframe, text="Limpar", command=lambda: searchvar.set("") or loadcomidastree("")).pack(side="left", padx=4)

    # --- Configuração da Tabela (Treeview) ---
    # Define os identificadores internos para cada coluna que a tabela exibirá.
    cols = ("id", "nome", "categoria", "origem", "porcao", "calorias", "quantidade", "estoque_minimo")

    # Cria o widget 'Treeview' (a tabela) com as colunas definidas.
    tree = ttk.Treeview(app, columns=cols, show="headings")

    # Dicionário que mapeia os identificadores das colunas para os textos dos cabeçalhos.
    headers = {
        "id": "ID", "nome": "Nome", "categoria": "Categoria", "origem": "Origem",
        "porcao": "Porção", "calorias": "Calorias", "quantidade": "Quantidade", "estoque_minimo": "Estoque Mínimo"
    }

    # Dicionário que define a largura em pixels para cada coluna.
    colwidths = {"id": 30, "nome": 160, "categoria": 80, "origem": 100, "porcao": 60, "calorias": 80, "quantidade": 80, "estoque_minimo": 100}

    # Laço para configurar cada coluna da tabela.
    for c in cols:
        # Define o texto do cabeçalho e o alinhamento (nome à esquerda, outros centralizados).
        tree.heading(c, text=headers[c], anchor="w" if c == "nome" else "center")
        # Define a largura da coluna e o alinhamento do conteúdo.
        tree.column(c, width=colwidths[c], anchor="w" if c == "nome" else "center")

    # Adiciona a tabela à janela, fazendo-a preencher todo o espaço disponível.
    tree.pack(expand=True, fill="both", padx=10, pady=8)

    # --- Lógica de Carregamento de Dados ---
    # Função interna para buscar os dados no banco e popular a tabela.
    def loadcomidastree(searchterm=""):
        # Limpa todas as linhas atuais da tabela antes de carregar as novas.
        for it in tree.get_children():
            tree.delete(it)

        # Abre uma conexão segura com o banco de dados.
        with getconnection() as conn:
            # Se um termo de busca foi fornecido...
            if searchterm:
                # Prepara o termo para uma busca 'LIKE' em SQL, que procura por partes do texto.
                q = f"%{searchterm}%"
                # Executa a busca na tabela 'comidas' onde o nome OU a descrição contenham o termo.
                cur = conn.execute("SELECT * FROM comidas WHERE nome LIKE ? OR descricao LIKE ?", (q, q))
            # Se não houver termo de busca...
            else:
                # Seleciona todas as comidas da tabela.
                cur = conn.execute("SELECT * FROM comidas")

            # Pega todos os resultados da consulta.
            rows = cur.fetchall()
            # Ordena os resultados em ordem alfabética pelo nome.
            for r in sorted(rows, key=lambda r: r["nome"].lower()):
                # Define uma 'tag' "baixo" se a quantidade estiver no limite ou abaixo do estoque mínimo.
                tag = "baixo" if r["quantidade"] <= r["estoque_minimo"] else ""
                # Insere a linha na tabela com os valores da comida e a tag, se aplicável.
                tree.insert(
                    "", "end",
                    values=(r["id"], r["nome"], r["categoria"], r["origem"], r["porcao"], r["calorias"], r["quantidade"], r["estoque_minimo"]),
                    tags=(tag,)
                )

            # Configura o estilo visual da tag "baixo" para ter fundo vermelho e texto branco.
            tree.tag_configure("baixo", background="red", foreground="white")

    # Chama a função para carregar os dados na tabela pela primeira vez, sem filtro de busca.
    loadcomidastree()

    # --- Botões de Ação Inferiores ---
    # Cria um painel na parte inferior para os botões de edição e exclusão.
    btns = ttk.Frame(app, padding=6)
    btns.pack(fill="x")
    # Botão "Editar" que chama a função de edição.
    ttk.Button(btns, text="Editar", command=lambda: comidaeditar(app, tree)).pack(side="left", padx=6)
    # Botão "Excluir" que chama a função de exclusão.
    ttk.Button(btns, text="Excluir", command=lambda: comidaexcluir(app, tree)).pack(side="left", padx=6)

# --- Funções de Ação (CRUD) ---

# Função chamada pelo botão "Nova Comida".
def comidanova(app):
    # Simplesmente abre o formulário de comidas em modo de criação (sem dados existentes).
    comidaform(app)

# Função chamada pelo botão "Editar".
def comidaeditar(app, tree):
    # Obtém o item selecionado na tabela.
    sel = tree.selection()
    if not sel:  # Se nada estiver selecionado, exibe um aviso.
        messagebox.showinfo("Atenção", "Selecione uma comida para editar.")
        return
    # Pega o ID da comida da primeira coluna da linha selecionada.
    cid = tree.item(sel[0])["values"][0]
    # Conecta ao banco e busca todos os dados da comida com aquele ID.
    with getconnection() as conn:
        row = conn.execute("SELECT * FROM comidas WHERE id=?", (cid,)).fetchone()
        if row:  # Se a comida foi encontrada...
            # Abre o formulário, passando os dados existentes para preencher os campos.
            comidaform(app, existing=row)

# Função chamada pelo botão "Excluir".
def comidaexcluir(app, tree):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Atenção", "Selecione uma comida para excluir.")
        return
    cid = tree.item(sel[0])["values"][0]
    # ANTES DE EXCLUIR, verifica se existem movimentações de estoque para esta comida.
    with getconnection() as conn:
        cur = conn.execute("SELECT COUNT(*) AS total FROM movimentacoes WHERE comida_id=?", (cid,))
        total = cur.fetchone()["total"]
        # Se houver movimentações, a exclusão é bloqueada para manter a integridade do histórico.
        if total > 0:
            messagebox.showwarning("Aviso", "Não é possível excluir! Existem movimentações registradas para esta comida.")
            return
    # Pede confirmação ao usuário antes de prosseguir com a exclusão.
    if messagebox.askyesno("Confirmar", "Deseja realmente excluir a comida selecionada?"):
        with getconnection() as conn:
            # Executa o comando SQL para remover a comida da tabela.
            conn.execute("DELETE FROM comidas WHERE id=?", (cid,))
        # Recarrega a tela de comidas para refletir a exclusão.
        showcomidas(app)

# --- Função do Formulário ---
# Esta função cria a janela de formulário para adicionar ou editar uma comida.
def comidaform(app, existing=None):
    # Cria uma nova janela 'Toplevel' que fica sobre a janela principal.
    win = tk.Toplevel(app)
    win.title("Comida Nordestina")
    centralizarjanela(win, 500, 550)

    # Lista com os nomes das colunas (campos) que estarão no formulário.
    labels = [
        "nome", "descricao", "categoria", "origem", "ingredientes", "porcao",
        "calorias", "quantidade", "estoque_minimo"
    ]

    # Dicionário para traduzir os nomes dos campos para rótulos em português.
    labelspt = {
        "nome": "Nome", "descricao": "Descrição", "categoria": "Categoria", "origem": "Origem", "ingredientes": "Ingredientes",
        "porcao": "Porção", "calorias": "Calorias", "quantidade": "Quantidade", "estoque_minimo": "Estoque Mínimo"
    }

    # Dicionário para armazenar os widgets de entrada de texto, para que possamos ler seus valores depois.
    fields = {}
    # Laço para criar dinamicamente um rótulo e um campo de entrada para cada item em 'labels'.
    for i, key in enumerate(labels):
        ttk.Label(win, text=labelspt[key]).grid(column=0, row=i, sticky="e", padx=6, pady=4)
        ent = ttk.Entry(win, width=40)
        ent.grid(column=1, row=i, padx=6, pady=4, sticky="we")
        fields[key] = ent  # Armazena o campo de entrada no dicionário.

        # Se 'existing' não for None (ou seja, estamos em modo de edição)...
        if existing:
            # Preenche o campo de entrada com o valor correspondente da comida existente.
            ent.insert(0, str(existing[key]) if existing[key] is not None else "")

    # --- Lógica para Salvar ---
    # Função interna que será chamada pelo botão "Salvar" do formulário.
    def save():
        # Coleta todos os dados digitados nos campos do formulário.
        data = {k: fields[k].get().strip() for k in labels}

        # Validação: verifica se o campo "Nome" foi preenchido.
        if not data["nome"]:
            messagebox.showwarning("Validação", "Nome obrigatório.")
            return

        # Validação: tenta converter os campos numéricos. Se falhar, exibe um erro.
        try:
            calorias = float(data["calorias"]) if data["calorias"] else 0.0
            quantidade = int(data["quantidade"]) if data["quantidade"] else 0
            estoque_minimo = int(data["estoque_minimo"]) if data["estoque_minimo"] else 0
        except:
            messagebox.showwarning("Validação", "Calorias, Quantidade ou Estoque mínimo inválidos.")
            return

        # Abre a conexão com o banco para salvar os dados.
        with getconnection() as conn:
            # Se estamos editando ('existing' tem dados)...
            if existing:
                # Executa um comando SQL 'UPDATE' para atualizar o registro existente.
                conn.execute("""
                    UPDATE comidas SET nome=?, descricao=?, categoria=?, origem=?, ingredientes=?, porcao=?, calorias=?, quantidade=?, estoque_minimo=? WHERE id=?
                """, (data["nome"], data["descricao"], data["categoria"], data["origem"], data["ingredientes"], data["porcao"], calorias, quantidade, estoque_minimo, existing["id"]))
            # Se não, estamos criando um novo registro...
            else:
                # Executa um comando SQL 'INSERT' para adicionar uma nova linha à tabela.
                conn.execute("""
                    INSERT INTO comidas (nome, descricao, categoria, origem, ingredientes, porcao, calorias, quantidade, estoque_minimo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (data["nome"], data["descricao"], data["categoria"], data["origem"], data["ingredientes"], data["porcao"], calorias, quantidade, estoque_minimo))

        win.destroy()  # Fecha a janela do formulário após salvar.
        showcomidas(app)  # Recarrega a lista na tela principal para mostrar as alterações.
        messagebox.showinfo("Sucesso", "Comida salva com sucesso.")

    # Cria o botão "Salvar" no final do formulário.
    ttk.Button(win, text="Salvar", command=save).grid(column=0, row=len(labels), columnspan=2, pady=10)
