import os
import json
import markdown
import shutil
from datetime import datetime
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for authentication
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load user from config
admin_user = User(
    1, 
    app.config['ADMIN_USERNAME'], 
    generate_password_hash(app.config['ADMIN_PASSWORD'])
)

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:
        return admin_user
    return None

# Ensure content directories exist
for dir_path in [
    app.config['ARTICLES_DIR'],
    app.config['NOTEBOOKS_DIR'],
    app.config['PROJECTS_DIR'],
    app.config['UPLOADS_DIR']
]:
    os.makedirs(dir_path, exist_ok=True)

# Helper functions
def get_articles():
    articles = []
    for filename in os.listdir(app.config['ARTICLES_DIR']):
        if filename.endswith('.json'):
            with open(os.path.join(app.config['ARTICLES_DIR'], filename), 'r') as f:
                article = json.load(f)
                articles.append(article)
    return sorted(articles, key=lambda x: x['date'], reverse=True)

def get_notebooks():
    notebooks = []
    for filename in os.listdir(app.config['NOTEBOOKS_DIR']):
        if filename.endswith('.json'):
            with open(os.path.join(app.config['NOTEBOOKS_DIR'], filename), 'r') as f:
                notebook = json.load(f)
                notebooks.append(notebook)
    return sorted(notebooks, key=lambda x: x['date'], reverse=True)

def get_projects():
    projects = []
    for filename in os.listdir(app.config['PROJECTS_DIR']):
        if filename.endswith('.json'):
            with open(os.path.join(app.config['PROJECTS_DIR'], filename), 'r') as f:
                project = json.load(f)
                projects.append(project)
    return sorted(projects, key=lambda x: x['date'], reverse=True)

def save_article(title, content, tags, image=None):
    slug = title.lower().replace(' ', '-')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{slug}.json"
    
    article = {
        'id': timestamp,
        'title': title,
        'content': content,
        'content_html': markdown.markdown(content),
        'tags': tags.split(',') if tags else [],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'image': image if image else '',
        'slug': slug
    }
    
    with open(os.path.join(app.config['ARTICLES_DIR'], filename), 'w') as f:
        json.dump(article, f, indent=4)
    
    return article

def save_notebook(title, description, html_file, tags):
    slug = title.lower().replace(' ', '-')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{slug}.json"
    
    # Save the HTML file
    html_filename = f"{timestamp}_{slug}.html"
    html_path = os.path.join(app.config['NOTEBOOKS_DIR'], html_filename)
    shutil.copy(html_file, html_path)
    
    notebook = {
        'id': timestamp,
        'title': title,
        'description': description,
        'html_file': html_filename,
        'tags': tags.split(',') if tags else [],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'slug': slug
    }
    
    with open(os.path.join(app.config['NOTEBOOKS_DIR'], filename), 'w') as f:
        json.dump(notebook, f, indent=4)
    
    return notebook

def save_project(title, description, url, image, tags):
    slug = title.lower().replace(' ', '-')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{slug}.json"
    
    project = {
        'id': timestamp,
        'title': title,
        'description': description,
        'url': url,
        'image': image if image else '',
        'tags': tags.split(',') if tags else [],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'slug': slug
    }
    
    with open(os.path.join(app.config['PROJECTS_DIR'], filename), 'w') as f:
        json.dump(project, f, indent=4)
    
    return project

# Routes
@app.route('/')
def index():
    articles = get_articles()[:5]  # Get latest 5 articles
    notebooks = get_notebooks()[:5]  # Get latest 5 notebooks
    projects = get_projects()[:5]  # Get latest 5 projects
    current_year = date.today().year
    return render_template('public/index.html', 
                          articles=articles, 
                          notebooks=notebooks, 
                          projects=projects,
                          current_year=current_year)

@app.route('/articles')
def articles():
    articles = get_articles()
    current_year = date.today().year
    return render_template('public/articles.html', articles=articles, current_year=current_year)

@app.route('/article/<slug>')
def article(slug):
    current_year = date.today().year
    for article in get_articles():
        if article['slug'] == slug:
            return render_template('public/article.html', article=article, current_year=current_year)
    return redirect(url_for('articles'))

@app.route('/notebooks')
def notebooks():
    notebooks = get_notebooks()
    current_year = date.today().year
    return render_template('public/notebooks.html', notebooks=notebooks, current_year=current_year)

@app.route('/notebook/<slug>')
def notebook(slug):
    current_year = date.today().year
    for notebook in get_notebooks():
        if notebook['slug'] == slug:
            html_path = os.path.join(app.config['NOTEBOOKS_DIR'], notebook['html_file'])
            with open(html_path, 'r') as f:
                html_content = f.read()
            return render_template('public/notebook.html', 
                                  notebook=notebook, 
                                  html_content=html_content,
                                  current_year=current_year)
    return redirect(url_for('notebooks'))

@app.route('/projects')
def projects():
    projects = get_projects()
    current_year = date.today().year
    return render_template('public/projects.html', projects=projects, current_year=current_year)

@app.route('/project/<slug>')
def project(slug):
    current_year = date.today().year
    for project in get_projects():
        if project['slug'] == slug:
            return render_template('public/project.html', project=project, current_year=current_year)
    return redirect(url_for('projects'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == admin_user.username and admin_user.check_password(password):
            login_user(admin_user)
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    articles = get_articles()
    notebooks = get_notebooks()
    projects = get_projects()
    return render_template('admin/dashboard.html', 
                          articles=articles, 
                          notebooks=notebooks, 
                          projects=projects)

@app.route('/admin/article/new', methods=['GET', 'POST'])
@login_required
def new_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        image = ''
        
        if 'image' in request.files and request.files['image'].filename:
            image_file = request.files['image']
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image = f"{timestamp}_{filename}"
            image_file.save(os.path.join(app.config['UPLOADS_DIR'], image))
        
        save_article(title, content, tags, image)
        flash('Article created successfully!')
        return redirect(url_for('admin'))
    
    return render_template('admin/article_form.html')

@app.route('/admin/notebook/new', methods=['GET', 'POST'])
@login_required
def new_notebook():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags')
        
        if 'html_file' in request.files and request.files['html_file'].filename:
            html_file = request.files['html_file']
            filename = secure_filename(html_file.filename)
            temp_path = os.path.join(app.config['UPLOADS_DIR'], filename)
            html_file.save(temp_path)
            
            save_notebook(title, description, temp_path, tags)
            os.remove(temp_path)  # Remove the temp file
            
            flash('Notebook added successfully!')
            return redirect(url_for('admin'))
        else:
            flash('HTML file is required')
    
    return render_template('admin/notebook_form.html')

@app.route('/admin/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        tags = request.form.get('tags')
        image = ''
        
        if 'image' in request.files and request.files['image'].filename:
            image_file = request.files['image']
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image = f"{timestamp}_{filename}"
            image_file.save(os.path.join(app.config['UPLOADS_DIR'], image))
        
        save_project(title, description, url, image, tags)
        flash('Project added successfully!')
        return redirect(url_for('admin'))
    
    return render_template('admin/project_form.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADS_DIR'], filename)

@app.route('/admin/article/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    # Find the article
    article_path = None
    article_data = None
    
    for filename in os.listdir(app.config['ARTICLES_DIR']):
        if filename.endswith('.json'):
            with open(os.path.join(app.config['ARTICLES_DIR'], filename), 'r') as f:
                data = json.load(f)
                if data['id'] == id:
                    article_path = os.path.join(app.config['ARTICLES_DIR'], filename)
                    article_data = data
                    break
    
    if not article_data:
        flash('Article not found')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        image = article_data['image']
        
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image if exists
            if article_data['image']:
                try:
                    os.remove(os.path.join(app.config['UPLOADS_DIR'], article_data['image']))
                except:
                    pass
            
            image_file = request.files['image']
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image = f"{timestamp}_{filename}"
            image_file.save(os.path.join(app.config['UPLOADS_DIR'], image))
        
        # Update article
        article_data['title'] = title
        article_data['content'] = content
        article_data['content_html'] = markdown.markdown(content)
        article_data['tags'] = tags.split(',') if tags else []
        article_data['image'] = image
        article_data['slug'] = title.lower().replace(' ', '-')
        
        with open(article_path, 'w') as f:
            json.dump(article_data, f, indent=4)
        
        flash('Article updated successfully!')
        return redirect(url_for('admin'))
    
    return render_template('admin/article_form.html', article=article_data)

@app.route('/admin/article/delete/<id>', methods=['POST'])
@login_required
def delete_article(id):
    for filename in os.listdir(app.config['ARTICLES_DIR']):
        if filename.endswith('.json'):
            file_path = os.path.join(app.config['ARTICLES_DIR'], filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if data['id'] == id:
                    # Delete image if exists
                    if data['image']:
                        try:
                            os.remove(os.path.join(app.config['UPLOADS_DIR'], data['image']))
                        except:
                            pass
                    
                    # Delete article file
                    os.remove(file_path)
                    flash('Article deleted successfully!')
                    break
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=57658, debug=True)