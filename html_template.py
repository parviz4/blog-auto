#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def create_html_article(title, content, image_url):
    """
    یک قالب HTML زیبا و حرفه‌ای برای مقاله تولید می‌کند.
    این تابع شامل CSS داخلی برای اطمینان از سازگاری با ویرایشگر بلاگفا است.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');

            .article-container {{
                font-family: 'Vazirmatn', sans-serif;
                line-height: 1.8;
                color: #333;
                background-color: #f9f9f9;
                border-radius: 12px;
                padding: 25px;
                margin: 20px auto;
                max-width: 900px;
                border: 1px solid #e1e1e1;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                direction: rtl;
                text-align: right;
            }}
            .article-header h1 {{
                font-size: 28px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 20px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            .article-image {{
                width: 100%;
                max-height: 450px;
                object-fit: cover;
                border-radius: 8px;
                margin-bottom: 25px;
            }}
            .article-content p {{
                font-size: 17px;
                margin-bottom: 1.5em;
                text-align: justify;
            }}
            .article-content a {{
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
                transition: color 0.3s ease;
            }}
            .article-content a:hover {{
                color: #2980b9;
                text-decoration: underline;
            }}
            .internal-links {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
            }}
            .internal-links h3 {{
                font-size: 20px;
                color: #2c3e50;
            }}
            .internal-links ul {{
                list-style: none;
                padding: 0;
            }}
            .internal-links li {{
                margin-bottom: 10px;
            }}
            .internal-links a {{
                font-size: 16px;
                color: #3498db;
            }}
            @media (max-width: 768px) {{
                .article-container {{
                    padding: 15px;
                }}
                .article-header h1 {{
                    font-size: 24px;
                }}
                .article-content p {{
                    font-size: 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="article-container">
            <header class="article-header">
                <h1>{title}</h1>
            </header>
            <img src="{image_url}" alt="{title}" class="article-image">
            <div class="article-content">
                {content}
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

# مثال برای تست
if __name__ == '__main__':
    sample_title = "آشنایی با خاک‌شناسی مهندسی"
    sample_content = """
    <p>خاک‌شناسی یکی از علوم بنیادی در مهندسی عمران است که به مطالعه خواص فیزیکی، شیمیایی و مکانیکی خاک می‌پردازد. درک صحیح از رفتار خاک برای طراحی سازه‌هایی مانند پی‌ها، دیوارها و سدها ضروری است.</p>
    <div class="internal-links">
        <h3>مطالب مرتبط</h3>
        <ul>
            <li><a href="#">طراحی پی‌های سطحی</a></li>
            <li><a href="#">مقاومت برشی خاک</a></li>
        </ul>
    </div>
    """
    sample_image = "https://images.unsplash.com/photo-1594488518062-885744a1e94c?w=900"

    html_output = create_html_article(sample_title, sample_content, sample_image)

    # ذخیره در یک فایل برای پیش‌نمایش
    with open("article_preview.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("✅ پیش‌نمایش مقاله در `article_preview.html` ذخیره شد.")
