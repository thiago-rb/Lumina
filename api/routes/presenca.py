from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

presenca_bp = Blueprint('presenca', __name__)

@presenca_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar presenças",
    "description": "Retorna todas as presenças registradas.",
    "tags": ["Presenca"],
    "responses": {
        200: {
            "description": "Lista de presenças registradas.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_presenca": {"type": "integer"},
                        "id_aluno": {"type": "integer"},
                        "data_presenca": {"type": "string", "format": "date"},
                        "presente": {"type": "boolean"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar presenças."}
    }
})
def listar_presencas():
    """Lista todas as presenças registradas no sistema."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Presenca")
        presencas = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar presenças: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {"id_presenca": row[0], "id_aluno": row[1], "data_presenca": row[2], "presente": row[3]} for row in presencas
    ])

@presenca_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Registrar presença",
    "description": "Adiciona uma nova presença para um aluno.",
    "tags": ["Presenca"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "id_aluno": {"type": "integer", "example": 101},
                    "data_presenca": {"type": "string", "format": "date", "example": "2025-05-01"},
                    "presente": {"type": "boolean", "example": True}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Presença registrada com sucesso."},
        400: {"description": "Erro ao registrar presença."}
    }
})
def criar_presenca():
    """Registra uma nova presença no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
        """, (dados['id_aluno'], dados['data_presenca'], dados['presente']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao registrar presença: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Presença registrada com sucesso!"}), 201

@presenca_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar presença",
    "description": "Modifica os dados de uma presença existente.",
    "tags": ["Presenca"],
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
                    "id_aluno": {"type": "integer", "example": 101},
                    "data_presenca": {"type": "string", "format": "date", "example": "2025-05-01"},
                    "presente": {"type": "boolean", "example": False}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Presença atualizada com sucesso."},
        400: {"description": "Erro ao atualizar presença."}
    }
})
def atualizar_presenca(id):
    """Atualiza uma presença registrada no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Presenca
            SET id_aluno=%s, data_presenca=%s, presente=%s
            WHERE id_presenca=%s
        """, (dados['id_aluno'], dados['data_presenca'], dados['presente'], id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar presença: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Presença atualizada com sucesso!"})

@presenca_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir presença",
    "description": "Remove uma presença do sistema.",
    "tags": ["Presenca"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Presença excluída com sucesso."},
        400: {"description": "Erro ao excluir presença."}
    }
})
def excluir_presenca(id):
    """Exclui uma presença do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Presenca WHERE id_presenca=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir presença: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Presença excluída com sucesso!"})