import os

class Config:
    # Flask settings
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    
    # Admin credentials
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'  # Change this in production!
    
    # Directory settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CONTENT_DIR = os.path.join(BASE_DIR, 'content')
    ARTICLES_DIR = os.path.join(CONTENT_DIR, 'articles')
    NOTEBOOKS_DIR = os.path.join(CONTENT_DIR, 'notebooks')
    PROJECTS_DIR = os.path.join(CONTENT_DIR, 'projects')
    UPLOADS_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'html'}