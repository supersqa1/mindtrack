from flask import Blueprint, request, jsonify
from functools import wraps
from db import get_db_connection
from auth import create_user, verify_user, get_user_by_api_key

user_bp = Blueprint('user', __name__)

def require_api_key(f):
    # The @wraps decorator is used to preserve the original function's metadata 
    # (such as its name, docstring, etc.) when it is wrapped by another function.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"error": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        api_key = create_user(data['email'], data['password'])
        return jsonify({"api_key": api_key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = verify_user(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"api_key": user['api_key']})

@user_bp.route('/me/api-key', methods=['GET'])
@require_api_key
def get_api_key():
    api_key = request.headers.get('X-API-Key')
    return jsonify({"api_key": api_key})

@user_bp.route('/me/tasks', methods=['GET'])
@require_api_key
def get_user_tasks():
    api_key = request.headers.get('X-API-Key')
    user = get_user_by_api_key(api_key)
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.*, p.title as project_title, ut.is_done
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                JOIN user_tasks ut ON t.id = ut.task_id
                WHERE ut.user_id = %s
            """, (user['id'],))
            tasks = cursor.fetchall()
            return jsonify(tasks)
    finally:
        conn.close()

@user_bp.route('/me/tasks/<int:task_id>/toggle', methods=['POST'])
@require_api_key
def toggle_task(task_id):
    api_key = request.headers.get('X-API-Key')
    user = get_user_by_api_key(api_key)
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE user_tasks
                SET is_done = NOT is_done
                WHERE user_id = %s AND task_id = %s
            """, (user['id'], task_id))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Task not found"}), 404
            
            conn.commit()
            return jsonify({"message": "Task status toggled"})
    finally:
        conn.close()

@user_bp.route('/me/tasks/<int:task_id>/feedback', methods=['POST'])
@require_api_key
def submit_feedback(task_id):
    api_key = request.headers.get('X-API-Key')
    user = get_user_by_api_key(api_key)
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Feedback content required"}), 400
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO feedback (user_id, task_id, content)
                VALUES (%s, %s, %s)
            """, (user['id'], task_id, data['content']))
            
            conn.commit()
            return jsonify({"message": "Feedback submitted"})
    finally:
        conn.close() 