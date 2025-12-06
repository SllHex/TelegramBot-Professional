# 🤖 Professional Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg?logo=telegram)](https://t.me/my1testprojectbot)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

A **production-ready**, feature-rich Telegram bot showcasing modern bot development best practices. Built with Python and `python-telegram-bot` library, featuring AI integration, file processing, payment handling, and comprehensive admin controls.

---

## 🎮 Try Live Bot

> **See it in action! Test all features now:**

<div align="center">

[![Try Bot Now](https://img.shields.io/badge/🤖_Try_Bot_Now-Telegram-blue?style=for-the-badge&logo=telegram)](https://t.me/my1testprojectbot)

**[@my1testprojectbot](https://t.me/my1testprojectbot)**

</div>

**What you can test:**
- 🤖 **AI Features** - Text & image generation (Google Gemini + Pollinations.ai)
- 📁 **File Processing** - PDF extraction, image compression
- 💳 **Payment Demo** - Complete payment integration flow
- 📊 **Statistics** - Personal usage tracking & analytics
- ⚙️ **Settings** - Customizable preferences

**Quick start:** Send `/start` command to begin exploring!

---

## ✨ Key Features

### 🤖 AI-Powered Capabilities
- **Text Generation** - Create content using Google Gemini AI
- **Image Creation** - AI-powered image generation
- **Text Summarization** - Intelligent content condensation  
- **Smart Replies** - Context-aware responses

### 📁 File Processing Tools
- **PDF to Text** - Extract text from PDF documents
- **Image Compression** - Optimize images with quality control
- **File Analysis** - Detailed metadata and file information
- **Format Conversion** - Multi-format support

### 💳 Payment Integration
- Complete payment flow demonstration
- Multiple pricing tiers (Premium, Pro, Enterprise)
- Invoice generation and processing
- Transaction tracking and confirmation

### 🛡️ Admin Panel
- **Real-time Analytics** - User metrics and activity tracking
- **User Management** - View and manage all users
- **Broadcast System** - Mass messaging with delivery reports
- **Statistics Dashboard** - Comprehensive bot performance metrics

### 🔧 Technical Excellence
- **Modular Architecture** - Clean, maintainable code
- **Database Integration** - SQLite with efficient schema
- **Error Handling** - Robust recovery and logging
- **Rate Limiting** - Built-in abuse protection
- **Async Operations** - High-performance async/await

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- **Python 3.9+** installed
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
- **Google Gemini API Key** (optional, for AI) - [Get free key](https://makersuite.google.com/app/apikey)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/SllHex/TelegramBot-Professional.git
cd TelegramBot-Professional

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run bot
python main.py
```

### Detailed Installation

1. **Install Dependencies:**
   ```bash
   pip install python-telegram-bot Pillow PyPDF2 google-generativeai requests python-dotenv
   ```

2. **Configure Bot:**
   
   Create `.env` file:
   ```env
   BOT_TOKEN=your_bot_token_from_botfather
   ADMIN_USER_IDS=your_telegram_user_id
   GEMINI_API_KEY=your_gemini_api_key  # Optional
   ```

3. **Get Your User ID:**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Copy your user ID
   - Add to `.env` file

4. **Start Bot:**
   ```bash
   python main.py
   ```

Expected output:
```
🤖 Starting Professional Telegram Bot...
✅ Bot started successfully!
📱 Send /start to begin
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `BOT_TOKEN` | ✅ Yes | Telegram bot token | - |
| `ADMIN_USER_IDS` | ✅ Yes | Admin user IDs (comma-separated) | - |
| `GEMINI_API_KEY` | ❌ No | Google Gemini API key (free) | - |
| `PAYMENT_PROVIDER_TOKEN` | ❌ No | Payment provider token | - |
| `DEBUG_MODE` | ❌ No | Enable debug logging | `False` |
| `MAX_FILE_SIZE_MB` | ❌ No | Max file upload size (MB) | `10` |
| `RATE_LIMIT_MESSAGES` | ❌ No | Messages per time window | `30` |
| `RATE_LIMIT_SECONDS` | ❌ No | Rate limit window (seconds) | `60` |

### Getting API Keys

**Google Gemini (FREE):**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google
3. Create API key
4. Add to `.env`

**Benefits:**
- 60 requests per minute
- Generous monthly quota
- No credit card required

---

## 📖 Usage

### User Commands

| Command | Description |
|---------|-------------|
| `/start` | Launch bot and show main menu |
| `/help` | Display help and commands |
| `/profile` | View your profile and stats |
| `/stats` | Show activity statistics |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/admin` | Access admin dashboard |

### Interactive Features

Navigate using **inline keyboard buttons**:

1. **🤖 AI Features**
   - Generate Text
   - Create Image  
   - Summarize Text
   - Smart Reply

2. **📁 File Tools**
   - PDF to Text
   - Compress Image
   - File Info
   - Format Convert

3. **💳 Payment Demo**
   - Premium Plan
   - Pro Plan
   - Enterprise Plan

4. **📊 My Stats**
   - View usage statistics
   - Track activity

5. **⚙️ Settings**
   - Customize preferences
   - Manage notifications

---

## 📂 Project Structure

```
telegram-bot-professional/
├── Core Files
│   ├── main.py              # Bot entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database operations
│   └── requirements.txt     # Dependencies
│
├── Feature Handlers
│   ├── handlers/
│   │   ├── start.py         # Basic commands
│   │   ├── ai_features.py   # AI functionality
│   │   ├── file_processing.py # File tools
│   │   ├── payment_demo.py  # Payments
│   │   └── admin_panel.py   # Admin controls
│
├── Utilities
│   ├── utils/
│   │   ├── keyboards.py     # UI layouts
│   │   ├── decorators.py    # Custom decorators
│   │   └── loading.py       # Loading states
│
├── Documentation
│   ├── docs/
│   │   ├── API.md          # API integration
│   │   └── DEPLOYMENT.md   # Deployment guide
│
└── Configuration
    ├── .env.example         # Environment template
    ├── .gitignore          # Git ignore rules
    └── LICENSE             # MIT License
```

### Architecture

- **Modular Handlers** - Each feature isolated
- **Centralized Config** - All settings in one place
- **Reusable Utilities** - Common functions shared
- **Clean Separation** - Clear code organization
- **Scalable Design** - Easy to extend

---

## 🌟 Features

### AI Integration

**Text Generation:**
- Powered by Google Gemini API
- Creative content creation
- Question answering
- Context-aware responses

**Image Generation:**
- Free Pollinations.ai integration
- Text-to-image conversion
- High-quality outputs

**Text Summarization:**
- Long document condensation
- Key point extraction
- Smart content analysis

### File Processing

**PDF Tools:**
- Text extraction from PDFs
- Multi-page support
- Character count statistics

**Image Tools:**
- Quality-controlled compression
- Format conversion (JPG, PNG, WEBP)
- Size optimization with stats

**File Analysis:**
- Metadata display
- MIME type detection
- Telegram file ID retrieval

### Payment System

**Demo Flow:**
- Complete payment integration showcase
- Multiple pricing tiers
- Invoice generation
- Payment confirmation
- Transaction tracking

**Pricing Tiers:**
- 💎 Premium - $9.99/month
- 🌟 Pro - $19.99/month  
- 🚀 Enterprise - $49.99/month

### Admin Features

**Dashboard:**
- Total users count
- Active users tracking
- New user metrics
- Message statistics
- File processing logs

**User Management:**
- View all users
- Activity tracking
- User information display

**Broadcasting:**
- Mass message sending
- Delivery tracking
- Success/failure reports

---

## 🛠️ Development

### Running in Development

Enable debug mode:
```env
DEBUG_MODE=True
```

Benefits:
- Detailed logging
- Error stack traces
- Development warnings

### Code Style

Following:
- **PEP 8** Python style guide
- **Type hints** for clarity
- **Docstrings** for documentation
- **Modular design** for maintainability

### Adding Features

1. **Create Handler:**
   ```python
   # handlers/my_feature.py
   async def my_feature_handler(update, context):
       await update.message.reply_text("New feature!")
   ```

2. **Register Handler:**
   ```python
   # main.py
   from handlers.my_feature import my_feature_handler
   application.add_handler(CommandHandler("myfeature", my_feature_handler))
   ```

3. **Add to Menu:**
   ```python
   # utils/keyboards.py
   InlineKeyboardButton("🆕 My Feature", callback_data='my_feature')
   ```

### Database Schema

**Users Table:**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    join_date TIMESTAMP,
    message_count INTEGER DEFAULT 0,
    file_count INTEGER DEFAULT 0,
    ai_count INTEGER DEFAULT 0
);
```

**Activity Logs:**
```sql
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_type TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

## 🌐 Deployment

### Option 1: VPS (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git

# Clone and setup
git clone https://github.com/SllHex/TelegramBot-Professional.git
cd TelegramBot-Professional
pip3 install -r requirements.txt

# Configure
nano .env  # Add credentials

# Run with screen
screen -S telegram-bot
python3 main.py
# Ctrl+A, D to detach
```

### Option 2: Systemd Service

Create `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Option 3: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Run:
```bash
docker build -t telegram-bot .
docker run -d --env-file .env telegram-bot
```

### Option 4: Heroku

1. Create `Procfile`:
   ```
   worker: python main.py
   ```

2. Deploy:
   ```bash
   heroku create
   heroku config:set BOT_TOKEN=your_token
   git push heroku main
   heroku ps:scale worker=1
   ```

For detailed deployment guides, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🤝 Contributing

Contributions welcome! Here's how:

### Reporting Issues

1. Check existing issues
2. Use issue templates
3. Provide detailed description
4. Include error logs

### Pull Requests

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

### Guidelines

- Follow PEP 8
- Add docstrings
- Update documentation
- Test changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

See [LICENSE](LICENSE) file for full text.

---

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Google Gemini](https://ai.google.dev/) - AI capabilities
- [Pollinations.ai](https://pollinations.ai/) - Free image generation
- [Pillow](https://python-pillow.org/) - Image processing
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF manipulation

---

## 📞 Support

- **Try Bot**: [@my1testprojectbot](https://t.me/my1testprojectbot)
- **Documentation**: See `/docs` directory
- **Issues**: Use GitHub Issues for bug reports
- **Questions**: GitHub Discussions for Q&A

---

## 🗺️ Roadmap

### Current Features (v1.0)
- ✅ AI text & image generation
- ✅ File processing tools
- ✅ Payment integration demo
- ✅ Admin panel
- ✅ User statistics

### Planned Features
- [ ] Multi-language support
- [ ] Voice message transcription
- [ ] Advanced analytics
- [ ] Webhook deployment
- [ ] Redis caching
- [ ] PostgreSQL support
- [ ] Custom AI training
- [ ] Group chat features

---

## ⭐ Show Your Support

If you find this project useful:
- ⭐ Star the repository
- 🍴 Fork for your projects
- 📢 Share with others
- 💬 Provide feedback

---

<div align="center">

**Built with ❤️ using Python & Telegram Bot API**

**[🤖 Try Bot](https://t.me/my1testprojectbot) | [📚 Docs](docs/) | [🚀 Deploy](docs/DEPLOYMENT.md)**

</div>
