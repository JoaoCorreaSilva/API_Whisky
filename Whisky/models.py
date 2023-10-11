from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
