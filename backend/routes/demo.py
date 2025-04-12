from flask import Blueprint, jsonify
from db import get_db_connection
from config import Config

demo_bp = Blueprint('demo', __name__)

@demo_bp.route('/projects', methods=['GET'])
def get_demo_projects():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM projects")
            projects = cursor.fetchall()
            return jsonify(projects)
    finally:
        conn.close()

@demo_bp.route('/tasks', methods=['GET'])
def get_demo_tasks():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.*, p.title as project_title
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
            """)
            tasks = cursor.fetchall()
            return jsonify(tasks)
    finally:
        conn.close()

@demo_bp.route('/tasks/create', methods=['POST'])
def create_demo_task():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Create a demo task for the demo user
            cursor.execute("""
                INSERT INTO tasks (project_id, title, description)
                VALUES (1, 'Demo Task', 'This is a demo task that will be cleaned up')
            """)
            task_id = cursor.lastrowid
            
            # Assign to demo user
            cursor.execute("""
                INSERT INTO user_tasks (user_id, task_id)
                VALUES (%s, %s)
            """, (Config.DEMO_USER_ID, task_id))
            
            conn.commit()
            return jsonify({"message": "Demo task created", "task_id": task_id})
    finally:
        conn.close() 