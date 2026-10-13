from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from logic import calculate, solve
from backend.database import create_user,verify_user
from backend.database import init_db, get_db_connection


app = Flask(__name__)
CORS(app)

init_db()

@app.route('/api/splitapp', methods=['POST'])
def simplify_debts():
    data = request.get_json()

    debtors, creditors = calculate(data)

    tractions = solve(debtors,creditors)
    
    return jsonify(tractions)

@app.route('/api/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Puste pole'}), 400
    if create_user(username,password):
        return jsonify({'message': 'Sukces'}), 201
    else:
        return jsonify({'error': 'Błąd rejestracji'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
            return jsonify({'error': 'Puste pole'}), 400

    if verify_user(username,password):
            return jsonify({'message': 'Zalogowano pomyslnie'}), 200
    else:
            return jsonify({'error': 'Błedny login, lub haslo'}), 401
    

if __name__ == '__main__':
    app.run(debug=True, port = 5000)