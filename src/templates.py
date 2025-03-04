TEMPLATES = {
    "minimalistic": {
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width={width}">
    <title>Minimalistic Template - Watch Markdown Renderer</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            background: linear-gradient(135deg, #ececec, #f9f9f9);
            font-family: 'Roboto', sans-serif;
        }}
        .container {{
            max-width: {width}px;
            margin: 20px auto;
            padding: {padding}px;
            background-color: {bg_color};
            color: {text_color};
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
    <div class="container">
        {content}
    </div>
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
    <title>Modern Template - Watch Markdown Renderer</title>
    <link href="https://fonts.googleapis.com/css?family=Helvetica+Neue:400,500,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            background: linear-gradient(135deg, #ffffff, #f0f0f0);
            font-family: 'Helvetica Neue', sans-serif;
        }}
        .container {{
            max-width: {width}px;
            margin: 20px auto;
            padding: {padding}px;
            background-color: {bg_color};
            color: {text_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
    <div class="container">
        {content}
    </div>
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
    <title>Classic Template - Watch Markdown Renderer</title>
    <link href="https://fonts.googleapis.com/css?family=Times+New+Roman:400,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            background: #f7f7f7;
            font-family: 'Times New Roman', serif;
        }}
        .container {{
            max-width: {width}px;
            margin: 20px auto;
            padding: {padding}px;
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid #ddd;
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
    <div class="container">
        {content}
    </div>
</body>
</html>
"""
    }
}
