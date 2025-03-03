import logging
import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from handlers import (
    start,
    select_watch_model,
    model_selection,
    set_padding,
    select_font_size,
    font_size_selection,
    select_theme,
    theme_selection,
    select_layout,
    layout_selection,
    select_template,
    template_selection,
    select_fonts,
    font_category_selection,
    font_choice_selection,
    handle_text,
    handle_document,
    handle_preview,
    handle_pdf,
    error_handler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set in environment variables")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("model", select_watch_model))
    app.add_handler(CommandHandler("padding", set_padding))
    app.add_handler(CommandHandler("fontsize", select_font_size))
    app.add_handler(CommandHandler("theme", select_theme))
    app.add_handler(CommandHandler("layout", select_layout))
    app.add_handler(CommandHandler("template", select_template))
    app.add_handler(CommandHandler("fonts", select_fonts))
    app.add_handler(CommandHandler("preview", handle_preview))
    app.add_handler(CommandHandler("pdf", handle_pdf))

    app.add_handler(CallbackQueryHandler(model_selection, pattern='^(se_|series_|ultra_)'))
    app.add_handler(CallbackQueryHandler(font_size_selection, pattern='^font_(small|medium|large)$'))
    app.add_handler(CallbackQueryHandler(theme_selection, pattern='^theme_'))
    app.add_handler(CallbackQueryHandler(layout_selection, pattern='^layout_'))
    app.add_handler(CallbackQueryHandler(template_selection, pattern='^template_'))
    app.add_handler(CallbackQueryHandler(font_category_selection, pattern='^font_category_'))
    app.add_handler(CallbackQueryHandler(font_choice_selection, pattern='^font_choice_'))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_error_handler(error_handler)

    logger.info("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()
