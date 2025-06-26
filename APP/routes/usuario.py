from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar usuários",
    "description": "Retorna todos os usuários cadastrados.",
    "tags": ["Usuário"],
    "responses": {
        200: {
            "description": "Lista de usuários cadastrados.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_usuario": {"type": "integer"},
                        "login": {"type": "string"},
                        "nivel_acesso": {"type": "string"},
                        "id_professor": {"type": "integer"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar usuários."}
    }
})
def listar_usuarios():
    """Lista todos os usuários cadastrados no sistema."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario")
        usuarios = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar usuários: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {"id_usuario": row[0], "login": row[1], "nivel_acesso": row[2], "id_professor": row[3]} for row in usuarios
    ])

@usuario_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Criar usuário",
    "description": "Adiciona um novo usuário ao sistema.",
    "tags": ["Usuário"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "login": {"type": "string", "example": "admin"},
                    "senha": {"type": "string", "example": "123456"},
                    "nivel_acesso": {"type": "string", "example": "Administrador"},
                    "id_professor": {"type": "integer", "example": 5}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Usuário criado com sucesso."},
        400: {"description": "Erro ao criar usuário."}
    }
})
def criar_usuario():
    """Cria um novo usuário no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
        """, (dados['login'], dados['senha'], dados['nivel_acesso'], dados.get('id_professor')))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao criar usuário: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201

@usuario_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar usuário",
    "description": "Modifica as informações de um usuário existente.",
    "tags": ["Usuário"],
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
                    "login": {"type": "string", "example": "admin"},
                    "senha": {"type": "string", "example": "nova_senha"},
                    "nivel_acesso": {"type": "string", "example": "Administrador"},
                    "id_professor": {"type": "integer", "example": 5}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Usuário atualizado com sucesso."},
        400: {"description": "Erro ao atualizar usuário."}
    }
})
def atualizar_usuario(id):
    """Atualiza as informações de um usuário no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Usuario
            SET login=%s, senha=%s, nivel_acesso=%s, id_professor=%s
            WHERE id_usuario=%s
        """, (dados['login'], dados['senha'], dados['nivel_acesso'], dados.get('id_professor'), id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar usuário: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Usuário atualizado com sucesso!"})

@usuario_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir usuário",
    "description": "Remove um usuário do sistema.",
    "tags": ["Usuário"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Usuário excluído com sucesso."},
        400: {"description": "Erro ao excluir usuário."}
    }
})
def excluir_usuario(id):
    """Exclui um usuário do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id_usuario=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir usuário: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Usuário excluído com sucesso!"})