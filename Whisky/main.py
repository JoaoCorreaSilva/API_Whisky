from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'whiskies.db'

def get_whiskies_from_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, age, type FROM whiskies')
    whiskies = cursor.fetchall()
    conn.close()
    return whiskies

@app.route('/whiskies', methods=['GET'])
def get_whiskies():
    whiskies = get_whiskies_from_db()
    whiskies_list = []
    for whisky in whiskies:
        whisky_dict = {
            'id': whisky[0],
            'name': whisky[1],
            'age': whisky[2],
            'type': whisky[3]
        }
        whiskies_list.append(whisky_dict)
    return jsonify({'whiskies': whiskies_list})

def insert_whisky_into_db(name, age, type):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO whiskies (name, age, type) VALUES (?, ?, ?)', (name, age, type))
    conn.commit()
    conn.close()

@app.route('/whiskies', methods=['POST'])
def create_whisky():
    # Verifica se a solicitação tem dados JSON válidos no corpo
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados JSON inválidos'}), 400

    # Extrai os dados do corpo da solicitação
    name = data.get('name')
    age = data.get('age')
    whisky_type = data.get('type')

    # Valida os dados
    if not name or not age or not whisky_type:
        return jsonify({'error': 'Campos obrigatórios não preenchidos'}), 400

    # Insere o whisky no banco de dados
    insert_whisky_into_db(name, age, whisky_type)

    # Retorna o whisky criado em formato JSON com um código de status 201 (Created)
    return jsonify({'message': 'Whisky criado com sucesso'}), 201


def update_whisky_in_db(whisky_id, name, age, whisky_type):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE whiskies SET name=?, age=?, type=? WHERE id=?', (name, age, whisky_type, whisky_id))
    conn.commit()
    conn.close()

def get_whisky_by_id(whisky_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, age, type FROM whiskies WHERE id=?', (whisky_id,))
    whisky = cursor.fetchone()
    conn.close()
    return whisky

@app.route('/whiskies/<int:whisky_id>', methods=['PUT'])
def update_whisky(whisky_id):
    # Verifica se o whisky com o ID fornecido existe
    existing_whisky = get_whisky_by_id(whisky_id)
    if not existing_whisky:
        return jsonify({'error': 'Whisky não encontrado'}), 404

    # Verifica se a solicitação tem dados JSON válidos no corpo
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados JSON inválidos'}), 400

    # Extrai os dados do corpo da solicitação
    name = data.get('name')
    age = data.get('age')
    whisky_type = data.get('type')

    # Valida os dados
    if not name or not age or not whisky_type:
        return jsonify({'error': 'Campos obrigatórios não preenchidos'}), 400

    # Atualiza o whisky no banco de dados
    update_whisky_in_db(whisky_id, name, age, whisky_type)

    # Retorna o whisky atualizado em formato JSON com um código de status 200 (OK)
    updated_whisky = get_whisky_by_id(whisky_id)
    return jsonify({'message': 'Whisky atualizado com sucesso', 'whisky': updated_whisky})


def delete_whisky_from_db(whisky_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM whiskies WHERE id=?', (whisky_id,))
    conn.commit()
    conn.close()

def get_whisky_by_id(whisky_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, age, type FROM whiskies WHERE id=?', (whisky_id,))
    whisky = cursor.fetchone()
    conn.close()
    return whisky

@app.route('/whiskies/<int:whisky_id>', methods=['DELETE'])
def delete_whisky(whisky_id):
    # Verifica se o whisky com o ID fornecido existe
    existing_whisky = get_whisky_by_id(whisky_id)
    if not existing_whisky:
        return jsonify({'error': 'Whisky não encontrado'}), 404

    # Exclui o whisky do banco de dados
    delete_whisky_from_db(whisky_id)

    # Retorna uma resposta vazia (204 No Content) para indicar sucesso na exclusão
    return '', 204

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)