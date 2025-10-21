# Controle de Estoque de Comidas Nordestinas

Este é um sistema desenvolvido em Python utilizando a biblioteca Tkinter para interface gráfica. O sistema tem como objetivo a gestão de entradas, saídas e cadastro de comidas típicas da região nordestina do Brasil.

## Funcionalidades

- Login de usuários: permite que diferentes usuários acessem o sistema com autenticação.
- Cadastro, consulta, edição e exclusão de comidas típicas da culinária nordestina.
- Registro e histórico detalhado das movimentações no estoque (entradas e saídas).
- Alertas visuais para avisar quando o estoque de um alimento está abaixo do nível mínimo definido.

## Execução

1. Execute o arquivo `db_init.sql` para criar o banco de dados com suas tabelas e dados iniciais, ou deixe o sistema criar automaticamente no primeiro uso.
2. Execute o arquivo `main.py` para iniciar o sistema e acessar a interface gráfica.

## Estrutura de arquivos

- `main.py` : Arquivo principal que inicializa o sistema e gerencia as telas principais.
- `db.py` : Responsável pela conexão e inicialização do banco de dados SQLite.
- `login.py` : Tela e lógica de autenticação dos usuários.
- `comidas.py` : Cadastro, edição, exclusão e exibição das comidas típicas.
- `estoque.py` : Gestão das quantidades no estoque e registro das movimentações.
- `utils.py` : Funções auxiliares diversas, como centralização de janelas e ordenação.
- `db_init.sql` : Script SQL para criação do banco de dados com tabelas e dados iniciais.
- `README.md` : Este arquivo, com orientações e informações gerais sobre o sistema.

**Requisitos:** Python 3.12 ou superior, Tkinter e SQLite.
