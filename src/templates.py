TEMPLATES = {
    "minimalistic": {
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width={width}">
    <title>Minimalistic Template</title>
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: Arial, sans-serif;
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1 {{ font-size: {h1_size}px; }}
        h2 {{ font-size: {h2_size}px; }}
        h3 {{ font-size: {h3_size}px; }}
        h4 {{ font-size: {h4_size}px; }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: monospace;
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
    },
    "modern": {
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width={width}">
    <title>Modern Template</title>
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1 {{ font-size: {h1_size}px; font-weight: 300; }}
        h2 {{ font-size: {h2_size}px; font-weight: 300; }}
        h3 {{ font-size: {h3_size}px; font-weight: 300; }}
        h4 {{ font-size: {h4_size}px; font-weight: 300; }}
        pre {{
            background-color: #eaeaea;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: monospace;
            background-color: #eaeaea;
            padding: 2px 4px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
    },
    "classic": {
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width={width}">
    <title>Classic Template</title>
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: 'Times New Roman', serif;
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1 {{ font-size: {h1_size}px; font-weight: bold; }}
        h2 {{ font-size: {h2_size}px; font-weight: bold; }}
        h3 {{ font-size: {h3_size}px; font-weight: bold; }}
        h4 {{ font-size: {h4_size}px; font-weight: bold; }}
        pre {{
            background-color: #fafafa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: monospace;
            background-color: #fafafa;
            padding: 2px 4px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
    }
}