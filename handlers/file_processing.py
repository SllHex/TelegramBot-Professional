from telegram import Update
from telegram.ext import ContextTypes
from config import EMOJI, MAX_FILE_SIZE_MB
from utils.keyboards import get_file_menu_keyboard, get_back_button
from utils.decorators import handle_errors, track_user_activity
from database import db
import time
from PIL import Image
import PyPDF2
import os
import io

@handle_errors
@track_user_activity
async def file_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show file processing menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        f"{EMOJI['file']} <b>File Processing Tools</b>\n\n"
        "Professional file processing capabilities:\n\n"
        "📄 <b>PDF to Text</b> - Extract text from PDFs\n"
        "🖼️ <b>Compress Image</b> - Reduce image file size\n"
        "📊 <b>File Info</b> - Get detailed file information\n"
        "🔄 <b>Convert Format</b> - Change file formats\n\n"
        f"<i>Max file size: {MAX_FILE_SIZE_MB}MB</i>\n\n"
        "✅ All features are fully functional!"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_file_menu_keyboard())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_file_menu_keyboard())

@handle_errors
async def pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle PDF to text conversion"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "📄 <b>PDF to Text Converter</b>\n\n"
        "Send me a PDF file, and I'll extract all the text from it!\n\n"
        "<b>Features:</b>\n"
        "✅ Multi-page support\n"
        "✅ Fast processing\n"
        "✅ Character count stats\n"
        "✅ Processing time tracking\n\n"
        f"<i>Maximum file size: {MAX_FILE_SIZE_MB}MB</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'pdf_file'

@handle_errors
async def image_compress_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image compression"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🖼️ <b>Image Compressor</b>\n\n"
        "Send me an image, and I'll compress it to reduce file size!\n\n"
        "<b>Features:</b>\n"
        "✅ Smart quality optimization\n"
        "✅ Automatic format conversion\n"
        "✅ Size comparison stats\n"
        "✅ Multiple format support\n\n"
        "<i>Supported formats: JPG, PNG, WEBP, BMP</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'image_file'

@handle_errors
async def file_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file info request"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "📊 <b>File Information</b>\n\n"
        "Send me any file, and I'll show you detailed information about it!\n\n"
        "<b>Information provided:</b>\n"
        "├ File name and size\n"
        "├ MIME type\n"
        "├ Telegram file ID\n"
        "└ Upload timestamp\n\n"
        "<i>Works with any file type</i>"
    )
    
    try:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=get_back_button())
    except:
        await query.message.reply_text(text, parse_mode='HTML', reply_markup=get_back_button())
    
    context.user_data['awaiting'] = 'file_info'

@handle_errors
async def process_pdf_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process PDF file and extract text"""
    user_id = update.effective_user.id
    document = update.message.document
    
    if not document or not document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text(
            "❌ Please send a valid PDF file!",
            reply_markup=get_back_button()
        )
        return
    
    # Check file size
    if document.file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        await update.message.reply_text(
            f"❌ File too large! Maximum size is {MAX_FILE_SIZE_MB}MB",
            reply_markup=get_back_button()
        )
        return
    
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Processing PDF...</b>\n\n"
        "🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜ 10%\n"
        "⏳ Downloading file...",
        parse_mode='HTML'
    )
    
    start_time = time.time()
    
    try:
        # Download file
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing PDF...</b>\n\n"
            "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%\n"
            "📥 File downloaded...",
            parse_mode='HTML'
        )
        
        file = await context.bot.get_file(document.file_id)
        file_bytes = await file.download_as_bytearray()
        
        # Extract text from PDF
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing PDF...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ 70%\n"
            "📄 Extracting text...",
            parse_mode='HTML'
        )
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        total_pages = len(pdf_reader.pages)
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            extracted = page.extract_text()
            text += f"\n--- Page {page_num} ---\n{extracted}\n"
        
        # Analyzing
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing PDF...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ 90%\n"
            "📊 Analyzing content...",
            parse_mode='HTML'
        )
        
        processing_time = time.time() - start_time
        char_count = len(text)
        word_count = len(text.split())
        
        # Log to database
        db.log_file_processing(user_id, 'pdf', document.file_size, processing_time)
        db.increment_stat(user_id, 'file_count')
        
        # Prepare result
        preview_text = text[:2000] if len(text) > 2000 else text
        if len(text) > 2000:
            preview_text += "\n\n... (text truncated for preview)"
        
        # Complete
        await loading_msg.edit_text(
            f"✅ <b>Processing PDF...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
            "✨ Complete!",
            parse_mode='HTML'
        )
        
        import asyncio
        await asyncio.sleep(0.5)  # Show 100% briefly
        
        result_message = (
            f"✅ <b>PDF Processing Complete!</b>\n\n"
            f"📄 <b>File:</b> {document.file_name}\n"
            f"📊 <b>Statistics:</b>\n"
            f"├ Pages: {total_pages}\n"
            f"├ Characters: {char_count:,}\n"
            f"├ Words: {word_count:,}\n"
            f"├ Size: {document.file_size / 1024:.1f} KB\n"
            f"└ Processing Time: {processing_time:.2f}s\n\n"
            f"📝 <b>Extracted Text Preview:</b>\n"
            f"<code>{preview_text}</code>"
        )
        
        await loading_msg.edit_text(
            result_message,
            parse_mode='HTML',
            reply_markup=get_file_menu_keyboard()
        )
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ <b>Error Processing PDF</b>\n\n"
            f"An error occurred while processing your PDF:\n"
            f"<code>{str(e)}</code>\n\n"
            f"Please make sure the PDF is not encrypted or corrupted.",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    context.user_data.pop('awaiting', None)

@handle_errors
async def process_image_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and compress image"""
    user_id = update.effective_user.id
    
    # Get photo (largest size)
    photo = update.message.photo[-1] if update.message.photo else None
    if not photo:
        await update.message.reply_text(
            "❌ Please send an image!",
            reply_markup=get_back_button()
        )
        return
    
    loading_msg = await update.message.reply_text(
        f"{EMOJI['loading']} <b>Processing Image...</b>\n\n"
        "🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜ 20%\n"
        "⏳ Downloading image...",
        parse_mode='HTML'
    )
    
    start_time = time.time()
    
    try:
        # Download image
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing Image...</b>\n\n"
            "🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ 40%\n"
            "📥 Image downloaded...",
            parse_mode='HTML'
        )
        
        file = await context.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()
        
        # Open and get image info
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing Image...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%\n"
            "🖼️ Optimizing quality...",
            parse_mode='HTML'
        )
        
        image = Image.open(io.BytesIO(file_bytes))
        original_format = image.format
        original_size = len(file_bytes)
        width, height = image.size
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        
        # Compress with different qualities and choose best
        await loading_msg.edit_text(
            f"{EMOJI['loading']} <b>Processing Image...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜ 80%\n"
            "📦 Compressing file...",
            parse_mode='HTML'
        )
        
        best_output = None
        best_quality = 0
        
        for quality in [85, 75, 65]:
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_size = len(output.getvalue())
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            if reduction >= 30 and reduction <= 70:
                best_output = output
                best_quality = quality
                break
            elif reduction > 0:
                best_output = output
                best_quality = quality
        
        if not best_output:
            best_output = io.BytesIO()
            image.save(best_output, format='JPEG', quality=75, optimize=True)
            best_quality = 75
        
        best_output.seek(0)
        
        original_size_kb = original_size / 1024
        compressed_size = len(best_output.getvalue())
        compressed_size_kb = compressed_size / 1024
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        processing_time = time.time() - start_time
        
        # Log to database
        db.log_file_processing(user_id, 'image', original_size, processing_time)
        db.increment_stat(user_id, 'file_count')
        
        # Complete
        await loading_msg.edit_text(
            f"✅ <b>Processing Image...</b>\n\n"
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%\n"
            "✨ Complete!",
            parse_mode='HTML'
        )
        
        import asyncio
        await asyncio.sleep(0.5)  # Show 100% briefly
        
        # Send compressed image
        await loading_msg.delete()
        await update.message.reply_document(
            document=best_output,
            filename=f'compressed_{int(time.time())}.jpg',
            caption=(
                f"✅ <b>Image Compression Complete!</b>\n\n"
                f"📊 <b>Results:</b>\n"
                f"├ Original Size: {original_size_kb:.1f} KB\n"
                f"├ Compressed Size: {compressed_size_kb:.1f} KB\n"
                f"├ Reduction: {reduction:.1f}%\n"
                f"├ Quality: {best_quality}%\n"
                f"├ Resolution: {width}×{height}\n"
                f"├ Original Format: {original_format}\n"
                f"└ Processing Time: {processing_time:.2f}s\n\n"
                f"💾 <b>Savings:</b> {original_size_kb - compressed_size_kb:.1f} KB"
            ),
            parse_mode='HTML',
            reply_markup=get_file_menu_keyboard()
        )
        
    except Exception as e:
        await loading_msg.edit_text(
            f"❌ <b>Error Compressing Image</b>\n\n"
            f"An error occurred:\n<code>{str(e)}</code>",
            parse_mode='HTML',
            reply_markup=get_back_button()
        )
    
    context.user_data.pop('awaiting', None)

@handle_errors
async def process_file_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed file information"""
    user_id = update.effective_user.id
    document = update.message.document
    
    if not document:
        await update.message.reply_text(
            "❌ Please send a file!",
            reply_markup=get_back_button()
        )
        return
    
    # Get file extension
    file_name = document.file_name
    file_ext = os.path.splitext(file_name)[1].upper() if '.' in file_name else 'Unknown'
    
    # Format file size
    size_bytes = document.file_size
    if size_bytes < 1024:
        size_str = f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        size_str = f"{size_bytes / 1024:.2f} KB"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
    
    file_info = (
        f"📊 <b>File Information</b>\n\n"
        f"📁 <b>File Details:</b>\n"
        f"├ Name: {document.file_name}\n"
        f"├ Extension: {file_ext}\n"
        f"├ Size: {size_str}\n"
        f"├ MIME Type: {document.mime_type}\n"
        f"└ File ID: <code>{document.file_id[:20]}...</code>\n\n"
        f"✅ File is stored securely on Telegram servers\n"
        f"📥 Ready for processing"
    )
    
    db.increment_stat(user_id, 'file_count')
    
    await update.message.reply_text(
        file_info,
        parse_mode='HTML',
        reply_markup=get_file_menu_keyboard()
    )
    
    context.user_data.pop('awaiting', None)
