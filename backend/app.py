from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import run_slither
from ai_explainer import explain_vulnerability
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Smart Contract Scanner is running!"})

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({"error": "No Solidity code provided"}), 400
    
    solidity_code = data['code']
    vulnerabilities = run_slither(solidity_code)
    ai_report = explain_vulnerability(vulnerabilities)
    
    return jsonify({
        "vulnerabilities": vulnerabilities,
        "ai_report": ai_report,
        "total_found": len(vulnerabilities)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)