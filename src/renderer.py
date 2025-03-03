import logging
from io import BytesIO

import markdown
import imgkit
from PIL import Image
import pdfkit

from config import PAGE_OVERLAP

logger = logging.getLogger(__name__)

def get_html_preview(text: str, model: dict, font_multiplier: float, theme: str, padding: int) -> str:
    base_font_size = 16
    html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    if theme == "light":
        bg_color = "white"
        text_color = "black"
    else:
        bg_color = "black"
        text_color = "white"
    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width={model['width']}">
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
          html, body {{
            width: {model['width']}px;
            margin: 0;
            padding: {padding}px;
            box-sizing: border-box;
            background-color: {bg_color};
            color: {text_color};
          }}
          body {{
            font-family: sans-serif;
            font-size: {base_font_size * font_multiplier}px;
            line-height: 1.4;
          }}
          h1 {{ font-size: {2.0 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h2 {{ font-size: {1.75 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h3 {{ font-size: {1.5 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h4 {{ font-size: {1.25 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          pre {{
            background-color: #333;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
          }}
          code {{
            font-family: monospace;
            background-color: #333;
            padding: 2px 4px;
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        {html_body}
      </body>
    </html>
    """
    return html

def render_markdown_to_image(text: str, model: dict, font_multiplier: float, theme: str, padding: int) -> list:
    base_font_size = 16
    html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    if theme == "light":
        bg_color = "white"
        text_color = "black"
    else:
        bg_color = "black"
        text_color = "white"
    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width={model['width']}, height={model['height']}">
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
          html, body {{
            width: {model['width']}px;
            height: {model['height']}px;
            margin: 0;
            padding: {padding}px;
            box-sizing: border-box;
            background-color: {bg_color};
            color: {text_color};
          }}
          body {{
            font-family: sans-serif;
            font-size: {base_font_size * font_multiplier}px;
            line-height: 1.4;
          }}
          h1 {{ font-size: {2.0 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h2 {{ font-size: {1.75 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h3 {{ font-size: {1.5 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h4 {{ font-size: {1.25 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          pre {{
            background-color: #333;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
          }}
          code {{
            font-family: monospace;
            background-color: #333;
            padding: 2px 4px;
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        {html_body}
      </body>
    </html>
    """
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
        logger.error("Error rendering Markdown to image", exc_info=e)
        raise e
    buf = BytesIO(img_bytes)
    return [buf]

def render_markdown_to_images_paginated(text: str, model: dict, font_multiplier: float, theme: str, padding: int) -> list:
    base_font_size = 16
    html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    if theme == "light":
        bg_color = "white"
        text_color = "black"
    else:
        bg_color = "black"
        text_color = "white"
    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width={model['width']}">
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
          html, body {{
            width: {model['width']}px;
            margin: 0;
            padding: {padding}px;
            box-sizing: border-box;
            background-color: {bg_color};
            color: {text_color};
          }}
          body {{
            font-family: sans-serif;
            font-size: {base_font_size * font_multiplier}px;
            line-height: 1.4;
          }}
          h1 {{ font-size: {2.0 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h2 {{ font-size: {1.75 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h3 {{ font-size: {1.5 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h4 {{ font-size: {1.25 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          pre {{
            background-color: #333;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
          }}
          code {{
            font-family: monospace;
            background-color: #333;
            padding: 2px 4px;
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        {html_body}
      </body>
    </html>
    """
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

def render_markdown_to_pdf(text: str, model: dict, font_multiplier: float, theme: str, padding: int) -> BytesIO:
    base_font_size = 16
    html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    if theme == "light":
        bg_color = "white"
        text_color = "black"
    else:
        bg_color = "black"
        text_color = "white"
    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width={model['width']}">
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
          html, body {{
            width: {model['width']}px;
            margin: 0;
            padding: {padding}px;
            box-sizing: border-box;
            background-color: {bg_color};
            color: {text_color};
          }}
          body {{
            font-family: sans-serif;
            font-size: {base_font_size * font_multiplier}px;
            line-height: 1.4;
          }}
          h1 {{ font-size: {2.0 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h2 {{ font-size: {1.75 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h3 {{ font-size: {1.5 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          h4 {{ font-size: {1.25 * base_font_size * font_multiplier}px; margin: 0.5em 0; }}
          pre {{
            background-color: #333;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
          }}
          code {{
            font-family: monospace;
            background-color: #333;
            padding: 2px 4px;
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        {html_body}
      </body>
    </html>
    """
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
