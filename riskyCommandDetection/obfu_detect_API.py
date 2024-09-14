import json
import obfuscation_detection as od
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*"}}) # Enable CORS for all routes

def classify_commands(commands):
    oc = od.ObfuscationClassifier(od.PlatformType.ALL)
    classifications = oc(commands)
    # Convert numpy.int64 to Python int
    return [int(c) for c in classifications]

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    if not data or 'commands' not in data:
        return jsonify({"error": "No commands provided"}), 400
    
    commands = data['commands']
    results = classify_commands(commands)
    
    return jsonify({
        "classifications": results,
        "explanation": "1 indicates obfuscated, 0 indicates non-obfuscated"
    })

if __name__ == '__main__':
    app.run(debug=True)