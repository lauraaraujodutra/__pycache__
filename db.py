# --- Bloco de Importações ---
# Importa as bibliotecas necessárias para interagir com o banco de dados e o sistema de arquivos.

# Importa o módulo 'sqlite3', que é a biblioteca padrão do Python para trabalhar com bancos de dados SQLite.
import sqlite3
# Importa o módulo 'os', que permite interagir com o sistema operacional, como verificar se um arquivo existe.
import os

# --- Constante de Configuração ---
# Define o nome do arquivo que será usado para o banco de dados.
# Usar uma constante torna o código mais limpo e fácil de manter.
DBFILENAME = "comidasdb.sqlite"

# --- Função para Obter Conexão ---
# Esta função é a "porta de entrada" para o banco de dados.
# Toda vez que o programa precisar ler ou escrever dados, ele chamará esta função.
def getconnection():
    """Abre uma conexão com o banco de dados SQLite."""

    # Cria ou abre uma conexão com o arquivo de banco de dados especificado em DBFILENAME.
    conn = sqlite3.connect(DBFILENAME)

    # Configuração muito importante: muda a forma como os resultados das consultas são retornados.
    # Em vez de tuplas (ex: (1, 'Baião')), os resultados virão como objetos 'Row',
    # que funcionam como dicionários (ex: {'id': 1, 'nome': 'Baião'}), facilitando o acesso aos dados por nome de coluna.
    conn.row_factory = sqlite3.Row

    # Executa um comando PRAGMA no SQLite para garantir que as regras de chave estrangeira sejam sempre aplicadas.
    # Isso é crucial para manter a integridade dos dados (ex: não permitir uma movimentação para uma comida que não existe).
    conn.execute("PRAGMA foreign_keys = ON")

    # Retorna o objeto de conexão, que será usado para executar comandos SQL.
    return conn

# --- Função para Garantir a Existência do Banco ---
# Esta função é chamada uma única vez, no início da aplicação.
# Ela verifica se o banco de dados já foi criado. Se não, ela o cria.
def ensuredb():
    """
    Garante que o banco de dados exista.
    Se não existir, o cria executando o script do arquivo db_init.sql.
    """

    # Usa o módulo 'os' para verificar se o arquivo definido em DBFILENAME já existe no diretório.
    if not os.path.exists(DBFILENAME):
        # Se o arquivo não existe, significa que é a primeira vez que o programa está rodando.

        # Constrói o caminho completo para o arquivo 'db_init.sql'.
        # Isso garante que o programa encontre o arquivo, não importa de onde ele seja executado.
        scriptpath = os.path.join(os.path.dirname(__file__), "db_init.sql")

        # Verifica se o arquivo de script SQL realmente existe no caminho esperado.
        if os.path.exists(scriptpath):
            # Se o script existe, o banco de dados será criado e populado.

            # Obtém uma conexão com o banco (que será criado neste momento).
            # O 'with' garante que a conexão será fechada automaticamente no final.
            with getconnection() as conn:
                # Abre o arquivo 'db_init.sql' para leitura. 'encoding="utf-8"' garante compatibilidade.
                with open(scriptpath, "r", encoding="utf-8") as f:
                    # 'executescript()' lê todo o conteúdo do arquivo e executa todos os comandos SQL de uma só vez.
                    # É isso que cria as tabelas e insere os dados iniciais.
                    conn.executescript(f.read())
        else:
            # Se o arquivo 'db_init.sql' não for encontrado, o programa não pode continuar.
            # Lança um erro claro e informativo para o usuário/desenvolvedor.
            raise FileNotFoundError("db_init.sql não encontrado. Coloque db_init.sql na mesma pasta.")
