# Installation Guide

This guide will help you set up the portfolio website on your server.

## Prerequisites

- Python 3.6 or higher
- Nginx (optional but recommended)
- A Linux server (Ubuntu/Debian recommended)

## Installation Steps

### 1. Clone the repository

```bash
cd /var/www
sudo mkdir portfolio
sudo chown $USER:$USER portfolio
cd portfolio
git clone https://github.com/edmundarvin1/arvin_portfolio.git .
```

### 2. Set up a virtual environment

```bash
sudo apt update
sudo apt install -y python3-venv python3-full
python3 -m venv venv
source venv/bin/activate
```

### 3. Set up the systemd service

```bash
sudo cp portfolio.service /etc/systemd/system/
sudo chown -R www-data:www-data /var/www/portfolio
sudo systemctl daemon-reload
sudo systemctl start portfolio
sudo systemctl enable portfolio
```

### 4. Set up Nginx as a reverse proxy (Recommended)

Install Nginx:

```bash
sudo apt install -y nginx
```

Create a configuration file:

```bash
sudo nano /etc/nginx/sites-available/portfolio
```

Add the following content:

```nginx
server {
    listen 80;
    server_name your-domain-or-ip;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site if needed
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configure firewall (if enabled)

```bash
sudo ufw allow 'Nginx Full'
```

### 6. Access your website

Open a web browser and navigate to your server's IP address or domain name.

## Troubleshooting

If your website isn't working, check the logs:

```bash
# Check the portfolio service logs
sudo journalctl -u portfolio

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

If you need to make changes to your server.py file, remember to restart the service:

```bash
sudo systemctl restart portfolio
```