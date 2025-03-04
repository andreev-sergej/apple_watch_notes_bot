import pytest
from src.renderer import build_html


def test_build_html_minimalistic():
    text = "# Hello World"
    model = {"width": 400, "height": 400}
    font_multiplier = 1.0
    theme = "light"
    padding = 20
    template_style = "minimalistic"

    html = build_html(text, model, font_multiplier, theme, padding, template_style)
    assert "<h1>" in html
    assert "Hello World" in html
    assert f"padding: {padding}px;" in html
