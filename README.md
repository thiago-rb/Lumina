# Lumína - Sistema de Gerenciamento Escolar

Sistema completo de gerenciamento escolar desenvolvido em Python/Flask com arquitetura de microserviços, monitoramento e containerização.

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Documentação da API](#documentação-da-api)
- [Monitoramento](#monitoramento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Banco de Dados](#banco-de-dados)
- [Logs](#logs)
- [Contribuição](#contribuição)

## Visão Geral

O **Lumína** é um sistema de gerenciamento escolar completo que permite administrar alunos, professores, turmas, presenças, atividades e pagamentos. O sistema foi desenvolvido com foco em escalabilidade, monitoramento e facilidade de manutenção.

### Principais Características:
- **API RESTful** completa com documentação Swagger
- **Containerização** com Docker e Docker Compose
- **Monitoramento** integrado com Prometheus e Grafana
- **Logs estruturados** para auditoria
- **Banco de dados PostgreSQL** com dados iniciais
- **Arquitetura modular** com blueprints Flask

## Arquitetura

### Arquitetura do Backend

O backend foi desenvolvido seguindo os princípios de arquitetura em camadas e padrão MVC adaptado para APIs REST:

**Camada de Apresentação (API Layer):**
- **Flask Application** (`app.py`): Ponto de entrada da aplicação
- **Blueprints** (`routes/`): Organização modular das rotas por entidade
- **Swagger/Flasgger**: Documentação automática da API

**Camada de Negócio (Business Layer):**
- **CRUD Operations**: Lógica de negócio implementada em cada rota
- **Validação de Dados**: Tratamento e validação de entrada
- **Log System**: Sistema de auditoria e monitoramento

**Camada de Dados (Data Layer):**
- **Database Connection** (`db.py`): Gerenciamento de conexões PostgreSQL
- **SQL Queries**: Operações diretas no banco de dados
- **Transaction Management**: Controle de transações

### Arquitetura de Microserviços

O sistema utiliza uma arquitetura de microserviços containerizada:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Flask     │    │   PostgreSQL    │
│   (Futuro)      │◄──►│   (Port 5000)   │◄──►│   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Grafana       │◄──►│   Prometheus    │◄──►│ Postgres        │
│   (Port 3000)   │    │   (Port 9090)   │    │ Exporter        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Funcionalidades

### Gestão de Alunos
- Cadastro completo com dados pessoais e responsáveis
- Vinculação a turmas
- Histórico de atividades
- Controle de presenças

### Gestão de Professores
- Cadastro de professores
- Vinculação a turmas
- Controle de acesso ao sistema

### Gestão de Turmas
- Criação e gerenciamento de turmas
- Definição de horários
- Associação com professores

### Controle Financeiro
- Registro de pagamentos
- Diferentes formas de pagamento
- Status de pagamento (Pago/Pendente)
- Referências (mensalidade, material, etc.)

### Controle de Presença
- Registro diário de presenças
- Relatórios de frequência

### Gestão de Atividades
- Cadastro de atividades realizadas
- Vinculação de alunos às atividades
- Histórico de participação

### Sistema de Usuários
- Controle de acesso
- Níveis de permissão (admin/professor)
- Autenticação segura

## Tecnologias

### Backend
- **Python 3.9**
- **Flask 2.2.3** - Framework web
- **PostgreSQL** - Banco de dados
- **psycopg2** - Driver PostgreSQL
- **Flasgger** - Documentação Swagger automática

### DevOps & Monitoramento
- **Docker & Docker Compose** - Containerização
- **Prometheus** - Coleta de métricas
- **Grafana** - Visualização de dados
- **Postgres Exporter** - Métricas do banco

### Desenvolvimento
- **pytest** - Testes automatizados
- **Logging** - Sistema de logs estruturado

## Pré-requisitos

- **Docker** (versão 20.0+)
- **Docker Compose** (versão 2.0+)
- **Git**

## Instalação e Execução

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd Lumína
```

### 2. Execute com Docker Compose
```bash
# Inicia todos os serviços (backend Python na pasta APP)
docker-compose up -d

# Para ver os logs em tempo real
docker-compose logs -f

# Para parar todos os serviços
docker-compose down
```

### 3. Executar Backend Python Diretamente
```bash
# Navegar para a pasta APP (requisito de entrega)
cd APP

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação Python
python app.py

# A API estará disponível em http://localhost:5000
```

### 4. Verificar Serviços
Após a execução, os seguintes serviços estarão disponíveis:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| API Principal | http://localhost:5000 | API REST do sistema |
| Documentação Swagger | http://localhost:5000/apidocs | Documentação interativa da API |
| Grafana | http://localhost:3000 | Dashboard de monitoramento |
| Prometheus | http://localhost:9090 | Métricas do sistema |
| PostgreSQL | localhost:5432 | Banco de dados |

### 5. Credenciais Padrão

**Banco de dados:**
- Host: localhost
- Port: 5432
- Database: escola
- User: postgres
- Password: postgres

**Grafana:**
- URL: http://localhost:3000
- User: admin
- Password: admin (será solicitado para alterar no primeiro acesso)

## Documentação da API

A API possui documentação completa gerada automaticamente com Swagger. Acesse:

**http://localhost:5000/apidocs**

### Principais Endpoints:

#### Alunos
- `GET /alunos/aluno` - Listar todos os alunos
- `POST /alunos/` - Criar novo aluno
- `PUT /alunos/{id}` - Atualizar aluno
- `DELETE /alunos/{id}` - Excluir aluno

#### Turmas
- `GET /turmas/` - Listar turmas
- `POST /turmas/` - Criar turma
- `PUT /turmas/{id}` - Atualizar turma
- `DELETE /turmas/{id}` - Excluir turma

#### Professores
- `GET /professores/` - Listar professores
- `POST /professores/` - Criar professor
- `PUT /professores/{id}` - Atualizar professor
- `DELETE /professores/{id}` - Excluir professor

#### Pagamentos
- `GET /pagamentos/` - Listar pagamentos
- `POST /pagamentos/` - Registrar pagamento
- `PUT /pagamentos/{id}` - Atualizar pagamento
- `DELETE /pagamentos/{id}` - Excluir pagamento

#### Presenças
- `GET /presencas/` - Listar presenças
- `POST /presencas/` - Registrar presença
- `PUT /presencas/{id}` - Atualizar presença
- `DELETE /presencas/{id}` - Excluir presença

#### Atividades
- `GET /atividades/` - Listar atividades
- `POST /atividades/` - Criar atividade
- `PUT /atividades/{id}` - Atualizar atividade
- `DELETE /atividades/{id}` - Excluir atividade

#### Usuários
- `GET /usuarios/` - Listar usuários
- `POST /usuarios/` - Criar usuário
- `PUT /usuarios/{id}` - Atualizar usuário
- `DELETE /usuarios/{id}` - Excluir usuário

### Exemplo de Requisição (Criar Aluno):
```json
POST /alunos/
{
  "nome_completo": "João Silva",
  "data_nascimento": "2010-05-22",
  "id_turma": 1,
  "nome_responsavel": "Maria Silva",
  "telefone_responsavel": "11987654322",
  "email_responsavel": "maria.silva@gmail.com",
  "informacoes_adicionais": "Sem alergias"
}
```

## Monitoramento

### Prometheus
- **URL**: http://localhost:9090
- **Métricas disponíveis**: Métricas do PostgreSQL, sistema operacional
- **Configuração**: `prometheus.yml`

### Grafana
- **URL**: http://localhost:3000
- **Dashboards**: Visualização de métricas do banco de dados
- **Data Source**: Prometheus (http://prometheus:9090)

### Configuração do Grafana:
1. Acesse http://localhost:3000
2. Login: admin/admin
3. Adicione Data Source: Prometheus (http://prometheus:9090)
4. Importe dashboards para PostgreSQL

## Estrutura do Projeto

```
Lumína/
├── APP/                          # Backend Python (Requisito de Entrega)
│   ├── routes/                   # Rotas organizadas por módulo
│   │   ├── aluno.py             # CRUD de alunos
│   │   ├── atividade_aluno.py   # Relacionamento atividade-aluno
│   │   ├── atividade.py         # CRUD de atividades
│   │   ├── pagamento.py         # CRUD de pagamentos
│   │   ├── presenca.py          # CRUD de presenças
│   │   ├── professor.py         # CRUD de professores
│   │   ├── turma.py             # CRUD de turmas
│   │   └── usuario.py           # CRUD de usuários
│   ├── app.py                   # Aplicação principal Flask
│   ├── db.py                    # Configuração do banco
│   ├── log_config.py            # Configuração de logs
│   ├── Dockerfile               # Container da API
│   ├── requirements.txt         # Dependências Python
│   └── test_app.py             # Testes automatizados
├── db/                          # Configuração do banco
│   ├── Dockerfile              # Container PostgreSQL customizado
│   └── init.sql                # Script de inicialização do BD
├── Documentos/                  # Documentação
│   └── MER Sistema escolar.pdf  # Modelo Entidade-Relacionamento
├── docker-compose.yml           # Orquestração dos containers
├── log_config.py               # Configuração de logs
├── prometheus.yml              # Configuração do Prometheus
└── README.md                   # Este arquivo
```

## Banco de Dados

### Modelo de Dados

O sistema utiliza PostgreSQL com as seguintes tabelas principais:

#### Tabelas:
- **Aluno**: Dados dos estudantes e responsáveis
- **Professor**: Informações dos educadores
- **Turma**: Classes e horários
- **Pagamento**: Controle financeiro
- **Presenca**: Registro de frequência
- **Atividade**: Atividades realizadas
- **Atividade_Aluno**: Relacionamento N:N entre atividades e alunos
- **Usuario**: Controle de acesso ao sistema

#### Relacionamentos:
- Aluno ↔ Turma (N:1)
- Professor ↔ Turma (1:N)
- Aluno ↔ Pagamento (1:N)
- Aluno ↔ Presenca (1:N)
- Aluno ↔ Atividade (N:N através de Atividade_Aluno)
- Professor ↔ Usuario (1:1 opcional)

### Dados Iniciais
O banco é inicializado com dados de exemplo:
- 2 professores
- 2 turmas
- 2 alunos
- Registros de pagamento, presença e atividades

## Logs

O sistema gera logs estruturados em `escola_infantil.log` com:
- **Operações CRUD**: CREATE, READ, UPDATE, DELETE
- **Erros e exceções**
- **Timestamp** de todas as operações
- **Detalhes** das operações realizadas

### Exemplo de Log:
```
2025-01-27 10:30:15,123 - INFO - CREATE: Aluno João Silva criado com sucesso. ID: 3
2025-01-27 10:31:22,456 - INFO - READ: Listagem de 3 alunos realizada.
2025-01-27 10:32:10,789 - ERROR - DELETE: Erro ao excluir aluno 999 - Aluno não encontrado.
```

## Testes

Execute os testes automatizados:

```bash
# Dentro do container da API
docker-compose exec api pytest test_app.py -v

# Ou localmente (se tiver Python configurado)
cd api
pytest test_app.py -v
```

## Desenvolvimento

### Executar em Modo de Desenvolvimento:
```bash
# Para desenvolvimento local (sem Docker)
cd api
pip install -r requirements.txt
python app.py
```

### Variáveis de Ambiente:
```bash
DB_HOST=localhost      # Host do banco
DB_NAME=escola         # Nome do banco
DB_USER=postgres       # Usuário do banco
DB_PASSWORD=postgres   # Senha do banco
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Suporte

Para dúvidas ou suporte:
- Abra uma issue no repositório
- Consulte a documentação da API em `/apidocs`
- Verifique os logs do sistema

---

**Desenvolvido para facilitar a gestão escolar**