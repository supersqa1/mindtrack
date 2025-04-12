# Mindtrack Frontend

The frontend service for Mindtrack, built with static HTML, CSS, and JavaScript.

## Directory Structure

```
frontend/
├── static/           # Static assets
│   ├── css/         # Stylesheets
│   │   └── style.css
│   ├── js/          # JavaScript files
│   │   └── main.js
│   └── img/         # Images
├── templates/        # HTML templates
│   ├── base.html    # Base template
│   ├── index.html   # Home page
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
├── requirements.txt # Python dependencies
└── app.py          # Flask server for development
```

## Development Setup

### Prerequisites
- Python 3.9+ (for development server)
- Modern web browser
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

3. Start the development server:
```bash
python app.py
```

The frontend will be available at http://localhost:8000

### Docker Development

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The frontend will be available at http://localhost:8000

## Features

### User Interface
- Responsive design using Bootstrap 5
- Clean and intuitive navigation
- Mobile-friendly layout

### Pages
1. **Home Page** (`index.html`)
   - Project overview
   - Quick access to demo data
   - Navigation to register/login

2. **Registration** (`register.html`)
   - User registration form
   - Email and password validation
   - API key generation

3. **Login** (`login.html`)
   - User authentication
   - Session management
   - API key retrieval

4. **Dashboard** (`dashboard.html`)
   - Task management
   - Progress tracking
   - Feedback submission

### JavaScript Features
- API communication using Fetch
- Dynamic content loading
- Form validation
- Task status toggling
- Feedback submission
- API key management

## API Integration

The frontend communicates with the backend API at `http://localhost:6000`. Key API interactions include:

### Authentication
```javascript
// Register
fetch('http://localhost:6000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});

// Login
fetch('http://localhost:6000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});
```

### Task Management
```javascript
// Get tasks
fetch('http://localhost:6000/me/tasks', {
    headers: { 'X-API-Key': apiKey }
});

// Toggle task status
fetch(`http://localhost:6000/me/tasks/${taskId}/toggle`, {
    method: 'POST',
    headers: { 'X-API-Key': apiKey }
});

// Submit feedback
fetch(`http://localhost:6000/me/tasks/${taskId}/feedback`, {
    method: 'POST',
    headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: feedback })
});
```

## Styling

The frontend uses Bootstrap 5 for styling with custom CSS in `style.css`. Key styling features include:

- Responsive grid system
- Card-based layout
- Modern form styling
- Consistent color scheme
- Mobile-first design

## Browser Support

The frontend is compatible with:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test in multiple browsers
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 