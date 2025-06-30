from flask import Flask
from flasgger import Swagger
from routes.aluno import aluno_bp
from routes.turma import turma_bp
from routes.professor import professor_bp
from routes.pagamento import pagamento_bp
from routes.presenca import presenca_bp
from routes.atividade import atividade_bp
from routes.atividade_aluno import atividade_aluno_bp
from routes.usuario import usuario_bp
import os

app = Flask(__name__)

# Configurações do Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Lumína - Sistema de Gerenciamento Escolar",
        "description": "API RESTful completa para gerenciamento de escola infantil",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Registro dos blueprints para cada CRUD
app.register_blueprint(aluno_bp, url_prefix='/alunos')
app.register_blueprint(turma_bp, url_prefix='/turmas')
app.register_blueprint(professor_bp, url_prefix='/professores')
app.register_blueprint(pagamento_bp, url_prefix='/pagamentos')
app.register_blueprint(presenca_bp, url_prefix='/presencas')
app.register_blueprint(atividade_bp, url_prefix='/atividades')
app.register_blueprint(atividade_aluno_bp, url_prefix='/atividades_alunos')
app.register_blueprint(usuario_bp, url_prefix='/usuarios')

# Rota de teste para verificar se o servidor está funcionando
@app.route('/', methods=['GET'])
def index():
    """Endpoint de saúde da API"""
    return {
        "message": "API do sistema de gerenciamento escolar está funcionando!",
        "version": "1.0.0",
        "documentation": "/apidocs/"
    }

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde"""
    return {"status": "healthy", "service": "lumina-api"}

# Tratamento de erros globais
@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint não encontrado"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Erro interno do servidor"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)