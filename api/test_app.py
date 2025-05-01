import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Testes para Aluno
@patch('routes.aluno.connect_db')
def test_listar_alunos(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.fetchall.return_value = [
        (1, "João Silva", "2010-05-22", 1, "Maria Silva", "11987654322", "maria.silva@gmail.com", "Sem alergias")
    ]
    response = client.get('/alunos/')
    assert response.status_code == 200
    assert len(response.json) == 1

@patch('routes.aluno.connect_db')
def test_criar_aluno(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.rowcount = 1
    response = client.post('/alunos/', json={
        "nome_completo": "Maria Oliveira",
        "data_nascimento": "2010-08-15",
        "id_turma": 1,
        "nome_responsavel": "Ana Oliveira",
        "telefone_responsavel": "11987654321",
        "email_responsavel": "ana.oliveira@gmail.com",
        "informacoes_adicionais": "Sem alergias"
    })
    assert response.status_code == 201
    assert response.json['message'] == "Aluno criado com sucesso!"

@patch('routes.aluno.connect_db')
def test_atualizar_aluno(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.rowcount = 1
    response = client.put('/alunos/1', json={
        "nome_completo": "João Silva Atualizado",
        "data_nascimento": "2010-05-22",
        "id_turma": 2,
        "nome_responsavel": "Maria Silva",
        "telefone_responsavel": "11987654322",
        "email_responsavel": "maria.silva@gmail.com",
        "informacoes_adicionais": "Atualizado"
    })
    assert response.status_code == 200
    assert response.json['message'] == "Aluno atualizado com sucesso!"

@patch('routes.aluno.connect_db')
def test_excluir_aluno(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.rowcount = 1
    response = client.delete('/alunos/1')
    assert response.status_code == 200
    assert response.json['message'] == "Aluno excluído com sucesso!"

# Testes para Turma
@patch('routes.turma.connect_db')
def test_listar_turmas(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.fetchall.return_value = [
        (1, "Turma A", 1, "08:00 - 12:00")
    ]
    response = client.get('/turmas/')
    assert response.status_code == 200
    assert len(response.json) == 1

# Outros testes (Turma, Professor, Pagamento, etc.)
# Repita os mesmos padrões acima para as entidades restantes:
# - Criação (`POST`)
# - Atualização (`PUT`)
# - Exclusão (`DELETE`)

@patch('routes.usuario.connect_db')
def test_listar_usuarios(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.fetchall.return_value = [
        (1, "admin", "hashed_password", "administrador", None)
    ]
    response = client.get('/usuarios/')
    assert response.status_code == 200
    assert len(response.json) == 1

@patch('routes.usuario.connect_db')
def test_criar_usuario(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.rowcount = 1
    response = client.post('/usuarios/', json={
        "login": "novo_usuario",
        "senha": "nova_senha",
        "nivel_acesso": "professor",
        "id_professor": 1
    })
    assert response.status_code == 201
    assert response.json['message'] == "Usuário criado com sucesso!"

@patch('routes.usuario.connect_db')
def test_excluir_usuario(mock_connect_db, client):
    mock_connect_db.return_value.cursor.return_value.rowcount = 1
    response = client.delete('/usuarios/1')
    assert response.status_code == 200
    assert response.json['message'] == "Usuário excluído com sucesso!"