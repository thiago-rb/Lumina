from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

atividade_bp = Blueprint('atividade', __name__)

@atividade_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar atividades",
    "description": "Retorna todas as atividades cadastradas.",
    "tags": ["Atividade"],
    "responses": {
        200: {
            "description": "Lista de atividades cadastradas.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_atividade": {"type": "integer"},
                        "descricao": {"type": "string"},
                        "data_realizacao": {"type": "string", "format": "date"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar atividades."}
    }
})
def listar_atividades():
    """Lista todas as atividades cadastradas no banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Atividade")
        atividades = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar atividades: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([{"id_atividade": row[0], "descricao": row[1], "data_realizacao": row[2]} for row in atividades])

@atividade_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar uma nova atividade",
    "description": "Adiciona uma nova atividade ao sistema.",
    "tags": ["Atividade"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "descricao": {"type": "string", "example": "Aula de Ciências"},
                    "data_realizacao": {"type": "string", "format": "date", "example": "2025-05-01"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Atividade criada com sucesso."},
        400: {"description": "Erro ao criar atividade."}
    }
})
def criar_atividade():
    """Cria uma nova atividade no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Atividade (descricao, data_realizacao)
            VALUES (%s, %s)
        """, (dados['descricao'], dados['data_realizacao']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao criar atividade: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Atividade criada com sucesso!"}), 201

@atividade_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar uma atividade",
    "description": "Modifica as informações de uma atividade existente.",
    "tags": ["Atividade"],
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
                    "descricao": {"type": "string", "example": "Aula de Física"},
                    "data_realizacao": {"type": "string", "format": "date", "example": "2025-06-01"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Atividade atualizada com sucesso."},
        400: {"description": "Erro ao atualizar atividade."}
    }
})
def atualizar_atividade(id):
    """Atualiza uma atividade no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Atividade
            SET descricao=%s, data_realizacao=%s
            WHERE id_atividade=%s
        """, (dados['descricao'], dados['data_realizacao'], id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar atividade: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Atividade atualizada com sucesso!"})

@atividade_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir uma atividade",
    "description": "Remove uma atividade do sistema.",
    "tags": ["Atividade"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Atividade excluída com sucesso."},
        400: {"description": "Erro ao excluir atividade."}
    }
})
def excluir_atividade(id):
    """Exclui uma atividade do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Atividade WHERE id_atividade=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir atividade: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Atividade excluída com sucesso!"})