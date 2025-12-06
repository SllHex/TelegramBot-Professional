from telegram import Update
from telegram.ext import ContextTypes
from config import GEMINI_API_KEY, ENABLE_AI_FEATURES, EMOJI
from utils.keyboards import get_ai_menu_keyboard, get_back_button
from utils.decorators import handle_errors, track_user_activity
from database import db
import google.generativeai as genai

# Configure Gemini if available
if ENABLE_AI_FEATURES:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')  # Using Gemini 2.5 Pro

@handle_errors
@track_user_activity
async def ai_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show AI features menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🤖 <b>AI Features - Demo Mode</b>\n\n"
        "ℹ️ <b>Note:</b> AI features are running in <b>DEMO MODE</b>\n\n"
        "This bot is fully functional and demonstrates:\n"
        "✅ AI text generation capability\n"
        "✅ Image creation workflow\n"
        "✅ Text summarization flow\n"
        "✅ Smart reply system\n\n"
        "💡 <b>For Production Use:</b>\n"
        "To enable real AI responses, add a Google Gemini API key (FREE) to the configuration.\n\n"
        "🔗 Get free API: https://makersuite.google.com/app/apikey\n\n"
        "<i>The bot is working perfectly - try the features to see the demo!</i>"
    ) if not ENABLE_AI_FEATURES else (
        "🤖 <b>AI Features</b>\n\n"
        "Choose an AI tool below:\n\n"
        "✨ <b>Generate Text</b> - Create content with AI\n"
        "🎨 <b>Create Image</b> - Generate images from descriptions\n"
        "📝 <b>Summarize Text</b> - Condense long texts\n"
        "💡 <b>Smart Reply</b> - Get intelligent responses\n\n"
        "Try any feature to see AI in action!"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_ai_menu_keyboard())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_ai_menu_keyboard())

@handle_errors
async def ai_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text generation request"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "✨ <b>Text Generation</b>\n\n"
        "Please send me a prompt, and I'll generate text for you!\n\n"
        "<i>Example: Write a short story about a robot</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    # Set user state for next message
    context.user_data['awaiting'] = 'ai_text_prompt'

@handle_errors
async def ai_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image generation request"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🎨 <b>Image Generation</b>\n\n"
        "Send me a description, and I'll create an image!\n\n"
        "<i>Example: A futuristic cityscape at sunset</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'ai_image_prompt'

@handle_errors
async def ai_summarize_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text summarization request"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "📝 <b>Text Summarization</b>\n\n"
        "Send me a long text, and I'll summarize it for you!\n\n"
        "<i>Demo: This feature uses AI to condense long content</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'ai_summarize_text'

@handle_errors
async def ai_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle smart reply request"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "💡 <b>Smart Reply</b>\n\n"
        "Ask me anything, and I'll give you an intelligent response!\n\n"
        "<i>Example: What are the benefits of AI automation?</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'ai_smart_reply'

@handle_errors
async def process_ai_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process text generation with Google Gemini"""
    user_id = update.effective_user.id
    prompt = update.message.text
    
    # Send loading message
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Generating text with AI...</b>\n\n"
        "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%\n"
        "🤖 Initializing AI...",
        parse_mode='HTML'
    )
    
    try:
        import asyncio
        
        if ENABLE_AI_FEATURES:
            await loading_msg.edit_text(
                f"{EMOJI['loading']} <b>Generating text with AI...</b>\n\n"
                "🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%\n"
                "💭 Processing prompt...",
                parse_mode='HTML'
            )
            
            # Use Gemini 1.5 Flash to generate response
            response = model.generate_content(prompt)
            result = response.text
        else:
            # Demo mode - show progress
            await loading_msg.edit_text(
                f"{EMOJI['loading']} <b>Generating text with AI...</b>\n\n"
                "🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ 70%\n"
                "✨ Crafting response...",
                parse_mode='HTML'
            )
            await asyncio.sleep(0.5)
            
            await loading_msg.edit_text(
                f"{EMOJI['loading']} <b>Generating text with AI...</b>\n\n"
                "🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ 90%\n"
                "📝 Finalizing...",
                parse_mode='HTML'
            )
            await asyncio.sleep(0.3)
            
            # Demo mode - show what it would do
            result = (
                f"📝 <b>Demo Response</b>\n\n"
                f"This is a demonstration of AI text generation capability.\n\n"
                f"<b>Your prompt was:</b> \"{prompt[:100]}\"\n\n"
                f"<b>In production mode:</b> This would generate a complete, "
                f"AI-powered response using Google Gemini 1.5 Flash based on your prompt. "
                f"The response would be contextual, creative, and tailored to your needs.\n\n"
                f"✅ The feature is fully implemented and ready!\n"
                f"💡 Add Google Gemini API key (FREE) to enable real AI responses.\n\n"
                f"🔗 Get free API: https://makersuite.google.com/app/apikey"
            )
        
        # Show 100%
        await loading_msg.edit_text(
            f"✅ <b>Generating text with AI...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
            "✨ Complete!",
            parse_mode='HTML'
        )
        await asyncio.sleep(0.3)
        
        db.increment_stat(user_id, 'ai_count')
        
        await loading_msg.edit_text(
            result,
            parse_mode='HTML',
            reply_markup=get_ai_menu_keyboard()
        )
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ Error generating text: {str(e)}\n\n"
            "This is a demo feature showing AI capabilities.",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    # Clear state
    context.user_data.pop('awaiting', None)

@handle_errors
async def process_ai_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process image generation request"""
    user_id = update.effective_user.id
    prompt = update.message.text
    
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Creating image with AI...</b>\n\n"
        "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%\n"
        "🎨 Initializing...",
        parse_mode='HTML'
    )
    
    try:
        import asyncio
        import requests
        from io import BytesIO
        
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Creating image with AI...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ 70%\n"
            "✨ Generating image...",
            parse_mode='HTML'
        )
        
        # Use free Pollinations.ai API (no API key needed!)
        # Encode the prompt for URL
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        # Download the generated image
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image_data.seek(0)
            
            await loading_msg.edit_text(
                f"✅ <b>Image Creation</b>\n\n"
                "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
                "✨ Complete!",
                parse_mode='HTML'
            )
            await asyncio.sleep(0.3)
            
            # Send the generated image
            await loading_msg.delete()
            await update.message.reply_photo(
                photo=image_data,
                caption=(
                    f"🎨 <b>AI Generated Image</b>\n\n"
                    f"<b>Prompt:</b> {prompt}\n\n"
                    f"✨ <i>Powered by AI</i>"
                ),
                parse_mode='HTML',
                reply_markup=get_ai_menu_keyboard()
            )
            
            db.increment_stat(user_id, 'ai_count')
        else:
            raise Exception("Failed to generate image")
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ Error creating image: {str(e)}\n\n"
            "Please try again with a different prompt.",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    context.user_data.pop('awaiting', None)

@handle_errors
async def process_ai_summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process text summarization with Gemini"""
    user_id = update.effective_user.id
    text_to_summarize = update.message.text
    
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Summarizing text...</b>\n\n"
        "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%\n"
        "📝 Analyzing...",
        parse_mode='HTML'
    )
    
    try:
        import asyncio
        
        if ENABLE_AI_FEATURES:
            await loading_msg.edit_text(
                f"{EMOJI['loading']} <b>Summarizing text...</b>\n\n"
                "🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%\n"
                "🤖 Processing...",
                parse_mode='HTML'
            )
            
            prompt = f"Please summarize the following text concisely:\n\n{text_to_summarize}"
            response = model.generate_content(prompt)
            result = f"📝 <b>Summary:</b>\n\n{response.text}"
        else:
            await asyncio.sleep(0.5)
            result = (
                f"📝 <b>Text Summarization Demo</b>\n\n"
                f"<b>Original text length:</b> {len(text_to_summarize)} characters\n\n"
                f"<b>In production mode:</b> This would provide an AI-powered "
                f"summary of your text using Gemini 2.5 Pro.\n\n"
                f"✅ Feature is fully implemented!\n"
                f"💡 Add Gemini API key to enable real summarization."
            )
        
        await loading_msg.edit_text(
            f"✅ <b>Summarizing text...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
            "✨ Complete!",
            parse_mode='HTML'
        )
        await asyncio.sleep(0.3)
        
        db.increment_stat(user_id, 'ai_count')
        
        await loading_msg.edit_text(
            result,
            parse_mode='HTML',
            reply_markup=get_ai_menu_keyboard()
        )
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ Error: {str(e)}\n\nThis is a demo feature.",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    context.user_data.pop('awaiting', None)

@handle_errors
async def process_ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process smart reply with Gemini"""
    user_id = update.effective_user.id
    question = update.message.text
    
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Generating smart reply...</b>\n\n"
        "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%\n"
        "💡 Thinking...",
        parse_mode='HTML'
    )
    
    try:
        import asyncio
        
        if ENABLE_AI_FEATURES:
            await loading_msg.edit_text(
                f"{EMOJI['loading']} <b>Generating smart reply...</b>\n\n"
                "🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%\n"
                "🤖 Processing...",
                parse_mode='HTML'
            )
            
            response = model.generate_content(question)
            result = f"💡 <b>Smart Reply:</b>\n\n{response.text}"
        else:
            await asyncio.sleep(0.5)
            result = (
                f"💡 <b>Smart Reply Demo</b>\n\n"
                f"<b>Your question:</b> \"{question[:100]}\"\n\n"
                f"<b>In production mode:</b> This would provide an intelligent, "
                f"contextual response using Gemini 2.5 Pro AI.\n\n"
                f"✅ Feature is fully implemented!\n"
                f"💡 Add Gemini API key to enable real AI responses."
            )
        
        await loading_msg.edit_text(
            f"✅ <b>Generating smart reply...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
            "✨ Complete!",
            parse_mode='HTML'
        )
        await asyncio.sleep(0.3)
        
        db.increment_stat(user_id, 'ai_count')
        
        await loading_msg.edit_text(
            result,
            parse_mode='HTML',
            reply_markup=get_ai_menu_keyboard()
        )
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ Error: {str(e)}\n\nThis is a demo feature.",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    context.user_data.pop('awaiting', None)
