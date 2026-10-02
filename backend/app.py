from flask import Flask, jsonify, request
from logic import calculate, solve
app = Flask(__name__)

@app.route('/api/splitapp', methods=['POST'])
def simplify_debts():
    data = request.get_json()

    debtors, creditors = calculate(data)

    tractions = solve(debtors,creditors)
    
    return jsonify(tractions)

if __name__ == '__main__':
    app.run(debug=True, port = 5000)