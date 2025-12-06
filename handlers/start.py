from telegram import Update
from telegram.ext import ContextTypes
from config import MESSAGES
from utils.keyboards import get_main_menu_keyboard, get_back_button
from utils.decorators import track_user_activity, log_command, handle_errors
from database import db
from datetime import datetime

@handle_errors
@track_user_activity
@log_command('start')
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - show welcome message and main menu"""
    user = update.effective_user
    
    import asyncio
    
    # Beautiful animated progress bar with emojis
    frames = [
        ("⚡ <b>Starting Bot...</b>\n\n🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜ 10%", 0.15),
        ("⚡ <b>Loading Features...</b>\n\n🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜ 30%", 0.15),
        ("🤖 <b>Activating AI...</b>\n\n🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜ 50%", 0.15),
        ("🎨 <b>Loading File Tools...</b>\n\n🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜ 70%", 0.15),
        ("💳 <b>Initializing Payments...</b>\n\n🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜ 90%", 0.15),
        ("✅ <b>Ready!</b>\n\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%", 0.3),
    ]
    
    # Send first frame
    welcome_msg = await update.message.reply_text(frames[0][0], parse_mode='HTML')
    
    # Animate through frames
    for frame_text, delay in frames[1:]:
        try:
            await asyncio.sleep(delay)
            await welcome_msg.edit_text(frame_text, parse_mode='HTML')
        except:
            pass
    
    await asyncio.sleep(0.4)
    
    # Final welcome message
    welcome_text = MESSAGES['welcome']
    
    await welcome_msg.edit_text(
        welcome_text,
        parse_mode='HTML',
        reply_markup=get_main_menu_keyboard()
    )

@handle_errors
@track_user_activity
@log_command('help')
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        MESSAGES['help'],
        parse_mode='HTML',
        reply_markup=get_back_button()
    )

@handle_errors
@track_user_activity
@log_command('profile')
async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /profile command - show user profile"""
    user = update.effective_user
    user_data = db.get_user(user.id)
    user_stats = db.get_user_stats(user.id)
    
    if not user_data:
        await update.message.reply_text("Error loading profile. Please try /start first.")
        return
    
    # Format join date
    join_date = user_data.get('join_date', 'Unknown')
    if join_date != 'Unknown':
        try:
            dt = datetime.fromisoformat(join_date)
            join_date = dt.strftime('%b %d, %Y')
        except:
            pass
    
    profile_text = MESSAGES['profile'].format(
        user_id=user.id,
        username=user.username or 'Not set',
        first_name=user.first_name or 'User',
        join_date=join_date,
        message_count=user_stats.get('message_count', 0),
        file_count=user_stats.get('file_count', 0),
        ai_count=user_stats.get('ai_count', 0)
    )
    
    await update.message.reply_text(
        profile_text,
        parse_mode='HTML',
        reply_markup=get_back_button()
    )

@handle_errors
@track_user_activity
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)
    
    stats_text = f"""
📊 <b>Your Statistics</b>

<b>Activity Overview:</b>
├ Total Messages: {stats.get('message_count', 0)}
├ Files Processed: {stats.get('file_count', 0)}
├ AI Requests: {stats.get('ai_count', 0)}
└ Payments Made: {stats.get('payment_count', 0)}

Keep exploring to unlock more features! 🚀
    """
    
    # Check if called from callback or message
    if update.callback_query:
        query = update.callback_query
        try:
            await query.edit_message_text(
                stats_text,
                parse_mode='HTML',
                reply_markup=get_back_button()
            )
        except:
            await query.message.reply_text(
                stats_text,
                parse_mode='HTML',
                reply_markup=get_back_button()
            )
    else:
        await update.message.reply_text(
            stats_text,
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
