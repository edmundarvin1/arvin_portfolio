# Portfolio CMS

A simple Content Management System for your portfolio website. This CMS allows you to:

- Write and publish articles using Markdown
- Upload HTML exports of Jupyter notebooks
- Manage links to your other applications and projects

## Features

- **Article Management**: Write, edit, and delete articles with Markdown support
- **Jupyter Notebook Integration**: Upload HTML exports of your Jupyter notebooks
- **Project Showcase**: Add links to your applications and projects
- **Tag-based Filtering**: Organize content with tags
- **Responsive Design**: Works on all devices
- **Simple Admin Interface**: Easy-to-use admin panel

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edmundarvin1/arvin_portfolio.git
cd arvin_portfolio/cms
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Update the configuration:
```bash
# Edit config.py to set your admin username and password
nano config.py
```

4. Run the application:
```bash
python app.py
```

5. Access the CMS:
   - Public site: http://localhost:8081
   - Admin panel: http://localhost:8081/admin

## Deployment

For production deployment, it's recommended to use Gunicorn and Nginx:

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/portfolio-cms.service
```

3. Add the following content:
```ini
[Unit]
Description=Portfolio CMS
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/portfolio/cms
ExecStart=/var/www/portfolio/cms/venv/bin/gunicorn -w 4 -b 127.0.0.1:8081 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/portfolio-cms
```

5. Add the following content:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/portfolio-cms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Usage

### Admin Panel

1. Log in to the admin panel at `/admin` using your credentials
2. Use the dashboard to manage your content
3. Create new articles, notebooks, or projects using the respective forms

### Writing Articles

1. Go to "New Article" in the admin panel
2. Enter a title, content (in Markdown), and tags
3. Optionally upload a featured image
4. Click "Save" to publish the article

### Adding Jupyter Notebooks

1. Export your Jupyter notebook as HTML:
   - In Jupyter, go to File > Export Notebook As > HTML
   - Save the HTML file
2. Go to "New Notebook" in the admin panel
3. Enter a title, description, and tags
4. Upload the HTML file
5. Click "Save" to publish the notebook

### Adding Projects

1. Go to "New Project" in the admin panel
2. Enter a title, description, URL, and tags
3. Optionally upload a featured image
4. Click "Save" to add the project

## Customization

- Edit the templates in `templates/public/` to customize the public-facing pages
- Modify `static/css/public.css` to change the styling
- Update `templates/admin/base.html` to customize the admin interface

## Security

For production use, make sure to:

1. Change the `SECRET_KEY` in `config.py`
2. Set a strong admin password
3. Use HTTPS in production
4. Regularly backup your content directory