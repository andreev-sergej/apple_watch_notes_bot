import logging
from io import BytesIO

from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import WATCH_MODELS
from renderer import (
    get_html_preview,
    render_markdown_to_image,
    render_markdown_to_images_paginated,
    render_markdown_to_pdf
)
from utils import get_user_model, get_padding

logger = logging.getLogger(__name__)

async def select_watch_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("SE 40mm", callback_data='se_40mm'),
         InlineKeyboardButton("SE 44mm", callback_data='se_44mm')],
        [InlineKeyboardButton("Series 41mm", callback_data='series_41mm'),
         InlineKeyboardButton("Series 45mm", callback_data='series_45mm')],
        [InlineKeyboardButton("Ultra 2", callback_data='ultra_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your watch model ℹ️", reply_markup=reply_markup)

async def model_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data in WATCH_MODELS:
        model = WATCH_MODELS[query.data]
        context.user_data['watch_model'] = model
        await query.edit_message_text(f"Model selected: {model['name']} ℹ️")

async def set_padding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /padding <value> ")
        return
    try:
        padding = int(args[0])
    except ValueError:
        await update.message.reply_text("Invalid value. Please provide an integer. ")
        return
    context.user_data["padding"] = padding
    await update.message.reply_text(f"Padding set to {padding} px ")

async def select_font_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Small", callback_data='font_small'),
         InlineKeyboardButton("Medium", callback_data='font_medium'),
         InlineKeyboardButton("Large", callback_data='font_large')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select font size ", reply_markup=reply_markup)

async def font_size_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    size_mapping = {
        'font_small': 0.8,
        'font_medium': 1.0,
        'font_large': 1.2
    }
    multiplier = size_mapping.get(query.data, 1.0)
    context.user_data['font_multiplier'] = multiplier
    size_name = query.data.split('_')[1].capitalize()
    await query.edit_message_text(f"Font size set to {size_name} ")

async def select_theme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Dark", callback_data='theme_dark'),
         InlineKeyboardButton("Light", callback_data='theme_light')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select theme ", reply_markup=reply_markup)

async def theme_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    theme_mapping = {
        'theme_dark': 'dark',
        'theme_light': 'light'
    }
    theme = theme_mapping.get(query.data, 'dark')
    context.user_data['theme'] = theme
    await query.edit_message_text(f"Theme set to {theme.capitalize()} ")

async def select_layout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Continuous", callback_data='layout_continuous'),
         InlineKeyboardButton("Multi-Page", callback_data='layout_multipage')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select layout ", reply_markup=reply_markup)

async def layout_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    layout_mapping = {
        'layout_continuous': 'continuous',
        'layout_multipage': 'multipage'
    }
    layout = layout_mapping.get(query.data, 'continuous')
    context.user_data['layout'] = layout
    await query.edit_message_text(f"Layout set to {layout.capitalize()} ")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome, this is @apple_watch_notes_bot\n"
        "Use /model to select your watch model.\n"
        "Use /fontsize, /theme, /layout to set appearance.\n"
        "Set padding with /padding <value> (in pixels).\n"
        "Send Markdown text or a .txt/.md file to generate an image.\n"
        "For HTML preview, use /preview <Markdown> "
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model first using /model ")
        return
    text = update.message.text
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    layout = context.user_data.get('layout', 'continuous')
    padding = get_padding(context)
    try:
        if layout == 'multipage':
            images = render_markdown_to_images_paginated(text, model, font_multiplier, theme, padding)
        else:
            images = render_markdown_to_image(text, model, font_multiplier, theme, padding)
        for i, img in enumerate(images):
            await update.message.reply_photo(
                photo=InputFile(img, filename=f"watch_markdown_{i+1}.png"),
                caption=f"Page {i+1} ({model['name']}) ℹ️"
            )
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        await update.message.reply_text("Error processing request")
    
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Выберите модель часов с помощью /model")
        return
    text = update.message.text.replace("/pdf", "", 1).strip()
    if not text:
        await update.message.reply_text("Укажите Markdown-текст после /pdf")
        return
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    padding = get_padding(context)
    try:
        pdf_buffer = render_markdown_to_pdf(text, model, font_multiplier, theme, padding)
        pdf_buffer.seek(0)
        await update.message.reply_document(
            document=InputFile(pdf_buffer, filename="output.pdf"),
            caption="PDF создан ℹ️"
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке PDF: {e}")
        await update.message.reply_text("Ошибка при создании PDF")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    file_name = document.file_name.lower()
    if not (file_name.endswith('.txt') or file_name.endswith('.md')):
        await update.message.reply_text("Upload a .txt or .md file")
        return
    try:
        file = await document.get_file()
        file_bytes = await file.download_as_bytearray()
        text = file_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        await update.message.reply_text("Error downloading file")
        return
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model ")
        return
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    layout = context.user_data.get('layout', 'continuous')
    padding = get_padding(context)
    try:
        if layout == 'multipage':
            images = render_markdown_to_images_paginated(text, model, font_multiplier, theme, padding)
        else:
            images = render_markdown_to_image(text, model, font_multiplier, theme, padding)
        for i, img in enumerate(images):
            await update.message.reply_photo(
                photo=InputFile(img, filename=f"watch_markdown_{i+1}.png"),
                caption=f"Page {i+1} ({model['name']}) ℹ️"
            )
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await update.message.reply_text("Error processing file")

async def handle_preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model ")
        return
    text = update.message.text.replace("/preview", "", 1).strip()
    if not text:
        await update.message.reply_text("Provide Markdown text after /preview ")
        return
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    padding = get_padding(context)
    html = get_html_preview(text, model, font_multiplier, theme, padding)
    buf = BytesIO(html.encode('utf-8'))
    buf.name = "preview.html"
    await update.message.reply_document(document=InputFile(buf), filename="preview.html", caption="HTML Preview ")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Error:", exc_info=context.error)
    if update.message:
        await update.message.reply_text("An error occurred")
