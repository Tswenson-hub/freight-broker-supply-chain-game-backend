from models import User
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

def create_user(username, password):
    if User.find_one({'username': username}):
        return {'success': False, 'message': 'Username already exists'}
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password)
    user.save()
    
    token = create_token(username)
    return {'success': True, 'token': token, 'username': username}

def authenticate_user(username, password):
    user = User.find_one({'username': username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return {'success': False, 'message': 'Invalid username or password'}
    
    token = create_token(username)
    return {'success': True, 'token': token, 'username': username}

def create_token(username):
    expiration = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm='HS256')

def get_user_data(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        user = User.find_one({'username': username})
        if user:
            return {'success': True, 'username': username}
        else:
            return {'success': False, 'message': 'User not found'}
    except jwt.ExpiredSignatureError:
        return {'success': False, 'message': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'success': False, 'message': 'Invalid token'}