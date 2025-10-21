# --- Bloco de Importações ---
# Importa as bibliotecas necessárias para as funcionalidades deste módulo.

# Importa o módulo 'tkinter' para acessar funcionalidades da interface gráfica, se necessário.
# Embora não seja usado diretamente nas funções, é uma boa prática mantê-lo por consistência.
import tkinter as tk

# Do nosso arquivo 'db.py', importa a função 'getconnection' para obter acesso ao banco de dados.
from db import getconnection

# --- Função para Gerar Código de Produto (Não utilizada no código atual, mas útil) ---
# Esta função foi projetada para criar um código único para cada nova comida (ex: C001, C002).
# No momento, o sistema usa o ID numérico, mas esta função fica como uma alternativa.
def gerarcodigo():
    """Gera um código sequencial para novos cadastros de comida."""
    # Abre uma conexão segura com o banco de dados.
    with getconnection() as conn:
        # Executa uma consulta SQL para encontrar o maior 'id' na tabela 'comidas'.
        # 'ORDER BY id DESC' ordena do maior para o menor, 'LIMIT 1' pega apenas o primeiro resultado.
        cur = conn.execute("SELECT id FROM comidas ORDER BY id DESC LIMIT 1")
        # Pega a primeira linha do resultado da consulta.
        row = cur.fetchone()
        # Se 'row' for None, significa que a tabela está vazia.
        if not row:
            # Retorna o primeiro código da sequência.
            return "C001"
        # Se a tabela não está vazia, pega o último 'id', soma 1, e formata o novo código.
        # f"C{...:03d}" formata o número para ter sempre 3 dígitos, preenchendo com zeros à esquerda (ex: 5 -> 005).
        return f"C{row['id']+1:03d}"

# --- Função de Ordenação (Não utilizada no código atual, mas útil) ---
# Esta função implementa o 'mergesort', um algoritmo de ordenação eficiente.
# Ela foi criada como uma alternativa para ordenar listas de produtos, embora o código atual use 'sorted()'.
def mergesortproducts(products, key="nome"):
    """
    Ordena uma lista de comidas (dicionários) por uma chave específica (padrão é "nome").
    Usa o algoritmo mergesort, que é eficiente e estável.
    """
    # Caso base da recursão: uma lista com 0 ou 1 elemento já está ordenada.
    if len(products) <= 1:
        return products

    # Encontra o meio da lista para dividi-la em duas metades.
    mid = len(products) // 2
    # Chama a própria função recursivamente para ordenar a metade da esquerda.
    left = mergesortproducts(products[:mid], key)
    # Chama a própria função recursivamente para ordenar a metade da direita.
    right = mergesortproducts(products[mid:], key)

    # Lista vazia que irá armazenar o resultado da fusão (merge) das duas metades ordenadas.
    merged = []
    # Inicializa os ponteiros para percorrer as listas 'left' e 'right'.
    i = j = 0
    # Loop para comparar os elementos das duas metades e adicioná-los à lista 'merged' em ordem.
    while i < len(left) and j < len(right):
        # Compara os valores da 'key' (ex: "nome"), convertendo para minúsculas para não diferenciar maiúsculas.
        if str(left[i][key]).lower() < str(right[j][key]).lower():
            # Se o elemento da esquerda for menor, adiciona-o à lista final.
            merged.append(left[i])
            i += 1  # Avança o ponteiro da lista esquerda.
        else:
            # Caso contrário, adiciona o elemento da direita.
            merged.append(right[j])
            j += 1  # Avança o ponteiro da lista direita.
    # Após o loop, uma das listas pode ainda ter elementos restantes.
    # Adiciona todos os elementos restantes da lista esquerda (se houver).
    merged.extend(left[i:])
    # Adiciona todos os elementos restantes da lista direita (se houver).
    merged.extend(right[j:])
    # Retorna a lista final, completamente ordenada.
    return merged

# --- Função para Centralizar Janelas ---
# Uma função muito útil para garantir que todas as janelas (principal, formulários, etc.)
# apareçam no centro da tela do usuário, melhorando a experiência de uso.
def centralizarjanela(win, largura=800, altura=600):
    """Centraliza uma janela Tkinter na tela do monitor."""
    # Garante que as dimensões da janela ('win') estejam calculadas e prontas para uso.
    win.update_idletasks()
    # Pega a largura total em pixels da tela do monitor.
    screenw = win.winfo_screenwidth()
    # Pega a altura total em pixels da tela do monitor.
    screenh = win.winfo_screenheight()
    # Calcula a coordenada X (horizontal) para o canto superior esquerdo da janela.
    # Pega o centro da tela (screenw // 2) e subtrai metade da largura da janela (largura // 2).
    x = screenw // 2 - largura // 2
    # Calcula a coordenada Y (vertical) para o canto superior esquerdo da janela.
    y = screenh // 2 - altura // 2
    # Define a geometria da janela usando um formato de string especial: "larguraxaltura+x+y".
    win.geometry(f"{largura}x{altura}+{x}+{y}")
