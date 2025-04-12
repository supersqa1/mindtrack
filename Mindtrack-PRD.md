# PRD: Mindtrack - Learning Progress Tracker App

## Overview
**Mindtrack** is a beginner-friendly web application built to support a YouTube Python tutorial series. It helps learners track their progress through structured projects (e.g., "Learn Python"), manage their tasks, and optionally interact with the app via a public API. The application demonstrates practical use of Python, backend APIs, authentication, basic CRUD, and deployment workflows in a clean, modular way. It is built to be beginner-friendly while still modeling real-world app structures.

---

## Goals
- Provide a realistic learning companion app for the course
- Use the app to demonstrate Python concepts through real-world use cases
- Allow users to track their progress, interact with content, and experiment with APIs
- Keep the codebase simple and accessible to beginners
- Offer a public API with API key protection on modification routes
- Deployable via Docker with frontend and backend as separate apps
- Structured for full app build in the later part of the course

---

## Stack & Architecture

### Backend (API)
- **Framework**: Flask
- **Database**: MySQL
- **Driver**: `pymysql`
- **ORM**: None (raw SQL only)
- **Authentication**: Basic username/password with hashed passwords + API key
- **API style**: REST

### Frontend
- **Static site** (HTML/CSS/JS)
- **Styling**: Bootstrap
- **Separate app from backend**
- Communicates with backend via HTTP requests

### Deployment
- Docker + Docker Compose (frontend, backend, MySQL)
- GitHub repo with optional GitHub Actions (CI optional)

---

## App Features

### Users
- Register with email + password
- Login with email + password
- Automatically assigned an API key on registration
- Can request/reset API key from dashboard

### Projects
- Projects are containers for grouped tasks (e.g., "Learn Python")
- Each project has a title and description
- Admin can create projects via raw SQL or CLI script (no admin panel needed initially)

### To-Do Items (Tasks)
- Associated with a specific project
- Have a title, optional description, and status (done/not done)
- Students cannot create their own projects, only interact with pre-assigned tasks
- When a user registers, default tasks are assigned to their account under the "Learn Python" project
- Students can mark each task as done or undone
- Students can submit optional feedback or questions per task

### API Key & Access Control
- Students can access their API key from their dashboard
- API key required to access POST/PUT/DELETE endpoints
- API key only allows modification of that student’s data (user scoping)
- Basic GET endpoints are publicly available

---

## API Endpoints

### Public (No Auth Required)
- `GET /public/projects` - List sample projects (static or pre-seeded)
- `GET /public/tasks` - List sample tasks from "Learn Python"

### Auth (API Key Required)
- `POST /register` - Create a new user (returns API key)
- `POST /login` - Authenticates user, returns session/token
- `GET /me/api-key` - Returns current user’s API key
- `GET /me/tasks` - List tasks assigned to the user
- `POST /me/tasks/<task_id>/toggle` - Toggle done/not-done status
- `POST /me/tasks/<task_id>/feedback` - Submit a comment/question about a task

### Optional Dummy Endpoints (Teaching Tools)
- `POST /dummy/create-task` - Create a test task for experimentation (auto-scoped to test user)
- A cron job or scheduled cleanup removes dummy tasks older than X hours

---

## Database Design (MySQL - raw SQL, no migrations)

### users
| id | email | password_hash | api_key | created_at |

### projects
| id | title | description |

### tasks
| id | project_id | title | description |

### user_tasks
| id | user_id | task_id | is_done | created_at |

### feedback
| id | user_id | task_id | content | created_at |

---

## Dev Simplicity & Constraints
- No ORM
- No Alembic/Migrations
- No JWT or advanced OAuth (basic session or token system only)
- Minimal error handling, just enough to teach try/except
- Cron cleanup optional, done via Python scheduled script or cron in Docker
- Keep code simple and beginner-friendly with minimal abstractions

---

## Teaching Integration
- Python course will demonstrate concepts using small, real code snippets from Mindtrack
- Full app will be built from scratch after core Python tutorial is complete
- Early examples will use `GET` endpoints to show data fetching
- Later examples will introduce `POST`, user auth, API key usage, and database operations
- Encourages experimentation via dummy endpoints
- Frontend and backend separation helps teach HTTP requests and real-world app architecture

---

## Stretch Ideas (Future or Bootcamp)
- Admin panel
- Task stats / progress charts
- User achievements (gamification)
- Project recommendations
- Quiz module (merge quiz idea later)
