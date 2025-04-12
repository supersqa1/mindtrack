# Mindtrack - Learning Progress Tracker

A beginner-friendly web application for tracking learning progress through structured projects and tasks. Built with Flask (backend) and static HTML/CSS/JS (frontend).

## Project Structure

```
mindtrack/
├── backend/           # Flask backend application
│   ├── routes/        # API route handlers
│   ├── db.py          # Database connection and initialization
│   ├── config.py      # Configuration settings
│   ├── requirements.txt
│   └── README.md      # Backend-specific documentation
├── frontend/          # Static frontend application
│   ├── static/        # Static assets (CSS, JS, images)
│   ├── templates/     # HTML templates
│   ├── requirements.txt
│   └── README.md      # Frontend-specific documentation
└── docker-compose.yml # Docker configuration
```

## Features

- **User Management**
  - Registration and authentication
  - API key-based access control
  - Secure password handling

- **Project & Task Management**
  - Create and manage learning projects
  - Track task completion status
  - Submit task feedback and questions

- **API Access**
  - RESTful API endpoints
  - API key authentication
  - Demo data for testing

- **Development Features**
  - Docker-based deployment
  - Separate frontend and backend services
  - MySQL database
  - Clean, modular codebase

## Tech Stack

### Backend
- **Framework**: Flask
- **Database**: MySQL
- **Driver**: `pymysql`
- **ORM**: None (raw SQL for learning purposes)
- **Authentication**: Basic username/password + API key
- **API Style**: REST

### Frontend
- **Static Site**: HTML/CSS/JS
- **Styling**: Bootstrap 5
- **JavaScript**: Vanilla JS
- **API Communication**: Fetch API

### Deployment
- **Containerization**: Docker + Docker Compose
- **Database**: MySQL 8.0
- **Web Server**: Flask (development)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mindtrack
```

2. Configure Environment Variables:
Create a `.env` file in the backend directory with the following variables:
```bash
MYSQL_HOST=mysql
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

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:8000
- Backend API: http://localhost:6000
- MySQL: localhost:3306

### API Documentation

#### Public Endpoints (No Auth Required)
- `GET /demo/projects` - List sample projects
- `GET /demo/tasks` - List sample tasks

#### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login with email and password

#### User Endpoints (API Key Required)
- `GET /me/api-key` - Get your API key
- `GET /me/tasks` - List your tasks
- `POST /me/tasks/<task_id>/toggle` - Toggle task status
- `POST /me/tasks/<task_id>/feedback` - Submit task feedback

For detailed API usage examples, see the [API Examples](docs/api-examples.md) document.

## Development

### Backend Development
See [backend/README.md](backend/README.md) for detailed backend development instructions.

### Frontend Development
See [frontend/README.md](frontend/README.md) for detailed frontend development instructions.

## Database Schema

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

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.