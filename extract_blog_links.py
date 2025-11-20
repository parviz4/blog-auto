#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

BLOG_URL = "https://rasta4u.blogfa.com"

def extract_active_blog_links():
    """استخراج تمام لینک‌های فعال وبلاگ"""
    print("🔍 درحال استخراج لینک‌های وبلاگ...\n")
    
    try:
        response = requests.get(BLOG_URL, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        active_links = {}
        
        # استخراج تمام لینک‌های post (مقالات)
        print("📄 مقالات:")
        post_links = []
        for link in soup.find_all('a', href=True):
            url = link['href']
            text = link.get_text(strip=True)
            
            if '/post/' in url and text and len(text) > 3:
                full_url = urljoin(BLOG_URL, url)
                if full_url not in [l['url'] for l in post_links]:
                    post_links.append({
                        'title': text[:100],
                        'url': full_url
                    })
                    print(f"  ✅ {text[:60]}")
        
        active_links['posts'] = post_links
        
        # استخراج دسته‌بندی‌ها
        print(f"\n📂 دسته‌بندی‌ها:")
        category_links = []
        for link in soup.find_all('a', href=True):
            if '/category/' in link['href']:
                full_url = urljoin(BLOG_URL, link['href'])
                text = link.get_text(strip=True)
                
                if text and len(text) > 2 and full_url not in [l['url'] for l in category_links]:
                    category_links.append({
                        'title': f"دسته: {text}",
                        'url': full_url
                    })
                    print(f"  ✅ {text}")
        
        active_links['categories'] = category_links
        
        # ذخیره در فایل
        with open('active_blog_links.json', 'w', encoding='utf-8') as f:
            json.dump(active_links, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {len(post_links)} مقاله + {len(category_links)} دسته = کل {len(post_links) + len(category_links)} لینک")
        print("📁 ذخیره شد: active_blog_links.json\n")
        
        return active_links
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        return {}

if __name__ == '__main__':
    extract_active_blog_links()
