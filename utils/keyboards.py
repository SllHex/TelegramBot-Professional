from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import EMOJI

def get_main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['robot']} AI Features", callback_data='menu_ai'),
            InlineKeyboardButton(f"{EMOJI['file']} File Tools", callback_data='menu_files'),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['payment']} Payment Demo", callback_data='menu_payment'),
            InlineKeyboardButton(f"{EMOJI['stats']} My Stats", callback_data='menu_stats'),
        ],
        [
            InlineKeyboardButton(f"{EMOJI['settings']} Settings", callback_data='menu_settings'),
            InlineKeyboardButton(f"{EMOJI['help']} Help", callback_data='menu_help'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_menu_keyboard():
    """AI features menu"""
    keyboard = [
        [
            InlineKeyboardButton("✨ Generate Text", callback_data='ai_text'),
            InlineKeyboardButton("🎨 Create Image", callback_data='ai_image'),
        ],
        [
            InlineKeyboardButton("📝 Summarize Text", callback_data='ai_summarize'),
            InlineKeyboardButton("💡 Smart Reply", callback_data='ai_reply'),
        ],
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_file_menu_keyboard():
    """File processing menu"""
    keyboard = [
        [
            InlineKeyboardButton("📄 PDF to Text", callback_data='file_pdf'),
            InlineKeyboardButton("🖼️ Compress Image", callback_data='file_image'),
        ],
        [
            InlineKeyboardButton("📊 File Info", callback_data='file_info'),
            InlineKeyboardButton("🔄 Convert Format", callback_data='file_convert'),
        ],
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_menu_keyboard():
    """Payment demo menu"""
    keyboard = [
        [
            InlineKeyboardButton("💎 Premium Plan - $9.99", callback_data='pay_premium'),
        ],
        [
            InlineKeyboardButton("🌟 Pro Plan - $19.99", callback_data='pay_pro'),
        ],
        [
            InlineKeyboardButton("🚀 Enterprise - $49.99", callback_data='pay_enterprise'),
        ],
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Admin panel keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Statistics", callback_data='admin_stats'),
            InlineKeyboardButton("👥 User List", callback_data='admin_users'),
        ],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast'),
            InlineKeyboardButton("⚙️ Settings", callback_data='admin_settings'),
        ],
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button():
    """Simple back button"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')]
    ])

def get_confirm_keyboard(action: str):
    """Confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['success']} Confirm", callback_data=f'confirm_{action}'),
            InlineKeyboardButton(f"{EMOJI['error']} Cancel", callback_data='back_main'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    """Settings menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔔 Notifications", callback_data='settings_notif'),
            InlineKeyboardButton("🌐 Language", callback_data='settings_lang'),
        ],
        [
            InlineKeyboardButton("🎨 Theme", callback_data='settings_theme'),
            InlineKeyboardButton("🔐 Privacy", callback_data='settings_privacy'),
        ],
        [InlineKeyboardButton(f"{EMOJI['back']} Back to Menu", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)
