TEMPLATES = {
    "minimalistic": {
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width={width}">
    <title>Minimalistic Template</title>
    {extra_head}
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: {font_body};
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1, h2, h3, h4 {{
            font-family: {font_header};
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: {font_code};
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
    {extra_head}
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: {font_body};
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1, h2, h3, h4 {{
            font-family: {font_header};
            font-weight: 300;
        }}
        pre {{
            background-color: #eaeaea;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: {font_code};
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
    {extra_head}
    <style>
        body {{
            margin: 0;
            padding: {padding}px;
            font-family: {font_body};
            font-size: {font_size}px;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}
        h1, h2, h3, h4 {{
            font-family: {font_header};
            font-weight: bold;
        }}
        pre {{
            background-color: #fafafa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            font-family: {font_code};
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
