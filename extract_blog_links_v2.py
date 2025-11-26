#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import concurrent.futures

BLOG_URL = "https://rasta4u.blogfa.com"
MAX_WORKERS = 10

def is_internal_post_link(url):
    """بررسی می‌کند که آیا لینک یک پست داخلی وبلاگ است یا خیر."""
    parsed_url = urlparse(url)
    return parsed_url.path.startswith('/post/')

def check_link_health(url):
    """بررسی می‌کند که آیا لینک سالم است یا خیر."""
    try:
        response = requests.head(url, timeout=8, allow_redirects=True)
        if response.status_code == 200:
            print(f"  ✅ [200] {url.split('/')[-1]}")
            return url
    except requests.RequestException:
        pass
    return None

def extract_blog_links():
    """لینک‌های وبلاگ را استخراج و سلامت آن‌ها را بررسی می‌کند."""
    print("🔍 درحال استخراج لینک‌های وبلاگ...\n")
    try:
        response = requests.get(BLOG_URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        post_links = []
        seen_urls = set()

        for link in soup.find_all('a', href=True):
            url = link['href']
            text = link.get_text(strip=True)

            full_url = urljoin(BLOG_URL, url)

            if is_internal_post_link(full_url) and text and full_url not in seen_urls:
                post_links.append({'title': text.strip(), 'url': full_url})
                seen_urls.add(full_url)

        print(f"🔗 {len(post_links)} لینک داخلی پیدا شد. در حال بررسی سلامت...\n")

        active_links = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(check_link_health, item['url']): item for item in post_links}
            for future in concurrent.futures.as_completed(future_to_url):
                item = future_to_url[future]
                if future.result():
                    active_links.append(item)

        with open('active_blog_links.json', 'w', encoding='utf-8') as f:
            json.dump({'posts': active_links, 'total': len(active_links)}, f, ensure_ascii=False, indent=2)

        print(f"\n✅ {len(active_links)} لینک سالم استخراج و ذخیره شد.\n")
        return active_links

    except requests.RequestException as e:
        print(f"❌ خطا در اتصال به وبلاگ: {e}\n")
        return []

if __name__ == '__main__':
    extract_blog_links()
