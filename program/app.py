from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_string_de_conexao_com_o_banco_de_dados'
db = SQLAlchemy(app)

class Catador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100))
    # Outros campos do catador

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            # Outros campos do catador
        }

# Rota para criar um novo catador
@app.route('/catadores', methods=['POST'])
def criar_catador():
    data = request.json
    novo_catador = Catador(nome=data['nome'], sobrenome=data.get('sobrenome', ''))
    db.session.add(novo_catador)
    db.session.commit()
    return jsonify(novo_catador.to_dict()), 201

# Rota para listar todos os catadores
@app.route('/catadores', methods=['GET'])
def listar_catadores():
    catadores = Catador.query.all()
    return jsonify([catador.to_dict() for catador in catadores])

# Rota para obter um catador por ID
@app.route('/catadores/<int:catador_id>', methods=['GET'])
def obter_catador(catador_id):
    catador = Catador.query.get(catador_id)
    if catador:
        return jsonify(catador.to_dict())
    return jsonify({'mensagem': 'Catador não encontrado'}), 404

# Rota para atualizar os dados de um catador por ID
@app.route('/catadores/<int:catador_id>', methods=['PUT'])
def atualizar_catador(catador_id):
    catador = Catador.query.get(catador_id)
    if not catador:
        return jsonify({'mensagem': 'Catador não encontrado'}), 404
    data = request.json
    catador.nome = data['nome']
    catador.sobrenome = data.get('sobrenome', '')
    db.session.commit()
    return jsonify(catador.to_dict())

# Rota para excluir um catador por ID
@app.route('/catadores/<int:catador_id>', methods=['DELETE'])
def excluir_catador(catador_id):
    catador = Catador.query.get(catador_id)
    if not catador:
        return jsonify({'mensagem': 'Catador não encontrado'}), 404
    db.session.delete(catador)
    db.session.commit()
    return jsonify({'mensagem': 'Catador excluído'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
