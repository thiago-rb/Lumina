from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db
from log_config import logger  # Importando configuração de logs

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar alunos",
    "description": "Retorna todos os alunos cadastrados na escola.",
    "tags": ["Aluno"],
    "responses": {
        200: {
            "description": "Lista de alunos cadastrados.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_aluno": {"type": "integer"},
                        "nome_completo": {"type": "string"},
                        "data_nascimento": {"type": "string", "format": "date"},
                        "id_turma": {"type": "integer"},
                        "nome_responsavel": {"type": "string"},
                        "telefone_responsavel": {"type": "string"},
                        "email_responsavel": {"type": "string"},
                        "informacoes_adicionais": {"type": "string"}
                    }
                }
            }
        }
    }
})
def listar_alunos():
    """Endpoint que retorna todos os alunos cadastrados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aluno")
        alunos = cursor.fetchall()
        logger.info(f"READ: Listagem de {len(alunos)} alunos realizada.")
    except Exception as e:
        logger.error(f"READ: Erro ao listar alunos - {str(e)}")
        return jsonify({"error": f"Erro ao listar alunos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {
            "id_aluno": row[0],
            "nome_completo": row[1], 
            "data_nascimento": str(row[2]),
            "id_turma": row[3],
            "nome_responsavel": row[4],
            "telefone_responsavel": row[5],
            "email_responsavel": row[6],
            "informacoes_adicionais": row[7]
        } for row in alunos
    ])

@aluno_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar aluno",
    "description": "Cria um novo aluno na escola.",
    "tags": ["Aluno"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "nome_completo": {"type": "string"},
                    "data_nascimento": {"type": "string", "format": "date"},
                    "id_turma": {"type": "integer"},
                    "nome_responsavel": {"type": "string"},
                    "telefone_responsavel": {"type": "string"},
                    "email_responsavel": {"type": "string"},
                    "informacoes_adicionais": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Aluno criado com sucesso!"},
        400: {"description": "Erro ao criar aluno."}
    }
})
def criar_aluno():
    """Endpoint para criar um novo aluno no banco de dados."""
    dados = request.json
    
    # Validação básica
    if not dados or not all(k in dados for k in ['nome_completo', 'data_nascimento', 'nome_responsavel', 'telefone_responsavel', 'email_responsavel']):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (dados['nome_completo'], dados['data_nascimento'], dados['id_turma'], 
              dados['nome_responsavel'], dados['telefone_responsavel'], dados['email_responsavel'], 
              dados.get('informacoes_adicionais')))
        conn.commit()
        aluno_id = cursor.lastrowid
        logger.info(f"CREATE: Aluno {dados['nome_completo']} criado com sucesso. ID: {aluno_id}")
    except Exception as e:
        logger.error(f"CREATE: Erro ao criar aluno {dados['nome_completo']} - {str(e)}")
        return jsonify({"error": f"Erro ao criar aluno: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Aluno criado com sucesso!"}), 201

@aluno_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar aluno",
    "description": "Atualiza os dados de um aluno existente.",
    "tags": ["Aluno"],
    "responses": {
        200: {"description": "Aluno atualizado com sucesso!"},
        400: {"description": "Erro ao atualizar aluno."}
    }
})
def atualizar_aluno(id):
    """Endpoint para atualizar as informações de um aluno."""
    dados = request.json
    
    # Validação básica
    if not dados:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE aluno
            SET nome_completo=%s, data_nascimento=%s, id_turma=%s, nome_responsavel=%s, telefone_responsavel=%s, email_responsavel=%s, informacoes_adicionais=%s
            WHERE id_aluno=%s
        """, (dados['nome_completo'], dados['data_nascimento'], dados['id_turma'], 
              dados['nome_responsavel'], dados['telefone_responsavel'], dados['email_responsavel'], 
              dados.get('informacoes_adicionais'), id))
        conn.commit()
        logger.info(f"UPDATE: Aluno com ID {id} atualizado. Novos dados: {dados}")
    except Exception as e:
        logger.error(f"UPDATE: Erro ao atualizar aluno {id} - {str(e)}")
        return jsonify({"error": f"Erro ao atualizar aluno: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Aluno atualizado com sucesso!"})

@aluno_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir aluno",
    "description": "Remove um aluno do banco de dados.",
    "tags": ["Aluno"],
    "responses": {
        200: {"description": "Aluno excluído com sucesso!"},
        400: {"description": "Erro ao excluir aluno."}
    }
})
def excluir_aluno(id):
    """Endpoint para excluir um aluno."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aluno WHERE id_aluno=%s", (id,))
        if cursor.rowcount == 0:
            logger.error(f"DELETE: Falha ao deletar aluno {id} - Não encontrado.")
            return jsonify({"error": "Aluno não encontrado."}), 404
        conn.commit()
        logger.info(f"DELETE: Aluno com ID {id} removido com sucesso.")
    except Exception as e:
        logger.error(f"DELETE: Erro ao excluir aluno {id} - {str(e)}")
        return jsonify({"error": f"Erro ao excluir aluno: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Aluno excluído com sucesso!"})