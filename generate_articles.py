#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime

# 25 الگوی مقالهٔ عمرانی
ARTICLE_TEMPLATES = [
    {"title": "خاک‌شناسی: درک خصوصیات فیزیکی و شیمیایی خاک", "keywords": "خاک‌شناسی، خصوصیات خاک، مهندسی عمران", "content": "خاک یکی از مهم‌ترین مصالح در مهندسی عمران است..."},
    {"title": "طراحی پی‌های سطحی: فشار تحمل‌پذیر", "keywords": "پی سطحی، فشار تحمل‌پذیر، طراحی", "content": "پی‌های سطحی برای منازل و ساختمان‌های کم‌ارتفاع..."},
    # ... مقالات دیگر
]

def generate_articles():
    """تولید 25 مقالهٔ جدید با ترتیب تصادفی"""
    random.shuffle(ARTICLE_TEMPLATES)
    data = {"articles": ARTICLE_TEMPLATES}
    
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(ARTICLE_TEMPLATES)} مقالهٔ جدید تولید شد!")

if __name__ == '__main__':
    generate_articles()
