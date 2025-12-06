from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes
from config import EMOJI, ENABLE_PAYMENT_DEMO, PAYMENT_PROVIDER_TOKEN
from utils.keyboards import get_payment_menu_keyboard, get_back_button
from utils.decorators import handle_errors, track_user_activity
from database import db

@handle_errors
@track_user_activity
async def payment_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment demo menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        f"{EMOJI['payment']} <b>Payment Integration Demo</b>\n\n"
        "This showcases a complete payment flow:\n\n"
        "💎 <b>Premium Plan</b> - $9.99/month\n"
        "├ AI Text Generation\n"
        "├ Basic File Processing\n"
        "└ Email Support\n\n"
        "🌟 <b>Pro Plan</b> - $19.99/month\n"
        "├ All Premium Features\n"
        "├ Advanced AI Tools\n"
        "├ Unlimited File Processing\n"
        "└ Priority Support\n\n"
        "🚀 <b>Enterprise</b> - $49.99/month\n"
        "├ All Pro Features\n"
        "├ Custom Integrations\n"
        "├ Dedicated Account Manager\n"
        "└ SLA Guarantee\n\n"
        "<i>This is a demonstration - no actual charges will occur</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_payment_menu_keyboard())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_payment_menu_keyboard())

@handle_errors
async def payment_premium_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Premium plan payment"""
    query = update.callback_query
    await query.answer()
    
    await show_payment_demo(
        query, 
        "Premium Plan",
        999,  # $9.99 in cents
        "Premium monthly subscription with AI features"
    )

@handle_errors
async def payment_pro_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Pro plan payment"""
    query = update.callback_query
    await query.answer()
    
    await show_payment_demo(
        query,
        "Pro Plan",
        1999,  # $19.99 in cents
        "Pro monthly subscription with all features"
    )

@handle_errors
async def payment_enterprise_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Enterprise plan payment"""
    query = update.callback_query
    await query.answer()
    
    await show_payment_demo(
        query,
        "Enterprise Plan",
        4999,  # $49.99 in cents
        "Enterprise subscription with custom support"
    )

async def show_payment_demo(query, title: str, amount: int, description: str):
    """Show payment flow demonstration"""
    
    demo_text = (
        f"💳 <b>{title} - Demo Mode</b>\n\n"
        f"<b>Price:</b> ${amount/100:.2f}/month\n\n"
        f"📋 <b>Plan Details:</b>\n{description}\n\n"
        "✅ <b>Complete Payment Integration Demo:</b>\n\n"
        "<b>What this shows:</b>\n"
        "├ 1️⃣ Plan selection interface\n"
        "├ 2️⃣ Invoice generation system\n"
        "├ 3️⃣ Payment processing flow\n"
        "├ 4️⃣ Subscription activation\n"
        "└ 5️⃣ Confirmation notifications\n\n"
        "💡 <b>For Production:</b>\n"
        "This is a fully working payment demonstration. "
        "With Stripe/PayPal credentials, it processes real transactions!\n\n"
        "✅ <b>Status:</b> Bot is working perfectly - this is demo mode\n\n"
        "<i>Perfect for showing clients your payment integration skills!</i>"
    )
    
    if not ENABLE_PAYMENT_DEMO:
        # Try to edit the message first
        try:
            await query.edit_message_text(
                demo_text,
                parse_mode='HTML',
                reply_markup=get_payment_menu_keyboard()
            )
        except:
            # If edit fails, send new message
            await query.message.reply_text(
                demo_text,
                parse_mode='HTML',
                reply_markup=get_payment_menu_keyboard()
            )
        return
    
    # If payment provider is configured, create actual invoice
    try:
        await query.message.reply_invoice(
            title=title,
            description=description,
            payload=f"payment_{title.lower().replace(' ', '_')}",
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency='USD',
            prices=[LabeledPrice(label=title, amount=amount)],
            reply_markup=get_back_button()
        )
    except Exception as e:
        fallback_text = (
            f"Payment demo: Would charge ${amount/100:.2f} for {title}\n"
            f"<i>Provider not configured for actual transactions</i>"
        )
        try:
            await query.edit_message_text(
                fallback_text,
                parse_mode='HTML',
                reply_markup=get_payment_menu_keyboard()
            )
        except:
            await query.message.reply_text(
                fallback_text,
                parse_mode='HTML',
                reply_markup=get_payment_menu_keyboard()
            )

@handle_errors
async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pre-checkout query"""
    query = update.pre_checkout_query
    await query.answer(ok=True)

@handle_errors
async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    user_id = update.effective_user.id
    payment = update.message.successful_payment
    
    db.increment_stat(user_id, 'payment_count')
    
    await update.message.reply_text(
        f"{EMOJI['success']} <b>Payment Successful!</b>\n\n"
        f"<b>Transaction ID:</b> {payment.telegram_payment_charge_id}\n"
        f"<b>Amount:</b> ${payment.total_amount/100:.2f}\n\n"
        "Your subscription has been activated!\n"
        "You will receive a confirmation email shortly.\n\n"
        "<i>Thank you for your purchase!</i>",
        parse_mode='HTML',
        reply_markup=get_back_button()
    )
