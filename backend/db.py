import pymysql
import time
from config import Config

def get_db_connection(max_retries=5, retry_delay=5):
    for attempt in range(max_retries):
        try:
            return pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                db=Config.MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.err.OperationalError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Failed to connect to MySQL (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    return None

def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT
                )
            """)
            
            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    project_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)
            
            # Create user_tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    task_id INT NOT NULL,
                    is_done BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)
            
            # Create feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    task_id INT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)
            
            # Insert demo project if not exists
            cursor.execute("""
                INSERT IGNORE INTO projects (id, title, description)
                VALUES (1, 'Learn Python', 'A beginner-friendly Python learning project')
            """)
            
            # Insert demo tasks if not exists
            demo_tasks = [
                (1, 'Install Python', 'Download and install Python on your computer'),
                (1, 'Hello World', 'Write your first Python program'),
                (1, 'Variables', 'Learn about variables and data types'),
                (1, 'Functions', 'Understand how to create and use functions')
            ]
            
            for project_id, title, description in demo_tasks:
                cursor.execute("""
                    INSERT IGNORE INTO tasks (project_id, title, description)
                    VALUES (%s, %s, %s)
                """, (project_id, title, description))
            
        conn.commit()
    finally:
        conn.close()
