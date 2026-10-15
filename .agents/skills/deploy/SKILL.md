---
name: deploy
description: Deploy changes to the production GCP VM for arvindeleon.com
---

# Deploy to Production

Deploy the latest changes from the main branch to the GCP VM hosting arvindeleon.com.

## Prerequisites

- Changes must be pushed to the `main` branch on GitHub
- User must have gcloud CLI configured and authenticated
- GCP instance: `instance-20250301-143625` in zone `europe-north2-a`

## Deployment Steps

Use this skill when the user asks to deploy, push to production, or update the live site.

### 1. Add Git Safe Directory (if needed)

Git may complain about dubious ownership. Fix this first:

```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo git config --global --add safe.directory /var/www/portfolio"
```

### 2. Pull Latest Changes

Fetch and reset to the latest main branch:

```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="cd /var/www/portfolio && sudo git fetch origin && sudo git reset --hard origin/main"
```

This command will output the new HEAD commit and any files that changed.

### 3. Restart the Python Server

Kill the existing server process and start a new one:

```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo pkill -f 'python /var/www/portfolio/server.py' && sleep 2 && cd /var/www/portfolio && nohup sudo -u www-data /var/www/portfolio/venv/bin/python /var/www/portfolio/server.py > /var/log/portfolio-server.log 2>&1 &"
```

### 4. Verify Deployment

Check that the server is running:

```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sleep 3 && ps aux | grep 'python /var/www/portfolio/server.py' | grep -v grep"
```

You should see output showing the Python server process (usually as www-data user).

### 5. Test the Site

Verify the site is accessible and serving the latest content:

```bash
curl -s https://arvindeleon.com/ | grep -o '<title>.*</title>'
```

Expected output: `<title>Arvin De Leon</title>` or similar.

Optionally test specific pages:
- Main site: `https://arvindeleon.com/`
- Projects: `https://arvindeleon.com/projects.html`
- About: `https://arvindeleon.com/about.html`
- Trading Dashboard: `https://arvindeleon.com/projects/trading-pnl/`
- Gym Analytics: `https://arvindeleon.com/projects/gym-analytics/`

## Report to User

After successful deployment, inform the user:
1. The new HEAD commit hash
2. List of files that changed
3. Server status (PID and user)
4. Confirmation that the site is accessible via HTTPS

Example summary:
```
✅ Deployment Complete!

Deployed commit: abc1234 "Your commit message"
Files changed: 5 files (index.html, styles/main.css, ...)
Server restarted: PID 12345 (running as www-data)
Site accessible: ✅ https://arvindeleon.com
```

## Troubleshooting

### Server Won't Start
Check the logs:
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo tail -50 /var/log/portfolio-server.log"
```

### Nginx Issues
Check nginx status and restart if needed:
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo systemctl status nginx"
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo systemctl restart nginx"
```

### Port Conflicts
Check what's listening on port 8080:
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo netstat -tlnp | grep 8080"
```

## Backend Deployment (Flask API)

If deploying the Flask backend API (for dashboards):

1. **Install dependencies:**
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="cd /var/www/portfolio/backend && sudo /var/www/portfolio/venv/bin/pip install -r requirements.txt"
```

2. **Set up environment variables:**
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo nano /var/www/portfolio/backend/.env"
```

3. **Create systemd service for Flask:**
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo tee /etc/systemd/system/portfolio-api.service <<'EOF'
[Unit]
Description=Portfolio API Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/portfolio/backend
Environment=\"PATH=/var/www/portfolio/venv/bin\"
ExecStart=/var/www/portfolio/venv/bin/python /var/www/portfolio/backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
"
```

4. **Start the service:**
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo systemctl daemon-reload && sudo systemctl enable portfolio-api && sudo systemctl start portfolio-api"
```

5. **Configure nginx to proxy /api/ requests:**
Add to nginx config at `/etc/nginx/sites-available/portfolio`:
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:5001/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Then restart nginx:
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a --command="sudo systemctl restart nginx"
```

## Important Notes

- **Always verify changes are pushed to GitHub first** - The VM pulls from the remote repository
- **The Python server runs as www-data** - Don't change ownership of files
- **Nginx acts as reverse proxy** - Port 80/443 → 8080 (Python server)
- **SSL/TLS is handled by nginx** - Let's Encrypt certificate auto-renews
- **Server directory:** `/var/www/portfolio`
- **Log file:** `/var/log/portfolio-server.log`

## Architecture

```
Internet (HTTPS)
    ↓
Nginx (port 80/443) - SSL termination
    ↓
Python server (port 8080) - Static files
```

For API-enabled dashboards:
```
Internet (HTTPS)
    ↓
Nginx (port 80/443)
    ├→ Python server (port 8080) - Static files
    └→ Flask API (port 5001) - Backend API at /api/*
```
