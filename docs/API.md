# API Integration Guide

This document provides detailed information about the external APIs integrated into the bot and how to use them.

---

## 🤖 Google Gemini API

### Overview

Google Gemini is a powerful, free AI API that powers all AI features in this bot.

### Getting Started

1. **Get API Key** (Free)
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with Google account
   - Click "Create API Key"
   - Copy your key

2. **Add to Environment**
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Usage Limits (Free Tier)**
   - 60 requests per minute
   - Generous daily quota
   - No credit card required

### Implementation

#### Text Generation

```python
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure API
genai.configure(api_key=GEMINI_API_KEY)

# Create model
model = genai.GenerativeModel('gemini-pro')

# Generate text
async def generate_text(prompt: str) -> str:
    """Generate text using Gemini AI"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None
```

#### Image Generation

```python
# For image generation
model = genai.GenerativeModel('gemini-pro-vision')

async def generate_image(prompt: str) -> bytes:
    """Generate image from text description"""
    try:
        response = model.generate_content([prompt])
        return response.image_data
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return None
```

#### Safety Settings

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

response = model.generate_content(
    prompt,
    safety_settings=safety_settings
)
```

### Error Handling

```python
from google.api_core import exceptions

async def safe_generate(prompt: str) -> str:
    """Generate with error handling"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except exceptions.ResourceExhausted:
        return "⚠️ API quota exceeded. Please try again later."
    except exceptions.InvalidArgument:
        return "❌ Invalid prompt. Please rephrase your request."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "❌ An error occurred. Please try again."
```

### Best Practices

1. **Rate Limiting**
   - Implement client-side rate limiting
   - Queue requests during high traffic
   - Cache common responses

2. **Prompt Engineering**
   - Be specific and clear
   - Include context
   - Set appropriate length limits

3. **Cost Management**
   - Monitor API usage
   - Set up quotas
   - Implement fallbacks

---

## 📱 Telegram Bot API

### Overview

This bot uses `python-telegram-bot` v20+, which provides async/await support and comprehensive features.

### Installation

```bash
pip install python-telegram-bot>=20.0
```

### Basic Setup

```python
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Create application
application = Application.builder().token(BOT_TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT, handle_message))

# Run bot
application.run_polling()
```

### Advanced Features

#### Inline Keyboards

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Option 1", callback_data='opt1')],
    [InlineKeyboardButton("Option 2", callback_data='opt2')],
]
reply_markup = InlineKeyboardMarkup(keyboard)

await update.message.reply_text(
    "Choose an option:",
    reply_markup=reply_markup
)
```

#### Callback Query Handling

```python
from telegram.ext import CallbackQueryHandler

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    if query.data == 'opt1':
        await query.edit_message_text("You selected Option 1")

application.add_handler(CallbackQueryHandler(button_callback))
```

#### File Handling

```python
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads"""
    document = update.message.document
    
    # Get file
    file = await context.bot.get_file(document.file_id)
    
    # Download file
    file_path = await file.download_to_drive()
    
    # Process file
    # ...
    
    await update.message.reply_text(f"Processed: {document.file_name}")

application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
```

#### Sending Files

```python
# Send photo
await update.message.reply_photo(
    photo=open('image.jpg', 'rb'),
    caption="Here's your image!"
)

# Send document
await update.message.reply_document(
    document=open('file.pdf', 'rb'),
    filename='document.pdf'
)
```

#### Error Handling

```python
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f'Update {update} caused error {context.error}')
    
    # Notify user
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Our team has been notified."
        )

application.add_error_handler(error_handler)
```

### Rate Limiting

```python
from functools import wraps
import time

user_last_request = {}
RATE_LIMIT = 30  # messages
TIME_WINDOW = 60  # seconds

def rate_limit(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        current_time = time.time()
        
        if user_id in user_last_request:
            time_passed = current_time - user_last_request[user_id]['time']
            if time_passed < TIME_WINDOW:
                if user_last_request[user_id]['count'] >= RATE_LIMIT:
                    await update.message.reply_text(
                        "⚠️ Too many requests. Please wait."
                    )
                    return
                user_last_request[user_id]['count'] += 1
            else:
                user_last_request[user_id] = {'time': current_time, 'count': 1}
        else:
            user_last_request[user_id] = {'time': current_time, 'count': 1}
        
        return await func(update, context)
    return wrapper

@rate_limit
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your command logic
    pass
```

---

## 💳 Telegram Payments API

### Overview

Telegram supports native payment processing with various providers.

### Supported Providers

- **Stripe** (Recommended)
- **PayPal**
- **Telegram Stars** (in-app currency)
- Custom payment gateways

### Setup with Stripe

1. **Get Stripe Token**
   - Create [Stripe account](https://stripe.com)
   - Get publishable key
   - Talk to [@BotFather](https://t.me/BotFather)
   - Use `/mybots` → Select bot → `Payments`
   - Enter Stripe token

2. **Configure in Bot**
   ```env
   PAYMENT_PROVIDER_TOKEN=your_stripe_token
   ```

### Implementation

#### Send Invoice

```python
from telegram import LabeledPrice

async def send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send payment invoice"""
    
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Premium Plan",
        description="Unlock all premium features",
        payload="premium_plan_001",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="USD",
        prices=[LabeledPrice("Premium Subscription", 999)],  # $9.99
        start_parameter="premium-plan",
        photo_url="https://example.com/product-image.jpg",
        photo_width=640,
        photo_height=480
    )
```

#### Handle Pre-Checkout

```python
from telegram.ext import PreCheckoutQueryHandler

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate payment before processing"""
    query = update.pre_checkout_query
    
    # Validation logic
    if query.invoice_payload == 'premium_plan_001':
        await query.answer(ok=True)
    else:
        await query.answer(
            ok=False,
            error_message="Invalid payment. Please contact support."
        )

application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
```

#### Handle Successful Payment

```python
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process successful payment"""
    payment = update.message.successful_payment
    
    # Update user subscription in database
    db.update_user_subscription(
        user_id=update.effective_user.id,
        plan='premium',
        transaction_id=payment.telegram_payment_charge_id
    )
    
    await update.message.reply_text(
        "✅ Payment successful! Your premium features are now active."
    )

application.add_handler(MessageHandler(
    filters.SUCCESSFUL_PAYMENT,
    successful_payment
))
```

### Payment Object Structure

```python
{
    'currency': 'USD',
    'total_amount': 999,  # in cents
    'invoice_payload': 'premium_plan_001',
    'telegram_payment_charge_id': 'tg_charge_xxx',
    'provider_payment_charge_id': 'stripe_charge_xxx'
}
```

---

## 🗄️ Database Integration

### SQLite (Current)

```python
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                join_date TIMESTAMP,
                message_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str, first_name: str):
        """Add new user"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, join_date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, datetime.now()))
        self.conn.commit()
```

### PostgreSQL Migration (Optional)

For production deployments, consider PostgreSQL:

```python
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresDatabase:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(
            connection_string,
            cursor_factory=RealDictCursor
        )
    
    async def add_user(self, user_id: int, username: str):
        """Add user asynchronously"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (user_id, username)
        )
        self.conn.commit()
```

---

## 📊 Analytics Integration

### Custom Analytics

```python
import json
from datetime import datetime

class Analytics:
    def __init__(self):
        self.events = []
    
    def track_event(self, user_id: int, event_type: str, data: dict = None):
        """Track user event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'event_type': event_type,
            'data': data or {}
        }
        self.events.append(event)
        self.save_to_file()
    
    def save_to_file(self):
        """Save events to JSON file"""
        with open('analytics.json', 'w') as f:
            json.dump(self.events, f, indent=2)

# Usage
analytics = Analytics()
analytics.track_event(user_id=123, event_type='command_used', data={'command': '/start'})
```

### Google Analytics Integration

```python
import requests

class GoogleAnalytics:
    def __init__(self, tracking_id: str):
        self.tracking_id = tracking_id
        self.endpoint = "https://www.google-analytics.com/collect"
    
    def track_event(self, user_id: int, category: str, action: str):
        """Send event to Google Analytics"""
        data = {
            'v': '1',
            'tid': self.tracking_id,
            'cid': str(user_id),
            't': 'event',
            'ec': category,
            'ea': action
        }
        requests.post(self.endpoint, data=data)

# Usage
ga = GoogleAnalytics('UA-XXXXX-Y')
ga.track_event(user_id=123, category='Bot Command', action='Start')
```

---

## 🔐 Security Best Practices

### 1. Environment Variables

Never commit sensitive data:

```python
# ❌ Bad - Hardcoded credentials
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# ✅ Good - Environment variables
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
```

### 2. Input Validation

```python
import re

def sanitize_input(text: str) -> str:
    """Remove potentially harmful characters"""
    # Remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()
```

### 3. Rate Limiting

Prevent abuse with rate limits (shown earlier in Telegram API section).

### 4. Admin Authentication

```python
def admin_only(func):
    """Decorator for admin-only commands"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in ADMIN_USER_IDS:
            await update.message.reply_text("❌ Unauthorized. Admin only.")
            return
        return await func(update, context)
    return wrapper

@admin_only
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Admin logic here
    pass
```

---

## 🔄 API Best Practices

### 1. Async/Await

Use async operations for better performance:

```python
# ✅ Good - Async
async def process_request():
    result = await api_call()
    return result

# ❌ Bad - Blocking
def process_request():
    result = api_call()  # Blocks execution
    return result
```

### 2. Error Handling

Always handle API errors:

```python
async def safe_api_call():
    try:
        result = await external_api()
        return result
    except ConnectionError:
        logger.error("API connection failed")
        return None
    except TimeoutError:
        logger.error("API timeout")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### 3. Caching

Cache API responses when appropriate:

```python
from functools import lru_cache
import time

cache = {}
CACHE_DURATION = 3600  # 1 hour

async def cached_api_call(key: str):
    """API call with caching"""
    if key in cache:
        cached_data, timestamp = cache[key]
        if time.time() - timestamp < CACHE_DURATION:
            return cached_data
    
    # Call API
    data = await api_call(key)
    cache[key] = (data, time.time())
    return data
```

### 4. Retry Logic

Implement retries for transient failures:

```python
import asyncio

async def api_call_with_retry(max_retries=3):
    """API call with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await api_call()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            await asyncio.sleep(wait_time)
```

---

## 📚 Additional Resources

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Stripe Payment Integration](https://stripe.com/docs/payments)

---

## 💡 Tips and Tricks

1. **Logging**: Always log API requests for debugging
2. **Monitoring**: Set up alerts for API errors
3. **Testing**: Test with small requests before deploying
4. **Documentation**: Keep API documentation updated
5. **Versioning**: Pin API versions in production

---

Need help? Check the documentation or contact support!
