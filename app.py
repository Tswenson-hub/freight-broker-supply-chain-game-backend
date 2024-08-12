from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from auth import create_user, authenticate_user, get_user_data
import os
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/register', methods=['POST'])
def register():
    app.logger.debug(f"Received registration request: {request.json}")
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    result = create_user(username, password)
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    app.logger.debug(f"Received login request: {request.json}")
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    result = authenticate_user(username, password)
    return jsonify(result)

@app.route('/api/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    result = get_user_data(token)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)