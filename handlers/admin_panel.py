from telegram import Update
from telegram.ext import ContextTypes
from config import MESSAGES, EMOJI, ADMIN_USER_IDS
from utils.keyboards import get_admin_keyboard, get_back_button
from utils.decorators import admin_only, handle_errors
from database import db
from datetime import datetime

@handle_errors
@admin_only
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel"""
    stats = get_bot_statistics()
    
    admin_text = MESSAGES['admin_panel'].format(**stats)
    
    await update.message.reply_text(
        admin_text,
        parse_mode='HTML',
        reply_markup=get_admin_keyboard()
    )

@handle_errors
async def admin_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed bot statistics"""
    query = update.callback_query
    
    # Verify admin
    if query.from_user.id not in ADMIN_USER_IDS:
        await query.answer("Access denied!", show_alert=True)
        return
    
    await query.answer()
    
    stats = get_bot_statistics()
    
    detailed_stats = f"""
📊 <b>Detailed Bot Statistics</b>

👥 <b>User Metrics:</b>
├ Total Users: {stats['total_users']}
├ Active Today: {stats['active_today']}
├ New Users (24h): {stats['new_users_24h']}
└ Growth Rate: {_calculate_growth_rate()}%

💬 <b>Message Statistics:</b>
├ Total Messages: {stats['total_messages']}
├ Messages (24h): {stats['messages_24h']}
└ Avg per User: {stats['total_messages'] / max(stats['total_users'], 1):.1f}

📁 <b>File Processing:</b>
└ Total Files: {stats['total_files']}

⏰ <b>Activity:</b>
├ Peak Hour: {stats['peak_hour']}
└ Current Load: Normal

🎯 <b>Feature Usage:</b>
├ AI Requests: {_get_total_ai_requests()}
├ File Operations: {stats['total_files']}
└ Payment Demos: {_get_total_payments()}

<i>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
    """
    
    await query.edit_message_text(
        detailed_stats,
        parse_mode='HTML',
        reply_markup=get_admin_keyboard()
    )

@handle_errors
async def admin_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user management interface"""
    query = update.callback_query
    
    if query.from_user.id not in ADMIN_USER_IDS:
        await query.answer("Access denied!", show_alert=True)
        return
    
    await query.answer()
    
    # Get recent users
    recent_users = _get_recent_users(limit=10)
    
    user_list = "👥 <b>Recent Users</b>\n\n"
    
    for i, user in enumerate(recent_users, 1):
        user_list += (
            f"{i}. <b>{user['first_name']}</b>\n"
            f"   ID: <code>{user['user_id']}</code>\n"
            f"   Username: @{user['username'] or 'None'}\n"
            f"   Joined: {user['join_date'][:10]}\n\n"
        )
    
    user_list += f"<i>Total: {get_bot_statistics()['total_users']} users</i>"
    
    await query.edit_message_text(
        user_list,
        parse_mode='HTML',
        reply_markup=get_admin_keyboard()
    )

@handle_errors
async def admin_broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Setup broadcast message"""
    query = update.callback_query
    
    if query.from_user.id not in ADMIN_USER_IDS:
        await query.answer("Access denied!", show_alert=True)
        return
    
    await query.answer()
    
    await query.edit_message_text(
        "📢 <b>Broadcast Message</b>\n\n"
        "Send me the message you want to broadcast to all users.\n\n"
        "<i>Use /cancel to cancel broadcast</i>",
        parse_mode='HTML',
        reply_markup=get_back_button()
    )
    
    context.user_data['awaiting'] = 'broadcast_message'

@handle_errors
async def process_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and send broadcast message"""
    admin_id = update.effective_user.id
    
    if admin_id not in ADMIN_USER_IDS:
        return
    
    broadcast_text = update.message.text
    
    # Get all users
    user_ids = db.get_all_user_ids()
    
    status_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Broadcasting...</b>\n\n"
        f"Sending to {len(user_ids)} users...",
        parse_mode='HTML'
    )
    
    sent = 0
    failed = 0
    
    for user_id in user_ids:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📢 <b>Broadcast Message</b>\n\n{broadcast_text}",
                parse_mode='HTML'
            )
            sent += 1
        except:
            failed += 1
    
    # Log broadcast
    cursor = db.conn.cursor()
    cursor.execute('''
        INSERT INTO broadcasts (admin_id, message_text, sent_count, failed_count)
        VALUES (?, ?, ?, ?)
    ''', (admin_id, broadcast_text, sent, failed))
    db.conn.commit()
    
    await status_msg.edit_text(
        f"{EMOJI['success']} <b>Broadcast Complete!</b>\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}\n"
        f"📊 Success Rate: {(sent/(sent+failed)*100):.1f}%",
        parse_mode='HTML',
        reply_markup=get_admin_keyboard()
    )
    
    context.user_data.pop('awaiting', None)

def get_bot_statistics():
    """Get comprehensive bot statistics"""
    return {
        'total_users': db.get_total_users(),
        'active_today': db.get_active_users_today(),
        'new_users_24h': db.get_new_users_24h(),
        'total_messages': db.get_total_messages(),
        'messages_24h': db.get_messages_24h(),
        'total_files': _get_total_files(),
        'peak_hour': _get_peak_hour(),
    }

def _get_total_files():
    """Get total file count"""
    cursor = db.conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM file_logs')
    return cursor.fetchone()[0]

def _get_total_ai_requests():
    """Get total AI requests"""
    cursor = db.conn.cursor()
    cursor.execute('SELECT SUM(ai_count) FROM user_stats')
    result = cursor.fetchone()[0]
    return result or 0

def _get_total_payments():
    """Get total payment demos"""
    cursor = db.conn.cursor()
    cursor.execute('SELECT SUM(payment_count) FROM user_stats')
    result = cursor.fetchone()[0]
    return result or 0

def _calculate_growth_rate():
    """Calculate user growth rate"""
    total = db.get_total_users()
    new = db.get_new_users_24h()
    if total == 0:
        return 0
    return round((new / total) * 100, 1)

def _get_peak_hour():
    """Get peak activity hour"""
    # Simplified - returns current hour
    return datetime.now().strftime('%H:00')

def _get_recent_users(limit=10):
    """Get list of recent users"""
    cursor = db.conn.cursor()
    cursor.execute('''
        SELECT user_id, username, first_name, join_date 
        FROM users 
        ORDER BY join_date DESC 
        LIMIT ?
    ''', (limit,))
    
    return [dict(row) for row in cursor.fetchall()]
