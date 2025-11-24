#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

BLOG_URL = "https://rasta4u.blogfa.com"

def extract_blog_links():
    print("🔍 درحال استخراج لینک‌های وبلاگ...\n")
    try:
        response = requests.get(BLOG_URL, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        post_links = []
        for link in soup.find_all('a', href=True):
            url = link['href']
            text = link.get_text(strip=True)
            if '/post/' in url and text and len(text) > 3:
                full_url = urljoin(BLOG_URL, url)
                if full_url not in [item['url'] for item in post_links]:
                    post_links.append({'title': text[:80], 'url': full_url})
                    print(f"  ✅ {text[:60]}")
        with open('active_blog_links.json', 'w', encoding='utf-8') as f:
            json.dump({'posts': post_links, 'total': len(post_links)}, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {len(post_links)} لینک استخراج شد\n")
        return post_links
    except Exception as e:
        print(f"❌ خطا: {e}\n")
        return []

if __name__ == '__main__':
    extract_blog_links()
