import logging
import qrcode
import os
import tempfile
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

from pydub import AudioSegment
import speech_recognition as sr

logger = logging.getLogger(__name__)

async def select_watch_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("⌚ SE 40mm", callback_data='se_40mm'),
         InlineKeyboardButton("⌚ SE 44mm", callback_data='se_44mm')],
        [InlineKeyboardButton("⌚ Series 41mm", callback_data='series_41mm'),
         InlineKeyboardButton("⌚ Series 45mm", callback_data='series_45mm')],
        [InlineKeyboardButton("⌚ Ultra 2", callback_data='ultra_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your watch model", reply_markup=reply_markup)

async def model_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data in WATCH_MODELS:
        model = WATCH_MODELS[query.data]
        context.user_data['watch_model'] = model
        await query.edit_message_text(f"Model selected: {model['name']}")

async def set_padding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /padding <value>")
        return
    try:
        padding = int(args[0])
    except ValueError:
        await update.message.reply_text("Invalid value. Please provide an integer.")
        return
    context.user_data["padding"] = padding
    await update.message.reply_text(f"Padding set to {padding} px")

async def select_font_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔤 Small", callback_data='font_small'),
         InlineKeyboardButton("🔤 Medium", callback_data='font_medium'),
         InlineKeyboardButton("🔤 Large", callback_data='font_large')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select font size", reply_markup=reply_markup)

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
    await query.edit_message_text(f"Font size set to {size_name}")

async def select_theme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🌙 Dark", callback_data='theme_dark'),
         InlineKeyboardButton("☀️ Light", callback_data='theme_light')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select theme", reply_markup=reply_markup)

async def theme_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    theme_mapping = {
        'theme_dark': 'dark',
        'theme_light': 'light'
    }
    theme = theme_mapping.get(query.data, 'dark')
    context.user_data['theme'] = theme
    await query.edit_message_text(f"Theme set to {theme.capitalize()}")

async def select_layout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📜 Continuous", callback_data='layout_continuous'),
         InlineKeyboardButton("📄 Multi-Page", callback_data='layout_multipage')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select layout", reply_markup=reply_markup)

async def layout_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    layout_mapping = {
        'layout_continuous': 'continuous',
        'layout_multipage': 'multipage'
    }
    layout = layout_mapping.get(query.data, 'continuous')
    context.user_data['layout'] = layout
    await query.edit_message_text(f"Layout set to {layout.capitalize()}")

async def select_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Command /template. If an argument is provided (e.g. /template modern),
    the style is set immediately. Otherwise, an inline keyboard is displayed.
    """
    args = context.args
    available_templates = ['minimalistic', 'modern', 'classic']
    if args and args[0].lower() in available_templates:
        context.user_data['template_style'] = args[0].lower()
        await update.message.reply_text(f"Template set to {args[0].capitalize()}")
    else:
        keyboard = [
            [InlineKeyboardButton("🎨 Minimalistic", callback_data='template_minimalistic'),
             InlineKeyboardButton("🎨 Modern", callback_data='template_modern'),
             InlineKeyboardButton("🎨 Classic", callback_data='template_classic')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select output template style", reply_markup=reply_markup)

async def template_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("template_"):
        style = data.split("_", 1)[1]
        context.user_data['template_style'] = style
        await query.edit_message_text(f"Template set to {style.capitalize()}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to Apple Watch Notes Bot!\n"
        "Commands:\n"
        "• /model – Select your watch model\n"
        "• /fontsize, /theme, /layout, /template – Set appearance\n"
        "• /padding <value> – Set padding (in pixels)\n"
        "Send Markdown text, a .txt/.md file, or a voice note to generate an image.\n"
        "For HTML preview, use /preview <Markdown>"
        "• /qr <URL> – Create a QR-code\n"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model first using /model")
        return
    text = update.message.text
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    layout = context.user_data.get('layout', 'continuous')
    padding = get_padding(context)
    template_style = context.user_data.get('template_style', 'minimalistic')
    try:
        if layout == 'multipage':
            images = render_markdown_to_images_paginated(text, model, font_multiplier, theme, padding, template_style)
        else:
            images = render_markdown_to_image(text, model, font_multiplier, theme, padding, template_style)
        for i, img in enumerate(images):
            await update.message.reply_photo(
                photo=InputFile(img, filename=f"watch_markdown_{i+1}.png"),
                caption=f"Page {i+1} ({model['name']})"
            )
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        await update.message.reply_text("Error processing request")

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
        await update.message.reply_text("Select a watch model using /model")
        return
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    layout = context.user_data.get('layout', 'continuous')
    padding = get_padding(context)
    template_style = context.user_data.get('template_style', 'minimalistic')
    try:
        if layout == 'multipage':
            images = render_markdown_to_images_paginated(text, model, font_multiplier, theme, padding, template_style)
        else:
            images = render_markdown_to_image(text, model, font_multiplier, theme, padding, template_style)
        for i, img in enumerate(images):
            await update.message.reply_photo(
                photo=InputFile(img, filename=f"watch_markdown_{i+1}.png"),
                caption=f"Page {i+1} ({model['name']})"
            )
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await update.message.reply_text("Error processing file")

async def handle_preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model")
        return
    text = update.message.text.replace("/preview", "", 1).strip()
    if not text:
        await update.message.reply_text("Provide Markdown text after /preview")
        return
    template_style = context.user_data.get('template_style', 'minimalistic')
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    padding = get_padding(context)
    html = get_html_preview(text, model, font_multiplier, theme, padding, template_style)
    buf = BytesIO(html.encode('utf-8'))
    buf.name = "preview.html"
    await update.message.reply_document(document=InputFile(buf), filename="preview.html", caption="HTML Preview")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model")
        return
    text = update.message.text.replace("/pdf", "", 1).strip()
    if not text:
        await update.message.reply_text("Provide Markdown text after /pdf")
        return
    template_style = context.user_data.get('template_style', 'minimalistic')
    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    padding = get_padding(context)
    try:
        pdf_buffer = render_markdown_to_pdf(text, model, font_multiplier, theme, padding, template_style)
        pdf_buffer.seek(0)
        await update.message.reply_document(
            document=InputFile(pdf_buffer, filename="output.pdf"),
            caption="PDF created"
        )
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        await update.message.reply_text("Error creating PDF")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Error:", exc_info=context.error)
    if update.message:
        await update.message.reply_text("An error occurred")

async def handle_qrcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.replace("/qrcode", "", 1).strip()
    if not text:
        await update.message.reply_text("Usage: /qrcode <text to encode>")
        return

    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model")
        return

    model = get_user_model(context)
    size = min(model['width'], model['height'])

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    await update.message.reply_photo(
        photo=InputFile(buf, filename="qrcode.png"),
        caption="Here is your QR code!"
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Convert a voice note to text, create a summary, and render it to an image.
    """
    if 'watch_model' not in context.user_data:
        await update.message.reply_text("Select a watch model using /model")
        return

    voice = update.message.voice
    file = await voice.get_file()

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as ogg_file:
        ogg_path = ogg_file.name
        voice_bytes = await file.download_as_bytearray()
        ogg_file.write(voice_bytes)

    wav_path = ogg_path.replace(".ogg", ".wav")
    try:
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")
    except Exception as e:
        logger.error("Error converting audio", exc_info=e)
        await update.message.reply_text("Error processing voice note.")
        os.remove(ogg_path)
        return

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        await update.message.reply_text("Sorry, could not understand the voice message.")
        os.remove(ogg_path)
        os.remove(wav_path)
        return
    except sr.RequestError as e:
        await update.message.reply_text("Error during speech recognition service.")
        os.remove(ogg_path)
        os.remove(wav_path)
        return

    def summarize_text(text: str) -> str:
        sentences = text.split('.')
        summary = '.'.join([s.strip() for s in sentences if s.strip()][:2])
        if summary and not summary.endswith('.'):
            summary += '.'
        return summary if summary else text

    summary = summarize_text(recognized_text)

    os.remove(ogg_path)
    os.remove(wav_path)

    font_multiplier = context.user_data.get('font_multiplier', 1.0)
    theme = context.user_data.get('theme', 'dark')
    model = get_user_model(context)
    padding = get_padding(context)
    template_style = context.user_data.get('template_style', 'minimalistic')

    try:
        images = render_markdown_to_image(summary, model, font_multiplier, theme, padding, template_style)
        for i, img in enumerate(images):
            await update.message.reply_photo(
                photo=InputFile(img, filename=f"watch_markdown_{i+1}.png"),
                caption=f"Voice Summary (Page {i+1} - {model['name']})"
            )
    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        await update.message.reply_text("Error processing voice message.")
