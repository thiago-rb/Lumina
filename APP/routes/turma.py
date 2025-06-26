from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

turma_bp = Blueprint('turma', __name__)

@turma_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar turmas",
    "description": "Retorna todas as turmas cadastradas.",
    "tags": ["Turma"],
    "responses": {
        200: {
            "description": "Lista de turmas cadastradas.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_turma": {"type": "integer"},
                        "nome_turma": {"type": "string"},
                        "id_professor": {"type": "integer"},
                        "horario": {"type": "string"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar turmas."}
    }
})
def listar_turmas():
    """Lista todas as turmas cadastradas no banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Turma")
        turmas = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar turmas: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {"id_turma": row[0], "nome_turma": row[1], "id_professor": row[2], "horario": row[3]} for row in turmas
    ])

@turma_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar turma",
    "description": "Adiciona uma nova turma ao sistema.",
    "tags": ["Turma"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "nome_turma": {"type": "string", "example": "Turma A"},
                    "id_professor": {"type": "integer", "example": 5},
                    "horario": {"type": "string", "example": "08:00 - 12:00"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Turma criada com sucesso."},
        400: {"description": "Erro ao criar turma."}
    }
})
def criar_turma():
    """Cria uma nova turma no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
        """, (dados['nome_turma'], dados['id_professor'], dados['horario']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao criar turma: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Turma criada com sucesso!"}), 201

@turma_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar turma",
    "description": "Modifica as informações de uma turma existente.",
    "tags": ["Turma"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "nome_turma": {"type": "string", "example": "Turma B"},
                    "id_professor": {"type": "integer", "example": 10},
                    "horario": {"type": "string", "example": "13:00 - 17:00"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Turma atualizada com sucesso."},
        400: {"description": "Erro ao atualizar turma."}
    }
})
def atualizar_turma(id):
    """Atualiza as informações de uma turma no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Turma
            SET nome_turma=%s, id_professor=%s, horario=%s
            WHERE id_turma=%s
        """, (dados['nome_turma'], dados['id_professor'], dados['horario'], id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar turma: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Turma atualizada com sucesso!"})

@turma_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir turma",
    "description": "Remove uma turma do sistema.",
    "tags": ["Turma"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Turma excluída com sucesso."},
        400: {"description": "Erro ao excluir turma."}
    }
})
def excluir_turma(id):
    """Exclui uma turma do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Turma WHERE id_turma=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir turma: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Turma excluída com sucesso!"})