from telegram.ext import ContextTypes

from config import DEFAULT_PADDING, WATCH_MODELS


def get_user_model(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get("watch_model", WATCH_MODELS["series_45mm"])


def get_padding(context: ContextTypes.DEFAULT_TYPE) -> int:
    return context.user_data.get("padding", DEFAULT_PADDING)
