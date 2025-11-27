# Deployment Guide

## Production Deployment

### Backend Deployment (Heroku Example)

#### 1. Install Heroku CLI

```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli.heroku.com/install.sh | sh
```

#### 2. Prepare Backend for Heroku

Create `Procfile` in backend directory:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

Create `runtime.txt`:
```
python-3.10.0
```

#### 3. Deploy to Heroku

```bash
cd backend

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run python init_db.py

# View logs
heroku logs --tail
```

### Frontend Deployment (Vercel Example)

#### 1. Deploy to Vercel

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

Or connect GitHub repo in Vercel dashboard for automatic deployments.

#### 2. Configure Environment

Create `vercel.json`:
```json
{
  "env": {
    "REACT_APP_API_URL": "@api_url"
  }
}
```

Set environment variables in Vercel dashboard.

### Database Setup for Production

#### 1. Using PostgreSQL (Recommended)

```bash
# Create PostgreSQL database
psql -U postgres

# In psql console:
CREATE DATABASE hm_recommender;
CREATE USER hm_user WITH PASSWORD 'secure_password';
ALTER ROLE hm_user SET client_encoding TO 'utf8';
ALTER ROLE hm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hm_user SET default_transaction_deferrable TO on;
ALTER ROLE hm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hm_recommender TO hm_user;
```

#### 2. Update Database URI in Flask

Edit `app.py`:
```python
# Before:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'

# After:
import os
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://hm_user:password@localhost/hm_recommender')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

#### 3. Initialize Production Database

```bash
python init_db.py
```

## Docker Deployment

### 1. Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
```

### 3. Docker Compose

Create `docker-compose.yml` in project root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://hm_user:password@db:5432/hm_recommender
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./backend/images:/app/images
      - ./backend/static:/app/static

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=hm_recommender
      - POSTGRES_USER=hm_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### 4. Run with Docker Compose

```bash
# Start all services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
```

## AWS Deployment

### 1. EC2 Instance Setup

```bash
# SSH into instance
ssh -i key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install Python and Node
sudo yum install python3 python3-pip nodejs npm -y

# Clone repository
git clone https://github.com/your-username/hm-recommender.git
cd hm-recommender
```

### 2. Install RDS Database

1. Create RDS PostgreSQL instance in AWS console
2. Get connection string
3. Set environment variable:
   ```bash
   export DATABASE_URL=postgresql://user:password@rds-instance.amazonaws.com/hm_recommender
   ```

### 3. Deploy Backend with Gunicorn + Nginx

```bash
# Install Nginx
sudo yum install nginx -y

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Install Gunicorn
pip3 install gunicorn

# Create systemd service for backend
sudo nano /etc/systemd/system/hm-recommender.service
```

Service file content:
```ini
[Unit]
Description=H&M Recommender Backend
After=network.target

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/hm-recommender/backend
Environment="PATH=/home/ec2-user/.local/bin"
ExecStart=/home/ec2-user/.local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

```bash
sudo nano /etc/nginx/conf.d/hm-recommender.conf
```

Configuration:
```nginx
upstream hm_recommender {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://hm_recommender;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/ec2-user/hm-recommender/backend/static;
    }

    location /images {
        alias /home/ec2-user/hm-recommender/backend/images;
    }
}
```

### 5. Start Services

```bash
# Start backend service
sudo systemctl start hm-recommender
sudo systemctl enable hm-recommender

# Reload Nginx
sudo systemctl reload nginx
```

## SSL/HTTPS Setup

### Using Let's Encrypt with Certbot

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot-renew
```

## Monitoring & Logging

### Backend Logging

```python
# In app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/hm_recommender.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('H&M Recommender startup')
```

### Performance Monitoring

```bash
# Install monitoring tools
pip install prometheus-client
pip install gunicorn-exporter
```

## Backup Strategy

### Database Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump postgresql://user:password@localhost/hm_recommender > \
  $BACKUP_DIR/hm_recommender_$TIMESTAMP.sql

# Keep only last 7 days
find $BACKUP_DIR -name "hm_recommender_*.sql" -mtime +7 -delete
```

### Image Backups

```bash
# Backup product images
rsync -av ./backend/images/ /backup/images/
```

## Rollback Procedure

```bash
# If deployment fails, rollback to previous version
git revert <commit-hash>
git push heroku main

# Or restart previous version
heroku releases
heroku rollback v<number>
```

## Health Checks

### Add health check endpoint

```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })
```

### Configure monitoring

- AWS CloudWatch
- Datadog
- New Relic
- Sentry (error tracking)

## Troubleshooting

### Port already in use
```bash
# Find process on port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database connection issues
```bash
# Test connection
psql postgresql://user:password@host/database

# Check logs
heroku logs --tail
```

### Frontend not connecting to backend
- Check CORS settings
- Verify API_URL environment variable
- Check proxy in package.json

## Security Checklist

- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Set up monitoring and alerts
- [ ] Use rate limiting on API
- [ ] Implement request logging
- [ ] Keep dependencies updated
- [ ] Use secrets management (AWS Secrets Manager, HashiCorp Vault)

---

For more information, see the main README.md
