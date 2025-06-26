from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

atividade_aluno_bp = Blueprint('atividade_aluno', __name__)

@atividade_aluno_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar associações entre Atividade e Aluno",
    "description": "Retorna todas as associações entre atividades e alunos.",
    "tags": ["Atividade_Aluno"],
    "responses": {
        200: {
            "description": "Lista de associações entre atividades e alunos.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_atividade": {"type": "integer"},
                        "id_aluno": {"type": "integer"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar associações."}
    }
})
def listar_atividades_alunos():
    """Lista todas as associações entre Atividade e Aluno no banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Atividade_Aluno")
        atividades_alunos = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar atividades e alunos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([{"id_atividade": row[0], "id_aluno": row[1]} for row in atividades_alunos])

@atividade_aluno_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar associação entre Atividade e Aluno",
    "description": "Cria uma nova relação entre um aluno e uma atividade.",
    "tags": ["Atividade_Aluno"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "id_atividade": {"type": "integer", "example": 1},
                    "id_aluno": {"type": "integer", "example": 101}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Associação criada com sucesso."},
        400: {"description": "Erro ao criar associação."}
    }
})
def criar_atividade_aluno():
    """Cria uma nova associação entre Atividade e Aluno."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Atividade_Aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
        """, (dados['id_atividade'], dados['id_aluno']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao criar associação: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Associação entre Atividade e Aluno criada com sucesso!"}), 201

@atividade_aluno_bp.route('/', methods=['DELETE'])
@swag_from({
    "summary": "Excluir associação entre Atividade e Aluno",
    "description": "Remove a relação entre um aluno e uma atividade.",
    "tags": ["Atividade_Aluno"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "id_atividade": {"type": "integer", "example": 1},
                    "id_aluno": {"type": "integer", "example": 101}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Associação excluída com sucesso."},
        400: {"description": "Erro ao excluir associação."}
    }
})
def excluir_atividade_aluno():
    """Remove uma associação entre Atividade e Aluno."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Atividade_Aluno
            WHERE id_atividade=%s AND id_aluno=%s
        """, (dados['id_atividade'], dados['id_aluno']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir associação: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Associação entre Atividade e Aluno excluída com sucesso!"})