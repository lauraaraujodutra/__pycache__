PRAGMA foreign_keys = ON;
-- Ativa a verificação de integridade referencial (chaves estrangeiras).

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único gerado automaticamente
    usuario TEXT UNIQUE,                   -- Nome de usuário único (login)
    senha TEXT,                           -- Senha do usuário (em texto simples aqui)
    nome_completo TEXT                    -- Nome completo do usuário
);

-- Tabela de comidas nordestinas
CREATE TABLE IF NOT EXISTS comidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    -- Identificador único da comida
    codigo TEXT UNIQUE,                       -- Código único do prato/comida
    nome TEXT,                               -- Nome da comida
    descricao TEXT,                          -- Descrição detalhada
    categoria TEXT,                          -- Categoria (ex: prato principal, salgado)
    origem TEXT,                             -- Origem regional da comida
    ingredientes TEXT,                       -- Ingredientes usados
    porcao TEXT,                            -- Porção sugerida (ex: 300g)
    calorias REAL,                          -- Quantidade de calorias
    quantidade INTEGER DEFAULT 0,           -- Quantidade atual em estoque (padrão 0)
    estoque_minimo INTEGER DEFAULT 0        -- Quantidade mínima para alerta (padrão 0)
);

-- Tabela de movimentações (histórico de estoque)
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único da movimentação
    comida_id INTEGER,                      -- ID da comida movimentada
    usuario_id INTEGER,                     -- ID do usuário que realizou movimentação
    tipo TEXT,                             -- Tipo de movimentação ("entrada" ou "saída")
    quantidade INTEGER,                    -- Quantidade movimentada
    data TEXT,                            -- Data da movimentação (formato texto)
    observacao TEXT,                      -- Observação adicional

    FOREIGN KEY(comida_id) REFERENCES comidas(id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

-- Inserção de usuários iniciais (sistema terá esses usuários cadastrados)
INSERT OR IGNORE INTO usuarios (id, usuario, senha, nome_completo) VALUES
(1, 'vendedor1', '123', 'Helena Silva'),
(2, 'vendedor2', '123', 'Cecilia Lima'),
(3, 'vendedor3', '123', 'Ravi Santos');

-- Inserção de comidas iniciais no sistema
INSERT OR IGNORE INTO comidas (id, codigo, nome, descricao, categoria, origem, ingredientes, porcao, calorias, quantidade, estoque_minimo) VALUES
(1, 'C001', 'Baião de Dois', 'Arroz com feijão verde, queijo coalho e carne seca.', 'Prato Principal', 'Ceará', 'Arroz, feijão, queijo coalho, carne seca', '300g', 480, 15, 3),
(2, 'C002', 'Sarapatel', 'Miúdos de porco cozidos com sangue.', 'Prato Principal', 'Pernambuco', 'Miúdos de porco, sangue, alho, cebola', '350g', 600, 10, 3),
(3, 'C003', 'Acarajé', 'Bolinho de feijão-fradinho frito no azeite de dendê.', 'Salgado', 'Bahia', 'Feijão-fradinho, camarão seco, azeite de dendê', '150g', 350, 20, 5);

-- Inserção de movimentações iniciais no estoque
INSERT OR IGNORE INTO movimentacoes (id, comida_id, usuario_id, tipo, quantidade, data, observacao) VALUES
(1, 1, 1, 'entrada', 5, '2025-09-01', 'Reposição estoque mensal Baião de Dois'),
(2, 2, 2, 'saída', 2, '2025-09-05', 'Venda Sarapatel para evento'),
(3, 3, 3, 'entrada', 10, '2025-09-10', 'Novo lote de Acarajé');
