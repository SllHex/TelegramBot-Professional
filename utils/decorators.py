from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_USER_IDS, RATE_LIMIT_MESSAGES, RATE_LIMIT_SECONDS
from database import db
from datetime import datetime, timedelta
import time

# Rate limiting storage
user_message_times = {}

def admin_only(func):
    """Decorator to restrict command to admin users only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_USER_IDS:
            await update.message.reply_text(
                "❌ <b>Access Denied</b>\n\n"
                "This command is only available to administrators.",
                parse_mode='HTML'
            )
            return
        
        return await func(update, context)
    return wrapper

def track_user_activity(func):
    """Decorator to track user activity"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        # Update user in database
        db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code or 'en'
        )
        
        # Update last active
        db.update_last_active(user.id)
        
        return await func(update, context)
    return wrapper

def rate_limit(func):
    """Decorator to implement rate limiting"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        current_time = time.time()
        
        # Initialize user's message times if not exists
        if user_id not in user_message_times:
            user_message_times[user_id] = []
        
        # Remove old timestamps
        user_message_times[user_id] = [
            t for t in user_message_times[user_id] 
            if current_time - t < RATE_LIMIT_SECONDS
        ]
        
        # Check if rate limit exceeded
        if len(user_message_times[user_id]) >= RATE_LIMIT_MESSAGES:
            await update.message.reply_text(
                f"⚠️ <b>Rate Limit Exceeded</b>\n\n"
                f"Please wait a moment before sending more messages.\n"
                f"Limit: {RATE_LIMIT_MESSAGES} messages per {RATE_LIMIT_SECONDS} seconds.",
                parse_mode='HTML'
            )
            return
        
        # Add current timestamp
        user_message_times[user_id].append(current_time)
        
        return await func(update, context)
    return wrapper

def log_command(command_name: str):
    """Decorator to log command usage"""
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            db.log_message(user_id, command_name)
            db.increment_stat(user_id, 'message_count')
            return await func(update, context)
        return wrapper
    return decorator

def handle_errors(func):
    """Decorator to handle errors gracefully"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(update, context)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            
            error_message = (
                f"❌ <b>An Error Occurred</b>\n\n"
                f"Something went wrong while processing your request.\n"
                f"Please try again later or contact support.\n\n"
                f"<i>Error details have been logged.</i>"
            )
            
            if update.message:
                await update.message.reply_text(error_message, parse_mode='HTML')
            elif update.callback_query:
                await update.callback_query.answer("An error occurred. Please try again.")
                await update.callback_query.message.reply_text(error_message, parse_mode='HTML')
    return wrapper
