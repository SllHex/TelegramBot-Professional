import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_IDS = [int(id.strip()) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id.strip()]

# AI Configuration (Google Gemini - FREE)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ENABLE_AI_FEATURES = bool(GEMINI_API_KEY)

# Payment Configuration
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')
ENABLE_PAYMENT_DEMO = bool(PAYMENT_PROVIDER_TOKEN)

# Bot Settings
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 10))
RATE_LIMIT_MESSAGES = int(os.getenv('RATE_LIMIT_MESSAGES', 30))
RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', 60))

# Database
DATABASE_PATH = 'bot_database.db'

# Bot Messages (all in English)
MESSAGES = {
    'welcome': """
🎉 <b>Welcome to Professional Bot Showcase!</b>

This bot demonstrates cutting-edge capabilities:

🤖 <b>AI Features</b>
├ Text generation & analysis
├ Image creation
└ Smart responses

📁 <b>File Processing</b>
├ PDF text extraction
├ Image optimization
└ Format conversion

📊 <b>Analytics & Admin</b>
├ User statistics
├ Feature tracking
└ Broadcast system

💳 <b>Payment Integration</b>
└ Complete payment flow demo

ℹ️ <b>Note:</b> All features are fully functional!
Some run in demo mode to showcase capabilities.

👇 <b>Choose an option below to explore!</b>
    """,
    
    'help': """
📚 <b>Help & Commands</b>

<b>Main Commands:</b>
/start - Show main menu
/help - This help message
/profile - View your profile
/stats - Your statistics

<b>Features:</b>
🤖 AI Tools - Generate text & images
📁 File Tools - Process documents
💳 Payments - Demo payment flow
⚙️ Settings - Customize preferences

<b>Admin Commands:</b> (Admin only)
/admin - Admin dashboard
/broadcast - Send broadcast message
/users - User management

Need assistance? Contact support!
    """,
    
    'profile': """
👤 <b>Your Profile</b>

<b>User ID:</b> {user_id}
<b>Username:</b> @{username}
<b>Name:</b> {first_name}
<b>Member Since:</b> {join_date}

📊 <b>Statistics:</b>
├ Messages Sent: {message_count}
├ Files Processed: {file_count}
└ AI Requests: {ai_count}

⚙️ Use /settings to customize your experience
    """,
    
    'admin_panel': """
🛡️ <b>Admin Dashboard</b>

📊 <b>Bot Statistics:</b>
├ Total Users: {total_users}
├ Active Today: {active_today}
├ Total Messages: {total_messages}
└ Files Processed: {total_files}

📈 <b>Recent Activity:</b>
├ New Users (24h): {new_users_24h}
├ Messages (24h): {messages_24h}
└ Peak Hour: {peak_hour}

Choose an admin action below:
    """,
}

# Emoji Constants
EMOJI = {
    'robot': '🤖',
    'file': '📁',
    'payment': '💳',
    'settings': '⚙️',
    'stats': '📊',
    'help': '❓',
    'back': '🔙',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'loading': '⏳',
    'admin': '🛡️',
}
