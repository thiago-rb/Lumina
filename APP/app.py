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

app = Flask(__name__)
swagger = Swagger(app)

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
    return {"message": "API do sistema de gerenciamento escolar está funcionando!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)