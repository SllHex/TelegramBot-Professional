# Deployment Guide

This guide covers multiple deployment options for the Telegram bot, from simple VPS deployment to advanced containerized solutions.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Bot token from [@BotFather](https://t.me/BotFather)
- ✅ Admin user ID(s)
- ✅ Google Gemini API key (optional)
- ✅ Payment provider token (optional)
- ✅ Tested bot locally
- ✅ All dependencies in `requirements.txt`
- ✅ Environment variables configured

---

## 🖥️ Option 1: VPS Deployment (Recommended)

Deploy on a Virtual Private Server (Ubuntu, Debian, CentOS, etc.)

### Prerequisites

- Ubuntu 20.04+ or Debian 10+ server
- Root or sudo access
- Domain name (optional, for webhooks)

### Step-by-Step Guide

#### 1. Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3 python3-pip python3-venv -y

# Install git
sudo apt install git -y

# Optional: Install screen for persistent sessions
sudo apt install screen -y
```

#### 2. Clone and Setup Bot

```bash
# Create bot directory
cd /opt
sudo mkdir telegram-bot
sudo chown $USER:$USER telegram-bot
cd telegram-bot

# Clone repository
git clone https://github.com/SllHex/TelegramBot-Professional.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Create .env file
nano .env
```

Add your configuration:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_USER_IDS=123456789
GEMINI_API_KEY=your_gemini_key
DEBUG_MODE=False
MAX_FILE_SIZE_MB=10
```

Save with `Ctrl+O`, exit with `Ctrl+X`.

#### 4. Test the Bot

```bash
# Run bot to test
python main.py
```

If you see "✅ Bot started successfully!", press `Ctrl+C` to stop.

#### 5. Run with Screen (Simple Method)

```bash
# Start screen session
screen -S telegram-bot

# Activate virtual environment
cd /opt/telegram-bot
source venv/bin/activate

# Run bot
python main.py

# Detach from screen: Press Ctrl+A, then D
# Reattach: screen -r telegram-bot
# List screens: screen -ls
```

#### 6. Run as Systemd Service (Production Method)

Create service file:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add configuration:
```ini
[Unit]
Description=Telegram Bot Showcase
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable telegram-bot

# Start service
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

#### 7. Useful Commands

```bash
# Stop bot
sudo systemctl stop telegram-bot

# Restart bot
sudo systemctl restart telegram-bot

# View last 100 log lines
sudo journalctl -u telegram-bot -n 100

# Follow logs in real-time
sudo journalctl -u telegram-bot -f
```

### Updating the Bot

```bash
# Stop service
sudo systemctl stop telegram-bot

# Pull latest changes
cd /opt/telegram-bot
git pull

# Activate venv and update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Start service
sudo systemctl start telegram-bot
```

---

## 🐳 Option 2: Docker Deployment

Deploy using Docker containers for isolation and portability.

### Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose (optional, recommended)

### Single Container Deployment

#### 1. Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "main.py"]
```

#### 2. Build and Run

```bash
# Build image
docker build -t telegram-bot .

# Run container
docker run -d \
  --name telegram-bot \
  --env-file .env \
  --restart unless-stopped \
  telegram-bot

# View logs
docker logs -f telegram-bot

# Stop container
docker stop telegram-bot

# Start container
docker start telegram-bot
```

### Docker Compose Deployment

#### 1. Create docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: telegram-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./bot_database.db:/app/bot_database.db
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 2. Deploy

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop bot
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Advanced: Multi-Container Setup

For production with database and Redis:

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: telegram-bot
    restart: unless-stopped
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    networks:
      - bot-network

  postgres:
    image: postgres:14-alpine
    container_name: telegram-bot-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: telegram_bot
      POSTGRES_USER: botuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - bot-network

  redis:
    image: redis:7-alpine
    container_name: telegram-bot-redis
    restart: unless-stopped
    networks:
      - bot-network

volumes:
  postgres-data:

networks:
  bot-network:
    driver: bridge
```

---

## ☁️ Option 3: Heroku Deployment

Deploy to Heroku's free tier (or paid plans for better performance).

### Prerequisites

- Heroku account ([Sign up](https://signup.heroku.com/))
- Heroku CLI installed ([Install](https://devcenter.heroku.com/articles/heroku-cli))

### Deployment Steps

#### 1. Prepare Application

Create `Procfile`:
```
worker: python main.py
```

Create `runtime.txt`:
```
python-3.9.18
```

#### 2. Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-bot-name

# Set environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMIN_USER_IDS=your_id
heroku config:set GEMINI_API_KEY=your_key

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

#### 3. Manage Application

```bash
# View status
heroku ps

# Restart bot
heroku restart

# Stop bot
heroku ps:scale worker=0

# Start bot
heroku ps:scale worker=1
```

### Limitations

- Free tier has limited hours per month
- Dynos sleep after 30 minutes of inactivity (not ideal for bots)
- Consider paid tier for persistent running

---

## 🚀 Option 4: Railway Deployment

Modern platform with free tier, ideal for bots.

### Prerequisites

- Railway account ([Sign up](https://railway.app/))
- GitHub account (for repository linking)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [Railway](https://railway.app/)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python and installs dependencies

3. **Set Environment Variables**
   - Go to project settings
   - Add variables:
     - `BOT_TOKEN`
     - `ADMIN_USER_IDS`
     - `GEMINI_API_KEY`

4. **Deploy**
   - Railway automatically deploys
   - View logs in dashboard
   - Bot starts automatically

### Advantages

- Free tier with generous limits
- Always-on (no sleeping)
- Automatic deployments on git push
- Built-in logging and monitoring

---

## 🌐 Option 5: Webhooks (Advanced)

Use webhooks instead of polling for better performance.

### Prerequisites

- Domain name with SSL certificate
- Web server (nginx/apache) or reverse proxy

### Implementation

#### 1. Modify Bot Code

```python
from telegram.ext import Application

async def start_webhook(application: Application):
    """Start bot with webhooks"""
    await application.bot.set_webhook(
        url=f"https://yourdomain.com/{BOT_TOKEN}",
        drop_pending_updates=True
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers here...
    
    # Start webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path=BOT_TOKEN,
        webhook_url=f"https://yourdomain.com/{BOT_TOKEN}"
    )
```

#### 2. Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /your_bot_token {
        proxy_pass http://localhost:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. Benefits

- Lower latency
- Reduced server load
- No polling overhead
- Instant message delivery

---

## 📊 Monitoring and Maintenance

### Logging

#### Configure Logging

```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

#### Log Rotation

```bash
# Install logrotate
sudo apt install logrotate

# Create config
sudo nano /etc/logrotate.d/telegram-bot
```

Add configuration:
```
/opt/telegram-bot/bot.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 your-username your-username
}
```

### Monitoring Scripts

#### Health Check Script

```bash
#!/bin/bash
# check_bot.sh

if ! systemctl is-active --quiet telegram-bot; then
    echo "Bot is down! Restarting..."
    systemctl start telegram-bot
    
    # Send alert (optional)
    curl -X POST "https://api.telegram.com/bot$BOT_TOKEN/sendMessage" \
         -d "chat_id=$ADMIN_ID" \
         -d "text=⚠️ Bot was down and has been restarted"
fi
```

Make executable and add to cron:
```bash
chmod +x check_bot.sh
crontab -e

# Add line (check every 5 minutes)
*/5 * * * * /opt/telegram-bot/check_bot.sh
```

### Backup Strategy

#### Backup Script

```bash
#!/bin/bash
# backup_bot.sh

BACKUP_DIR="/backups/telegram-bot"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp /opt/telegram-bot/bot_database.db $BACKUP_DIR/db_$DATE.db

# Backup .env
cp /opt/telegram-bot/.env $BACKUP_DIR/env_$DATE

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.db" -mtime +30 -delete
```

Add to cron (daily at 2 AM):
```bash
0 2 * * * /opt/telegram-bot/backup_bot.sh
```

---

## 🔧 Troubleshooting

### Common Issues

#### Bot Not Starting

```bash
# Check logs
sudo journalctl -u telegram-bot -n 50

# Common causes:
# - Invalid bot token
# - Missing dependencies
# - Port already in use
# - File permission issues
```

#### Database Errors

```bash
# Check database file permissions
ls -l /opt/telegram-bot/bot_database.db

# Fix permissions
chmod 644 /opt/telegram-bot/bot_database.db
```

#### Memory Issues

```bash
# Check memory usage
free -h

# Restart bot to free memory
sudo systemctl restart telegram-bot
```

### Performance Optimization

#### 1. Use Connection Pooling

```python
from telegram.ext import Application

application = (
    Application.builder()
    .token(BOT_TOKEN)
    .concurrent_updates(True)
    .build()
)
```

#### 2. Implement Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_data(user_id: int):
    return db.get_user(user_id)
```

#### 3. Optimize Database Queries

```python
# Use indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON activity_logs(user_id)')

# Batch operations
cursor.executemany('INSERT INTO logs VALUES (?, ?)', data_batch)
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

For high-traffic bots:

1. **Load Balancer**: Distribute requests across multiple instances
2. **Message Queue**: Use Redis/RabbitMQ for task distribution
3. **Database**: Migrate to PostgreSQL with connection pooling
4. **Caching**: Implement Redis for session data

### Vertical Scaling

For single-instance optimization:

1. **Increase server resources** (RAM, CPU)
2. **Optimize code** (async operations, caching)
3. **Use webhooks** instead of polling
4. **Database tuning** (indexes, query optimization)

---

## 🔐 Security Checklist

- ✅ Use environment variables for secrets
- ✅ Enable firewall (allow only necessary ports)
- ✅ Keep dependencies updated
- ✅ Use HTTPS for webhooks
- ✅ Implement rate limiting
- ✅ Regular security audits
- ✅ Monitor logs for suspicious activity
- ✅ Backup data regularly

---

## 📚 Additional Resources

- [Telegram Bot API Best Practices](https://core.telegram.org/bots/best-practices)
- [Python Telegram Bot Examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)
- [Systemd Service Guide](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

Need help with deployment? Check the documentation or reach out for support!
