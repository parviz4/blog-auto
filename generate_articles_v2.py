#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime

ARTICLE_TEMPLATES = [
    {"title": "خاک‌شناسی مهندسی", "keywords": "خاک‌شناسی، خصوصیات خاک", "content": "خاک یکی از مهم‌ترین مصالح است..."},
    {"title": "طراحی پی‌ها", "keywords": "پی سطحی، فشار تحمل", "content": "پی‌های سطحی برای ساختمان‌های..."},
    {"title": "بهسازی خاک", "keywords": "بهسازی، تقویت خاک", "content": "خاک‌های ضعیف می‌توانند..."}
]

def load_blog_links():
    try:
        with open('active_blog_links.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('posts', [])[:8]
    except:
        return []

def add_internal_links(content, blog_links):
    if not blog_links:
        return content
    selected = random.sample(blog_links, min(3, len(blog_links)))
    links_text = "\n\n### مطالب مرتبط\n"
    for link in selected:
        links_text += f"• [{link.get('title', 'بدون عنوان')}]({link.get('url', '#')})\n"
    return content + links_text

def generate_articles():
    print("📝 درحال تولید مقالات...\n")
    blog_links = load_blog_links()
    articles = []
    for template in ARTICLE_TEMPLATES:
        article = template.copy()
        article['content'] = add_internal_links(article['content'], blog_links)
        article['date'] = datetime.now().strftime('%Y-%m-%d')
        articles.append(article)
        print(f"✅ {article['title']}")
    random.shuffle(articles)
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(articles)} مقاله آماده شد!\n")

if __name__ == '__main__':
    generate_articles()
