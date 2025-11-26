#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv('config.env')
BLOGFA_USERNAME = os.getenv('BLOGFA_USERNAME')
BLOGFA_PASSWORD = os.getenv('BLOGFA_PASSWORD')

def should_post_now():
    now = datetime.now()
    if now.weekday() in [4, 5]: return False
    if not 8 <= now.hour < 20: return False
    return True

def load_articles():
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('articles', [])
    except: return []

def select_random_article(articles):
    return random.choice(articles) if articles else None

def login_to_blogfa(driver):
    print("\n🔗 در حال اتصال به بلاگفا با حالت پیشرفته...")
    try:
        driver.get('https://blogfa.com/desktop/login.aspx')
        wait = WebDriverWait(driver, 30)
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='usrid']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='ups']")

        for char in BLOGFA_USERNAME:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

        for char in BLOGFA_PASSWORD:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

        login_button = driver.find_element(By.CSS_SELECTOR, "input[name='btnSubmit']")
        login_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'خروج')]")))
        print("✅ ورود موفقیت‌آمیز تأیید شد!")
        return True
    except Exception as e:
        print(f"❌ خطا در فرآیند ورود: {e.__class__.__name__}")
        driver.save_screenshot('login_error.png')
        return False

def post_html_article(driver, article):
    print("\n📝 در حال ارسال مقاله به صورت HTML...")
    try:
        driver.get('https://blogfa.com/desktop/Post.aspx?action=new')
        wait = WebDriverWait(driver, 30)

        title_input = wait.until(EC.presence_of_element_located((By.ID, 'txtPostTitle')))
        title_input.clear()
        title_input.send_keys(article['title'])
        print(f"  - عنوان: {article['title'][:60]}...")

        iframe_locator = (By.CSS_SELECTOR, "iframe.cke_wysiwyg_frame")
        wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_locator))

        editor_body = driver.find_element(By.TAG_NAME, 'body')
        driver.execute_script("arguments[0].innerHTML = arguments[1];", editor_body, article['html_content'])
        print(f"  - محتوای HTML تزریق شد.")

        driver.switch_to.default_content()

        keywords_input = driver.find_element(By.ID, 'txtTags')
        keywords_input.clear()
        keywords_input.send_keys(article['keywords'])
        print(f"  - کلمات کلیدی وارد شد.")

        publish_button = driver.find_element(By.ID, 'btnPublish')
        publish_button.click()
        print("  - دکمه انتشار کلیک شد. در حال انتظار برای پردازش سرور...")

        time.sleep(45)

        print("\n✅✅✅ مقاله با موفقیت منتشر شد!")
        return True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ خطا در ارسال مقاله: {e.__class__.__name__}")
        driver.save_screenshot('post_error_screenshot.png')
        return False

def main():
    print("\n" + "="*60)
    print("🚀 سیستم خودکار ارسال مقالات HTML به بلاگفا (حالت نهایی)")
    print("="*60)

    if not should_post_now(): return
    articles = load_articles()
    if not articles: return
    article_to_post = select_random_article(articles)
    if not article_to_post: return

    print(f"🎲 مقاله انتخابی: {article_to_post['title']}")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        if login_to_blogfa(driver):
            post_html_article(driver, article_to_post)
    finally:
        if driver: driver.quit()
        print("\n" + "="*60 + "\n✅ عملیات به پایان رسید.\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
