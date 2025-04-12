# MindTrack Backend

The backend service for Mindtrack, built with Flask and MySQL.

## Directory Structure

```
backend/
├── routes/           # API route handlers
│   ├── demo.py      # Demo data endpoints
│   └── user.py      # User management endpoints
├── db.py            # Database connection and initialization
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
└── app.py          # Flask application entry point
```

## Development Setup

### Prerequisites
- Python 3.13+
- MySQL 8.0
- Docker and Docker Compose (optional)

### Local Development

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Environment Variables:
Create a `.env` file in the backend directory:
```bash
touch .env
```

Add the following to `.env`:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=mindtrack
SECRET_KEY=your-secret-key-here
```

**Important Note about SECRET_KEY:**
The `SECRET_KEY` is used for cryptographic operations in Flask. It should be:
- At least 32 characters long
- A random mix of uppercase letters, lowercase letters, numbers, and special characters
- Different for each environment (development, staging, production)
- Never committed to version control

You can generate a secure secret key using Python:
```python
import secrets
import string

def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Example output: 'k9#mP$2L!vX8@nQ5&jR3*hW7^bY4%cU6'
```

4. Start the development server:
```bash
python app.py
```

The server will start at http://localhost:6000

### Docker Development

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The backend will be available at http://localhost:6000

## API Documentation

### Demo Endpoints

#### GET /demo/projects
Returns a list of sample projects.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Learn Python",
    "description": "A beginner-friendly Python learning project"
  }
]
```

#### GET /demo/tasks
Returns a list of sample tasks.

**Response:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Install Python",
    "description": "Download and install Python on your computer"
  }
]
```

### User Endpoints

#### POST /register
Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "api_key": "your-api-key-here"
}
```

#### POST /login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "api_key": "your-api-key-here"
}
```

#### GET /me/tasks
Get user's tasks (requires API key).

**Headers:**
```
X-API-Key: your-api-key-here
```

**Response:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Install Python",
    "description": "Download and install Python on your computer",
    "is_done": false
  }
]
```

#### POST /me/tasks/<task_id>/toggle
Toggle task completion status (requires API key).

**Headers:**
```
X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "message": "Task status updated"
}
```

#### POST /me/tasks/<task_id>/feedback
Submit feedback for a task (requires API key).

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request:**
```json
{
  "content": "This task was very helpful!"
}
```

**Response:**
```json
{
  "message": "Feedback submitted"
}
```

## Database

The backend uses MySQL with the following schema:

### users
- id (INT, PRIMARY KEY)
- email (VARCHAR(255), UNIQUE)
- password_hash (VARCHAR(255))
- api_key (VARCHAR(255), UNIQUE)
- created_at (TIMESTAMP)

### projects
- id (INT, PRIMARY KEY)
- title (VARCHAR(255))
- description (TEXT)

### tasks
- id (INT, PRIMARY KEY)
- project_id (INT, FOREIGN KEY)
- title (VARCHAR(255))
- description (TEXT)

### user_tasks
- id (INT, PRIMARY KEY)
- user_id (INT, FOREIGN KEY)
- task_id (INT, FOREIGN KEY)
- is_done (BOOLEAN)
- created_at (TIMESTAMP)

### feedback
- id (INT, PRIMARY KEY)
- user_id (INT, FOREIGN KEY)
- task_id (INT, FOREIGN KEY)
- content (TEXT)
- created_at (TIMESTAMP)

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 