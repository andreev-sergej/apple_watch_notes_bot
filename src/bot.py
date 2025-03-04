import logging
import os

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers import (
    error_handler,
    font_size_selection,
    handle_document,
    handle_pdf,
    handle_preview,
    handle_qrcode,
    handle_text,
    layout_selection,
    model_selection,
    select_font_size,
    select_layout,
    select_template,
    select_theme,
    select_watch_model,
    set_padding,
    start,
    template_selection,
    theme_selection,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
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
    app.add_handler(CommandHandler("preview", handle_preview))
    app.add_handler(CommandHandler("pdf", handle_pdf))
    app.add_handler(CommandHandler("qrcode", handle_qrcode))

    app.add_handler(
        CallbackQueryHandler(model_selection, pattern="^(se_|series_|ultra_)")
    )
    app.add_handler(CallbackQueryHandler(font_size_selection, pattern="^font_"))
    app.add_handler(CallbackQueryHandler(theme_selection, pattern="^theme_"))
    app.add_handler(CallbackQueryHandler(layout_selection, pattern="^layout_"))
    app.add_handler(CallbackQueryHandler(template_selection, pattern="^template_"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_error_handler(error_handler)

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
