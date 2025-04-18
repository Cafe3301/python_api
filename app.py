from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)

# Configura o JWT com a chave secreta vinda do .env
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Dados de produtos de papelaria
papelaria = [
    {'id': 1, 'produto': 'Mochila', 'quantidade': 3},
    {'id': 2, 'produto': 'Caderno', 'quantidade': 5},
    {'id': 3, 'produto': 'Caneta', 'quantidade': 10},
    {'id': 4, 'produto': 'Lápis', 'quantidade': 8},
    {'id': 5, 'produto': 'Borracha', 'quantidade': 12},
    {'id': 6, 'produto': 'Régua', 'quantidade': 7},
    {'id': 7, 'produto': 'Apontador', 'quantidade': 6},
    {'id': 8, 'produto': 'Marcador', 'quantidade': 4}
]

# Endpoint de login que gera o token JWT
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Verifica com os dados do .env
    if username != os.getenv("ADMIN_USERNAME") or password != os.getenv("ADMIN_PASSWORD"):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Lista todos os produtos (aberto)
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    return jsonify(papelaria)

# Adiciona produto (protegido)
@app.route('/api/produtos', methods=['POST'])
@jwt_required()
def add_produto():
    new_produto = request.get_json()
    papelaria.append(new_produto)

# Atualiza produto (protegido)
@app.route('/api/produtos/<int:id>', methods=['PUT'])
@jwt_required()
def update_produto(id):
    produto = next((item for item in papelaria if item['id'] == id), None)
    if produto:
        data = request.get_json()
        produto['produto'] = data.get('produto', produto['produto'])
        produto['quantidade'] = data.get('quantidade', produto['quantidade'])
        return jsonify(produto)
    return jsonify({'error': 'Produto não encontrado'}), 404

# Exclui produto (protegido)
@app.route('/api/produtos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_produto(id):
    global papelaria
    papelaria = [item for item in papelaria if item['id'] != id]
    return jsonify({'message': 'Produto excluído com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
