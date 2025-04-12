from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Backend API configuration
BACKEND_URL = 'http://backend:6000'  # Using Docker service name

# Sample data for demo endpoints
DEMO_PROJECTS = [
    {
        "id": 1,
        "name": "Learn Python Basics",
        "description": "A beginner-friendly project to learn Python fundamentals"
    },
    {
        "id": 2,
        "name": "Web Development with Flask",
        "description": "Build your first web application using Flask"
    },
    {
        "id": 3,
        "name": "Data Analysis with Python",
        "description": "Learn how to analyze data using Python libraries"
    }
]

DEMO_TASKS = {
    1: [
        {
            "id": 101,
            "title": "Install Python",
            "description": "Download and install Python on your computer"
        },
        {
            "id": 102,
            "title": "Hello World",
            "description": "Write your first Python program that prints 'Hello, World!'"
        },
        {
            "id": 103,
            "title": "Variables and Types",
            "description": "Learn about different data types in Python"
        }
    ],
    2: [
        {
            "id": 201,
            "title": "Install Flask",
            "description": "Set up a virtual environment and install Flask"
        },
        {
            "id": 202,
            "title": "First Route",
            "description": "Create your first Flask route that returns 'Hello, World!'"
        },
        {
            "id": 203,
            "title": "Templates",
            "description": "Learn how to use templates in Flask"
        }
    ],
    3: [
        {
            "id": 301,
            "title": "Install Pandas",
            "description": "Set up your environment with Pandas library"
        },
        {
            "id": 302,
            "title": "Load Data",
            "description": "Learn how to load data from CSV files"
        },
        {
            "id": 303,
            "title": "Basic Analysis",
            "description": "Perform basic data analysis operations"
        }
    ]
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('my_projects'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f'{BACKEND_URL}/register',
                json={'email': email, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            
            # Store user info in session
            session['user_id'] = data['user_id']
            session['email'] = email
            session['api_key'] = data['api_key']
            
            flash('Registration successful!', 'success')
            return redirect(url_for('my_projects'))
        except requests.exceptions.RequestException as e:
            flash(str(e), 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('my_projects'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f'{BACKEND_URL}/login',
                json={'email': email, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            
            # Store user info in session
            session['user_id'] = data['user_id']
            session['email'] = email
            session['api_key'] = data['api_key']
            
            flash('Login successful!', 'success')
            return redirect(url_for('my_projects'))
        except requests.exceptions.RequestException as e:
            flash(str(e), 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/my-projects')
@login_required
def my_projects():
    try:
        # Get user's projects
        projects_response = requests.get(
            f'{BACKEND_URL}/me/projects',
            headers={'X-API-Key': session['api_key']}
        )
        projects_response.raise_for_status()
        projects = projects_response.json()
        
        # Get available public projects
        public_projects_response = requests.get(f'{BACKEND_URL}/public/projects')
        public_projects_response.raise_for_status()
        public_projects = public_projects_response.json()
        
        return render_template('my_projects.html', 
                             projects=projects,
                             public_projects=public_projects)
    except requests.exceptions.RequestException as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@app.route('/project/<int:project_id>/tasks')
@login_required
def project_tasks(project_id):
    try:
        # Get project details
        project_response = requests.get(
            f'{BACKEND_URL}/projects/{project_id}',
            headers={'X-API-Key': session['api_key']}
        )
        project_response.raise_for_status()
        project = project_response.json()
        
        # Get tasks for the project
        tasks_response = requests.get(
            f'{BACKEND_URL}/projects/{project_id}/tasks',
            headers={'X-API-Key': session['api_key']}
        )
        tasks_response.raise_for_status()
        tasks = tasks_response.json()
        
        # Calculate progress
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get('is_done'))
        
        return render_template('project_tasks.html',
                             project=project,
                             tasks=tasks,
                             total_tasks=total_tasks,
                             completed_tasks=completed_tasks)
    except requests.exceptions.RequestException as e:
        flash(str(e), 'danger')
        return redirect(url_for('my_projects'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/me/reset-api-key', methods=['POST'])
@login_required
def reset_api_key():
    try:
        response = requests.post(
            f'{BACKEND_URL}/me/reset-api-key',
            headers={'X-API-Key': session['api_key']}
        )
        response.raise_for_status()
        data = response.json()
        
        # Update session with new API key
        session['api_key'] = data['api_key']
        
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 400

@app.route('/demo')
def demo():
    return render_template('demo.html', projects=DEMO_PROJECTS)

@app.route('/api/demo/projects')
def get_demo_projects():
    return jsonify(DEMO_PROJECTS)

@app.route('/api/demo/projects/<int:project_id>/tasks')
def get_demo_project_tasks(project_id):
    tasks = DEMO_TASKS.get(project_id, [])
    return jsonify(tasks)

@app.route('/api/demo/tasks', methods=['POST'])
def create_demo_task():
    try:
        data = request.get_json()
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
            
        # Create a simple response with the submitted data
        response_data = {
            'id': len(DEMO_TASKS) + 1,
            'title': data['title'],
            'description': data.get('description', ''),
            'message': 'This is a demo task. In a real application, this would be saved to a database.'
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/public')
def public():
    try:
        # Get public projects
        projects_response = requests.get(f'{BACKEND_URL}/public/projects')
        projects_response.raise_for_status()
        projects = projects_response.json()
        
        return render_template('public.html', projects=projects)
    except requests.exceptions.RequestException as e:
        flash(str(e), 'danger')
        return render_template('public.html', projects=[])

@app.route('/api/public/projects/<int:project_id>/tasks')
def public_project_tasks(project_id):
    try:
        response = requests.get(f'{BACKEND_URL}/public/projects/{project_id}/tasks')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
