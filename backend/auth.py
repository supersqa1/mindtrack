import secrets
import bcrypt
from db import get_db_connection
from config import Config

def generate_api_key():
    return secrets.token_hex(Config.API_KEY_LENGTH // 2)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_by_api_key(api_key):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE api_key = %s", (api_key,))
            return cursor.fetchone()
    finally:
        conn.close()

def create_user(email, password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            api_key = generate_api_key()
            password_hash = hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (email, password_hash, api_key)
                VALUES (%s, %s, %s)
            """, (email, password_hash, api_key))
            
            conn.commit()
            return api_key
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and verify_password(password, user['password_hash']):
                return user
            return None
    finally:
        conn.close()
