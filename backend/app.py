from flask import Flask
from routes.demo import demo_bp
from routes.user import user_bp
from db import init_db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(demo_bp, url_prefix='/demo')
    app.register_blueprint(user_bp, url_prefix='')
    
    # Initialize database
    with app.app_context():
        init_db()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
