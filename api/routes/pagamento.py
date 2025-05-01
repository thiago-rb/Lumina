from flask import Blueprint, jsonify, request
from flasgger import swag_from
from db import connect_db

pagamento_bp = Blueprint('pagamento', __name__)

@pagamento_bp.route('/', methods=['GET'])
@swag_from({
    "summary": "Listar pagamentos",
    "description": "Retorna todos os pagamentos registrados.",
    "tags": ["Pagamento"],
    "responses": {
        200: {
            "description": "Lista de pagamentos.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id_pagamento": {"type": "integer"},
                        "id_aluno": {"type": "integer"},
                        "data_pagamento": {"type": "string", "format": "date"},
                        "valor_pago": {"type": "number"},
                        "forma_pagamento": {"type": "string"},
                        "referencia": {"type": "string"},
                        "status": {"type": "string"}
                    }
                }
            }
        },
        500: {"description": "Erro ao listar pagamentos."}
    }
})
def listar_pagamentos():
    """Lista todos os pagamentos registrados no sistema."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pagamento")
        pagamentos = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": f"Erro ao listar pagamentos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify([
        {"id_pagamento": row[0], "id_aluno": row[1], "data_pagamento": row[2], "valor_pago": row[3], 
         "forma_pagamento": row[4], "referencia": row[5], "status": row[6]} for row in pagamentos
    ])

@pagamento_bp.route('/', methods=['POST'])
@swag_from({
    "summary": "Registrar pagamento",
    "description": "Registra um novo pagamento para um aluno.",
    "tags": ["Pagamento"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "id_aluno": {"type": "integer", "example": 101},
                    "data_pagamento": {"type": "string", "format": "date", "example": "2025-05-01"},
                    "valor_pago": {"type": "number", "example": 250.50},
                    "forma_pagamento": {"type": "string", "example": "Cartão de Crédito"},
                    "referencia": {"type": "string", "example": "Fatura 12345"},
                    "status": {"type": "string", "example": "Pago"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Pagamento registrado com sucesso."},
        400: {"description": "Erro ao registrar pagamento."}
    }
})
def criar_pagamento():
    """Registra um novo pagamento no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dados['id_aluno'], dados['data_pagamento'], dados['valor_pago'], dados['forma_pagamento'], dados['referencia'], dados['status']))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao registrar pagamento: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Pagamento registrado com sucesso!"}), 201

@pagamento_bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    "summary": "Atualizar pagamento",
    "description": "Modifica os dados de um pagamento existente.",
    "tags": ["Pagamento"],
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
                    "data_pagamento": {"type": "string", "format": "date", "example": "2025-05-01"},
                    "valor_pago": {"type": "number", "example": 250.50},
                    "forma_pagamento": {"type": "string", "example": "Cartão de Crédito"},
                    "referencia": {"type": "string", "example": "Fatura 12345"},
                    "status": {"type": "string", "example": "Pago"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Pagamento atualizado com sucesso."},
        400: {"description": "Erro ao atualizar pagamento."}
    }
})
def atualizar_pagamento(id):
    """Atualiza as informações de um pagamento no banco de dados."""
    dados = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pagamento
            SET id_aluno=%s, data_pagamento=%s, valor_pago=%s, forma_pagamento=%s, referencia=%s, status=%s
            WHERE id_pagamento=%s
        """, (dados['id_aluno'], dados['data_pagamento'], dados['valor_pago'], dados['forma_pagamento'], dados['referencia'], dados['status'], id))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar pagamento: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Pagamento atualizado com sucesso!"})

@pagamento_bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    "summary": "Excluir pagamento",
    "description": "Remove um pagamento do sistema.",
    "tags": ["Pagamento"],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "type": "integer"
        }
    ],
    "responses": {
        200: {"description": "Pagamento excluído com sucesso."},
        400: {"description": "Erro ao excluir pagamento."}
    }
})
def excluir_pagamento(id):
    """Exclui um pagamento do banco de dados."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Pagamento WHERE id_pagamento=%s", (id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir pagamento: {str(e)}"}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Pagamento excluído com sucesso!"})