#!/usr/bin/env python3
# -*- a: utf-8 -*-
import json
import random
import hashlib
from datetime import datetime
from html_template import create_html_article

# موضوعات مقالات با کلمات کلیدی
ARTICLE_TOPICS = [
    {"title": "خاک‌شناسی مهندسی: مبانی و کاربردها", "keywords": "خاک‌شناسی, مهندسی عمران, ژئوتکنیک, مکانیک خاک, آزمایش خاک", "content": "خاک به عنوان یکی از اصلی‌ترین مصالح در پروژه‌های عمرانی، نقشی حیاتی ایفا می‌کند. درک صحیح از خصوصیات فیزیکی و مکانیکی آن برای اطمینان از پایداری سازه‌ها ضروری است. این مقاله به بررسی مبانی خاک‌شناسی و کاربردهای آن در پروژه‌های مدرن می‌پردازد."},
    {"title": "طراحی پیشرفته پی‌ها در ساختمان‌های بلند", "keywords": "طراحی پی, پی عمیق, پی سطحی, باربری خاک, ساختمان بلند", "content": "با افزایش ارتفاع ساختمان‌ها، طراحی پی‌ها به یک چالش مهندسی پیچیده تبدیل شده است. پی‌های عمیق و شمعی راه‌حل‌هایی هستند که بارهای عظیم را به لایه‌های مقاوم‌تر زمین منتقل می‌کنند. در این مطلب، با جدیدترین تکنیک‌های طراحی پی آشنا می‌شوید."},
    {"title": "فناوری‌های نوین در بهسازی خاک‌های ضعیف", "keywords": "بهسازی خاک, تزریق پرفشار, ستون شنی, ژئوسنتتیک, خاک ضعیف", "content": "بسیاری از پروژه‌ها در مناطقی با خاک‌های ضعیف و نامناسب اجرا می‌شوند. فناوری‌های نوینی مانند تزریق پرفشار (Jet Grouting) و استفاده از ژئوسنتتیک‌ها به مهندسان اجازه می‌دهند تا ظرفیت باربری این خاک‌ها را به شکل چشمگیری افزایش دهند."}
]

def get_unique_image_url(title):
    """
    یک URL تصویر منحصر به فرد و ثابت بر اساس عنوان مقاله با استفاده از picsum.photos تولید می‌کند.
    این روش نیازی به کلید API ندارد.
    """
    # استفاده از هش عنوان برای تولید یک شناسه عددی منحصر به فرد
    seed = int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % 1000
    # ابعاد تصویر ۹۰۰ در ۴۵۰ برای نمایش بهتر
    image_url = f"https://picsum.photos/seed/{seed}/900/450"
    return image_url

def load_blog_links():
    """
    لینک‌های فعال وبلاگ را از فایل `active_blog_links.json` بارگذاری می‌کند.
    """
    try:
        with open('active_blog_links.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('posts', [])[:8]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def format_internal_links(blog_links):
    """
    لینک‌های داخلی را به صورت یک بخش HTML زیبا قالب‌بندی می‌کند.
    """
    if not blog_links:
        return ""

    selected_links = random.sample(blog_links, min(3, len(blog_links)))

    links_html = '<div class="internal-links">\n<h3>مطالب مرتبط</h3>\n<ul>\n'
    for link in selected_links:
        links_html += f'    <li><a href="{link.get("url", "#")}" target="_blank">{link.get("title", "مقاله مرتبط")}</a></li>\n'
    links_html += '</ul>\n</div>'
    return links_html

def generate_articles():
    """
    مقالات را با استفاده از قالب HTML، تصاویر منحصر به فرد و لینک‌های داخلی تولید می‌کند.
    """
    print("📝 درحال تولید مقالات پیشرفته...\n")

    blog_links = load_blog_links()
    articles_to_publish = []

    for topic in ARTICLE_TOPICS:
        print(f"  - در حال پردازش: {topic['title']}")

        # ۱. تولید URL تصویر منحصر به فرد
        image_url = get_unique_image_url(topic['title'])
        print(f"    🖼️ تصویر انتخاب شد: {image_url}")

        # ۲. قالب‌بندی لینک‌های داخلی
        internal_links_html = format_internal_links(blog_links)

        # ۳. ترکیب محتوای اصلی و لینک‌ها
        full_content_html = f"<p>{topic['content']}</p>\n{internal_links_html}"

        # ۴. تولید HTML نهایی مقاله
        final_html = create_html_article(topic['title'], full_content_html, image_url)

        # ۵. آماده‌سازی داده برای فایل JSON
        article_data = {
            "title": topic['title'],
            "keywords": ", ".join(topic['keywords'].split(',')[:5]),
            "html_content": final_html,
            "date_generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        articles_to_publish.append(article_data)

    random.shuffle(articles_to_publish)
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump({"articles": articles_to_publish}, f, ensure_ascii=False, indent=4)

    print(f"\n✅ {len(articles_to_publish)} مقاله با فرمت HTML پیشرفته آماده و در `articles.json` ذخیره شد!\n")

if __name__ == '__main__':
    generate_articles()
