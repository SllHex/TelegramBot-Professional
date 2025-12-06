import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
    ContextTypes
)
from config import BOT_TOKEN, EMOJI, DATABASE_PATH
from database import db

# Import handlers
from handlers.start import start_command, help_command, profile_command, stats_command
from handlers.ai_features import (
    ai_menu_handler, ai_text_handler, ai_image_handler,
    ai_summarize_handler, ai_reply_handler, process_ai_text
)
from handlers.file_processing import (
    file_menu_handler, pdf_handler, image_compress_handler,
    file_info_handler, process_pdf_file, process_image_file, process_file_info
)
from handlers.payment_demo import (
    payment_menu_handler, payment_premium_handler, payment_pro_handler,
    payment_enterprise_handler, precheckout_handler, successful_payment_handler
)
from handlers.admin_panel import (
    admin_command, admin_stats_handler, admin_users_handler,
    admin_broadcast_handler, process_broadcast
)

from utils.keyboards import get_main_menu_keyboard, get_settings_keyboard
from utils.decorators import handle_errors

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================================
# CALLBACK QUERY ROUTER
# ============================================================================

@handle_errors
async def callback_query_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callback queries to appropriate handlers"""
    query = update.callback_query
    data = query.data
    
    # Helper function to safely edit or send new message
    async def safe_send_or_edit(text, markup):
        """Try to edit message, if fails send new one"""
        try:
            await query.edit_message_text(
                text,
                parse_mode='HTML',
                reply_markup=markup
            )
        except:
            # If edit fails (e.g. message is photo/document), send new message
            await query.message.reply_text(
                text,
                parse_mode='HTML',
                reply_markup=markup
            )
    
    # Menu navigation
    if data == 'back_main':
        await query.answer()
        from config import MESSAGES
        await safe_send_or_edit(
            MESSAGES['welcome'],
            get_main_menu_keyboard()
        )
    
    elif data == 'menu_ai':
        await ai_menu_handler(update, context)
    
    elif data == 'menu_files':
        await file_menu_handler(update, context)
    
    elif data == 'menu_payment':
        await payment_menu_handler(update, context)
    
    elif data == 'menu_stats':
        await query.answer()
        await stats_command(update, context)
    
    elif data == 'menu_help':
        await query.answer()
        from config import MESSAGES
        await safe_send_or_edit(
            MESSAGES['help'],
            get_main_menu_keyboard()
        )
    
    elif data == 'menu_settings':
        await query.answer()
        await safe_send_or_edit(
            f"{EMOJI['settings']} <b>Settings</b>\n\n"
            "Customize your bot experience:\n\n"
            "🔔 <b>Notifications</b> - Manage alerts\n"
            "🌐 <b>Language</b> - Choose your language\n"
            "🎨 <b>Theme</b> - Personalize appearance\n"
            "🔐 <b>Privacy</b> - Security settings",
            get_settings_keyboard()
        )
    
    # AI Features
    elif data == 'ai_text':
        await ai_text_handler(update, context)
    elif data == 'ai_image':
        await ai_image_handler(update, context)
    elif data == 'ai_summarize':
        await ai_summarize_handler(update, context)
    elif data == 'ai_reply':
        await ai_reply_handler(update, context)
    
    # File Processing
    elif data == 'file_pdf':
        await pdf_handler(update, context)
    elif data == 'file_image':
        await image_compress_handler(update, context)
    elif data == 'file_info':
        await file_info_handler(update, context)
    elif data == 'file_convert':
        await query.answer()
        await safe_send_or_edit(
            "🔄 <b>Format Converter</b>\n\n"
            "This feature would convert between different file formats!\n\n"
            "<i>Demo: Shows file conversion capabilities</i>",
            get_main_menu_keyboard()
        )
    
    # Payment
    elif data == 'pay_premium':
        await payment_premium_handler(update, context)
    elif data == 'pay_pro':
        await payment_pro_handler(update, context)
    elif data == 'pay_enterprise':
        await payment_enterprise_handler(update, context)
    
    # Admin
    elif data == 'admin_stats':
        await admin_stats_handler(update, context)
    elif data == 'admin_users':
        await admin_users_handler(update, context)
    elif data == 'admin_broadcast':
        await admin_broadcast_handler(update, context)
    elif data == 'admin_settings':
        await query.answer()
        await safe_send_or_edit(
            "⚙️ <b>Admin Settings</b>\n\n"
            "Configure bot settings, rate limits, and features here.\n\n"
            "<i>This is a demo admin interface</i>",
            get_main_menu_keyboard()
        )
    
    # Settings
    elif data.startswith('settings_'):
        await query.answer()
        setting_name = data.replace('settings_', '').title()
        await safe_send_or_edit(
            f"{EMOJI['settings']} <b>{setting_name} Settings</b>\n\n"
            f"Configure your {setting_name.lower()} preferences here.\n\n"
            "<i>This demonstrates customizable user settings</i>",
            get_settings_keyboard()
        )

# ============================================================================
# MESSAGE HANDLERS
# ============================================================================

@handle_errors
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages based on current state"""
    
    # Check if waiting for specific input
    awaiting = context.user_data.get('awaiting')
    
    if awaiting == 'ai_text_prompt':
        await process_ai_text(update, context)
    elif awaiting == 'ai_image_prompt':
        from handlers.ai_features import process_ai_image
        await process_ai_image(update, context)
    elif awaiting == 'ai_summarize_text':
        from handlers.ai_features import process_ai_summarize
        await process_ai_summarize(update, context)
    elif awaiting == 'ai_smart_reply':
        from handlers.ai_features import process_ai_reply
        await process_ai_reply(update, context)
    elif awaiting == 'broadcast_message':
        await process_broadcast(update, context)
    else:
        # Default response
        await update.message.reply_text(
            "👋 I'm a professional bot showcase!\n\n"
            "Use /start to see all features or /help for assistance.",
            reply_markup=get_main_menu_keyboard()
        )

@handle_errors
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads"""
    awaiting = context.user_data.get('awaiting')
    
    if awaiting == 'pdf_file':
        await process_pdf_file(update, context)
    elif awaiting == 'file_info':
        await process_file_info(update, context)
    else:
        await update.message.reply_text(
            "📄 I received your file!\n\n"
            "Please choose a file operation from the File Tools menu.",
            reply_markup=get_main_menu_keyboard()
        )

@handle_errors
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads"""
    awaiting = context.user_data.get('awaiting')
    
    if awaiting == 'image_file':
        await process_image_file(update, context)
    else:
        await update.message.reply_text(
            "🖼️ Nice image!\n\n"
            "Use File Tools → Compress Image to optimize it.",
            reply_markup=get_main_menu_keyboard()
        )

# ============================================================================
# ERROR HANDLER
# ============================================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates"""
    logger.error(f'Update {update} caused error {context.error}')

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Start the bot"""
    
    # Verify bot token
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found!")
        print("Please set your bot token in the .env file")
        return
    
    print("🤖 Starting Professional Showcase Bot...")
    print(f"📊 Database: {DATABASE_PATH}")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    # Callback query handler (for inline buttons)
    application.add_handler(CallbackQueryHandler(callback_query_router))
    
    # Message handlers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_message
    ))
    application.add_handler(MessageHandler(
        filters.Document.ALL,
        handle_document
    ))
    application.add_handler(MessageHandler(
        filters.PHOTO,
        handle_photo
    ))
    
    # Payment handlers
    application.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    application.add_handler(MessageHandler(
        filters.SUCCESSFUL_PAYMENT,
        successful_payment_handler
    ))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    print("✅ Bot started successfully!")
    print("📱 Send /start to begin")
    print("🛑 Press Ctrl+C to stop\n")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        db.close()
        print("👋 Goodbye!")
