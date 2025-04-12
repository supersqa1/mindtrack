const API_BASE_URL = 'http://localhost:6000';
let currentApiKey = null;

// DOM Elements
const demoSection = document.getElementById('demoSection');
const authSection = document.getElementById('authSection');
const userSection = document.getElementById('userSection');
const demoProjects = document.getElementById('demoProjects');
const demoTasks = document.getElementById('demoTasks');
const userTasks = document.getElementById('userTasks');
const apiKeyDisplay = document.getElementById('apiKeyDisplay');
const copyApiKeyBtn = document.getElementById('copyApiKey');

// Navigation
document.getElementById('demoLink').addEventListener('click', (e) => {
    e.preventDefault();
    showSection('demo');
    loadDemoData();
});

document.getElementById('registerLink').addEventListener('click', (e) => {
    e.preventDefault();
    showSection('auth');
});

document.getElementById('loginLink').addEventListener('click', (e) => {
    e.preventDefault();
    showSection('auth');
});

// Forms
document.getElementById('registerForm').addEventListener('submit', handleRegister);
document.getElementById('loginForm').addEventListener('submit', handleLogin);
copyApiKeyBtn.addEventListener('click', copyApiKey);

function showSection(section) {
    demoSection.style.display = section === 'demo' ? 'block' : 'none';
    authSection.style.display = section === 'auth' ? 'block' : 'none';
    userSection.style.display = section === 'user' ? 'block' : 'none';
}

async function loadDemoData() {
    try {
        const [projects, tasks] = await Promise.all([
            fetch(`${API_BASE_URL}/demo/projects`).then(res => res.json()),
            fetch(`${API_BASE_URL}/demo/tasks`).then(res => res.json())
        ]);

        renderProjects(projects, demoProjects);
        renderTasks(tasks, demoTasks);
    } catch (error) {
        console.error('Error loading demo data:', error);
        alert('Failed to load demo data');
    }
}

async function loadUserTasks() {
    if (!currentApiKey) return;

    try {
        const response = await fetch(`${API_BASE_URL}/me/tasks`, {
            headers: {
                'X-API-Key': currentApiKey
            }
        });

        if (!response.ok) throw new Error('Failed to load tasks');

        const tasks = await response.json();
        renderTasks(tasks, userTasks, true);
    } catch (error) {
        console.error('Error loading user tasks:', error);
        alert('Failed to load tasks');
    }
}

function renderProjects(projects, container) {
    container.innerHTML = projects.map(project => `
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${project.title}</h5>
                    <p class="card-text">${project.description || ''}</p>
                </div>
            </div>
        </div>
    `).join('');
}

function renderTasks(tasks, container, isUserTasks = false) {
    container.innerHTML = tasks.map(task => `
        <div class="col-md-6">
            <div class="card task-card">
                <div class="card-body">
                    <div>
                        <h5 class="card-title">${task.title}</h5>
                        <p class="card-text">${task.description || ''}</p>
                        ${task.project_title ? `<small class="text-muted">Project: ${task.project_title}</small>` : ''}
                    </div>
                    <div class="task-actions">
                        ${isUserTasks ? `
                            <button class="btn btn-sm ${task.is_done ? 'btn-success' : 'btn-outline-secondary'}" 
                                    onclick="toggleTask(${task.id})">
                                ${task.is_done ? 'Done' : 'Mark Done'}
                            </button>
                            <button class="btn btn-sm btn-primary" 
                                    onclick="showFeedbackForm(${task.id})">
                                Feedback
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) throw new Error('Registration failed');

        const data = await response.json();
        currentApiKey = data.api_key;
        showUserSection();
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) throw new Error('Login failed');

        const data = await response.json();
        currentApiKey = data.api_key;
        showUserSection();
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed');
    }
}

function showUserSection() {
    showSection('user');
    apiKeyDisplay.textContent = currentApiKey;
    loadUserTasks();
}

async function toggleTask(taskId) {
    if (!currentApiKey) return;

    try {
        const response = await fetch(`${API_BASE_URL}/me/tasks/${taskId}/toggle`, {
            method: 'POST',
            headers: {
                'X-API-Key': currentApiKey
            }
        });

        if (!response.ok) throw new Error('Failed to toggle task');

        loadUserTasks();
    } catch (error) {
        console.error('Error toggling task:', error);
        alert('Failed to toggle task');
    }
}

function showFeedbackForm(taskId) {
    const feedbackForm = document.createElement('div');
    feedbackForm.className = 'feedback-form';
    feedbackForm.innerHTML = `
        <textarea class="form-control mb-2" placeholder="Enter your feedback or question"></textarea>
        <button class="btn btn-primary" onclick="submitFeedback(${taskId}, this)">Submit</button>
    `;

    const taskCard = document.querySelector(`[onclick="toggleTask(${taskId})"]`).closest('.card');
    taskCard.appendChild(feedbackForm);
}

async function submitFeedback(taskId, button) {
    if (!currentApiKey) return;

    const textarea = button.previousElementSibling;
    const content = textarea.value.trim();

    if (!content) {
        alert('Please enter feedback');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/me/tasks/${taskId}/feedback`, {
            method: 'POST',
            headers: {
                'X-API-Key': currentApiKey,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });

        if (!response.ok) throw new Error('Failed to submit feedback');

        button.closest('.feedback-form').remove();
        loadUserTasks();
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Failed to submit feedback');
    }
}

function copyApiKey() {
    navigator.clipboard.writeText(currentApiKey)
        .then(() => alert('API key copied to clipboard'))
        .catch(err => console.error('Failed to copy API key:', err));
}

// Initialize
loadDemoData();
