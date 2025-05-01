from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar professores",
    "description": "Retorna todos os professores cadastrados.",
    "tags": ["Professor"],
    "responses": {
        200: {
            "description": "Lista de professores cadastrados.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_professor": {"type": "integer"},
                        "nome_completo": {"type": "string"},
                        "email": {"type": "string"},
                        "telefone": {"type": "string"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar professores."}
    }
})
def listar_professores():
    """Lista todos os professores cadastrados no banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Professor")
        professores = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar professores: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {"id_professor": row[0], "nome_completo": row[1], "email": row[2], "telefone": row[3]} for row in professores
    ])

@professor_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar professor",
    "description": "Adiciona um novo professor ao sistema.",
    "tags": ["Professor"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "nome_completo": {"type": "string", "example": "Maria Silva"},
                    "email": {"type": "string", "example": "maria.silva@example.com"},
                    "telefone": {"type": "string", "example": "(11) 99999-9999"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Professor criado com sucesso."},
        400: {"description": "Erro ao criar professor."}
    }
})
def criar_professor():
    """Cria um novo professor no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Professor (nome_completo, email, telefone)
            VALUES (%s, %s, %s)
        """, (dados['nome_completo'], dados['email'], dados['telefone']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao criar professor: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Professor criado com sucesso!"}), 201

@professor_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar professor",
    "description": "Modifica as informações de um professor existente.",
    "tags": ["Professor"],
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
                    "nome_completo": {"type": "string", "example": "João Pereira"},
                    "email": {"type": "string", "example": "joao.pereira@example.com"},
                    "telefone": {"type": "string", "example": "(11) 98888-8888"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Professor atualizado com sucesso."},
        400: {"description": "Erro ao atualizar professor."}
    }
})
def atualizar_professor(id):
    """Atualiza as informações de um professor no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Professor
            SET nome_completo=%s, email=%s, telefone=%s
            WHERE id_professor=%s
        """, (dados['nome_completo'], dados['email'], dados['telefone'], id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar professor: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Professor atualizado com sucesso!"})

@professor_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir professor",
    "description": "Remove um professor do sistema.",
    "tags": ["Professor"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Professor excluído com sucesso."},
        400: {"description": "Erro ao excluir professor."}
    }
})
def excluir_professor(id):
    """Exclui um professor do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Professor WHERE id_professor=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir professor: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Professor excluído com sucesso!"})