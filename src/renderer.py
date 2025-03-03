import logging
from io import BytesIO

import markdown
import imgkit
from PIL import Image
import pdfkit

from config import PAGE_OVERLAP
from templates import TEMPLATES

logger = logging.getLogger(__name__)

def build_html(text: str, model: dict, font_multiplier: float, theme: str, padding: int, template_style: str = "minimalistic") -> str:
    base_font_size = 16
    html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    
    if theme == "light":
        bg_color = "white"
        text_color = "black"
    else:
        bg_color = "black"
        text_color = "white"
    
    font_size = base_font_size * font_multiplier
    h1_size = 2.0 * base_font_size * font_multiplier
    h2_size = 1.75 * base_font_size * font_multiplier
    h3_size = 1.5 * base_font_size * font_multiplier
    h4_size = 1.25 * base_font_size * font_multiplier

    template = TEMPLATES.get(template_style, TEMPLATES["minimalistic"])["html"]

    html = template.format(
        width=model['width'],
        padding=padding,
        font_size=font_size,
        h1_size=h1_size,
        h2_size=h2_size,
        h3_size=h3_size,
        h4_size=h4_size,
        bg_color=bg_color,
        text_color=text_color,
        content=html_body
    )
    return html

def get_html_preview(text: str, model: dict, font_multiplier: float, theme: str, padding: int, template_style: str = "minimalistic") -> str:
    return build_html(text, model, font_multiplier, theme, padding, template_style)

def render_markdown_to_image(text: str, model: dict, font_multiplier: float, theme: str, padding: int, template_style: str = "minimalistic") -> list:
    html = build_html(text, model, font_multiplier, theme, padding, template_style)
    options = {
        'width': model['width'],
        'height': model['height'],
        'disable-smart-width': '',
        'encoding': "UTF-8",
        'javascript-delay': '2000'
    }
    try:
        img_bytes = imgkit.from_string(html, False, options=options)
    except Exception as e:
        logger.error("Ошибка рендеринга Markdown в изображение", exc_info=e)
        raise e
    buf = BytesIO(img_bytes)
    return [buf]

def render_markdown_to_images_paginated(text: str, model: dict, font_multiplier: float, theme: str, padding: int, template_style: str = "minimalistic") -> list:
    html = build_html(text, model, font_multiplier, theme, padding, template_style)
    options = {
        'width': model['width'],
        'disable-smart-width': '',
        'encoding': "UTF-8",
        'javascript-delay': '2000'
    }
    try:
        full_img_bytes = imgkit.from_string(html, False, options=options)
    except Exception as e:
        logger.error("Error rendering full Markdown to image", exc_info=e)
        raise e

    full_image = Image.open(BytesIO(full_img_bytes))
    full_width, full_height = full_image.size
    page_height = model['height']
    images = []

    num_pages = ((full_height - padding) + (page_height - PAGE_OVERLAP) - 1) // (page_height - PAGE_OVERLAP)
    for i in range(num_pages):
        top = i * (page_height - PAGE_OVERLAP)
        bottom = top + page_height
        if bottom > full_height:
            bottom = full_height
        box = (0, top, full_width, bottom)
        page_image = full_image.crop(box)
        buf = BytesIO()
        page_image.save(buf, format='PNG')
        buf.seek(0)
        images.append(buf)
    return images

def render_markdown_to_pdf(text: str, model: dict, font_multiplier: float, theme: str, padding: int, template_style: str = "minimalistic") -> BytesIO:
    html = build_html(text, model, font_multiplier, theme, padding, template_style)
    options = {
        'encoding': 'UTF-8',
    }
    try:
        pdf_bytes = pdfkit.from_string(html, False, options=options)
    except Exception as e:
        logger.error("Ошибка при конвертации в PDF", exc_info=e)
        raise e
    buf = BytesIO(pdf_bytes)
    return buf
