-- ========================
-- Tabela Aluno
-- ========================
-- Armazena informações dos alunos, incluindo dados pessoais, turma associada e contato dos responsáveis.
CREATE TABLE aluno (
    id_aluno SERIAL PRIMARY KEY,  -- Identificador único do aluno
    nome_completo VARCHAR(255) NOT NULL,      -- Nome completo do aluno
    data_nascimento DATE NOT NULL,            -- Data de nascimento
    id_turma INT,                             -- Turma onde o aluno está matriculado (FK)
    nome_responsavel VARCHAR(255) NOT NULL,   -- Nome do responsável legal
    telefone_responsavel VARCHAR(20) NOT NULL,-- Telefone de contato do responsável
    email_responsavel VARCHAR(100) NOT NULL,  -- E-mail do responsável
    informacoes_adicionais TEXT,              -- Informações extras sobre o aluno
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma) -- Relacionamento com a turma
);

-- ========================
-- Tabela Turma
-- ========================
-- Registra as turmas disponíveis na escola e os professores responsáveis por elas.
CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,  -- Identificador único da turma
    nome_turma VARCHAR(50) NOT NULL,          -- Nome da turma
    id_professor INT,                         -- Professor responsável pela turma (FK)
    horario VARCHAR(100) NOT NULL,            -- Horário das aulas
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor) -- Relacionamento com o professor
);

-- ========================
-- Tabela Professor
-- ========================
-- Registra informações dos professores da instituição.
CREATE TABLE professor (
    id_professor SERIAL PRIMARY KEY, -- Identificador único do professor
    nome_completo VARCHAR(255) NOT NULL,         -- Nome completo do professor
    email VARCHAR(100) NOT NULL,                 -- E-mail de contato
    telefone VARCHAR(20) NOT NULL                -- Telefone de contato
);

-- ========================
-- Tabela Pagamento
-- ========================
-- Controla os pagamentos realizados pelos alunos, incluindo valores e formas de pagamento.
CREATE TABLE pagamento (
    id_pagamento SERIAL PRIMARY KEY, -- Identificador único do pagamento
    id_aluno INT NOT NULL,                       -- Relacionamento com aluno (FK)
    data_pagamento DATE NOT NULL,                -- Data do pagamento
    valor_pago DECIMAL(10,2) NOT NULL,           -- Valor pago
    forma_pagamento VARCHAR(50) NOT NULL,        -- Forma de pagamento (cartão, boleto, etc.)
    referencia VARCHAR(100),                     -- Referência do pagamento (mensalidade, material)
    status VARCHAR(20) NOT NULL,                 -- Status do pagamento (Pago/Pendente)
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- Relacionamento com aluno
);

-- ========================
-- Tabela Presenca
-- ========================
-- Registra a presença dos alunos diariamente.
CREATE TABLE presenca (
    id_presenca SERIAL PRIMARY KEY, -- Identificador único do registro de presença
    id_aluno INT,                               -- Relacionamento com aluno (FK)
    data_presenca DATE NOT NULL,                -- Data da aula
    presente BOOLEAN NOT NULL,                  -- Indica se o aluno esteve presente (true/false)
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- Relacionamento com aluno
);

-- ========================
-- Tabela Atividade
-- ========================
-- Guarda atividades realizadas pelos alunos durante o período escolar.
CREATE TABLE atividade (
    id_atividade SERIAL PRIMARY KEY, -- Identificador único da atividade
    descricao TEXT NOT NULL,                     -- Descrição da atividade
    data_realizacao DATE NOT NULL                -- Data em que a atividade foi realizada
);

-- ========================
-- Tabela Atividade_Aluno
-- ========================
-- Relaciona os alunos às atividades que realizaram (muitos-para-muitos).
CREATE TABLE atividade_aluno (
    id_atividade INT,  -- Relacionamento com a atividade (FK)
    id_aluno INT,      -- Relacionamento com aluno (FK)
    PRIMARY KEY (id_atividade, id_aluno), -- Chave primária composta
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade), -- Relacionamento com Atividade
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- Relacionamento com Aluno
);

-- ========================
-- Tabela Usuario
-- ========================
-- Registra os usuários do sistema (administradores, professores).
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,  -- Identificador único do usuário
    login VARCHAR(50) UNIQUE NOT NULL,          -- Nome de usuário
    senha VARCHAR(255) NOT NULL,                -- Senha do usuário (criptografada)
    nivel_acesso VARCHAR(20),                   -- Define nível de acesso (admin/professor)
    id_professor INT,                           -- Relacionamento opcional com professor (FK)
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor) -- Relacionamento com professor
);

-- ========================
-- Inserção de dados iniciais
-- ========================

INSERT INTO professor (nome_completo, email, telefone) VALUES
('Ana Souza', 'ana.souza@escola.com', '11987654321'),
('Carlos Pereira', 'carlos.pereira@escola.com', '11912345678');

INSERT INTO turma (nome_turma, id_professor, horario) VALUES
('Turma A', 1, '08:00 - 12:00'),
('Turma B', 2, '13:00 - 17:00');

INSERT INTO aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais) VALUES
('João Silva', '2010-05-22', 1, 'Maria Silva', '11987654322', 'maria.silva@gmail.com', 'Sem alergias'),
('Luiza Almeida', '2011-08-15', 2, 'Pedro Almeida', '11912345679', 'pedro.almeida@gmail.com', NULL);

INSERT INTO pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES
(1, '2025-03-15', 500.00, 'Cartão', 'Mensalidade Março', 'Pago'),
(2, '2025-03-16', 500.00, 'Boleto', 'Mensalidade Março', 'Pendente');

INSERT INTO presenca (id_aluno, data_presenca, presente) VALUES
(1, '2025-03-20', TRUE),
(2, '2025-03-20', FALSE);

INSERT INTO atividade (descricao, data_realizacao) VALUES
('Pintura de paisagens', '2025-03-25'),
('Montagem de quebra-cabeça', '2025-03-26');

INSERT INTO atividade_aluno (id_atividade, id_aluno) VALUES
(1, 1),
(2, 2);

INSERT INTO usuario (login, senha, nivel_acesso, id_professor) VALUES
('admin', 'hash_senha_admin', 'administrador', NULL),
('carlos.professor', 'hash_senha_carlos', 'professor', 2);