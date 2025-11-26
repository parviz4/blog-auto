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

# بارگذاری متغیرهای محیطی از config.env
load_dotenv('config.env')

BLOGFA_USERNAME = os.getenv('BLOGFA_USERNAME')
BLOGFA_PASSWORD = os.getenv('BLOGFA_PASSWORD')

def should_post_now():
    """بررسی می‌کند که آیا زمان فعلی برای ارسال پست مناسب است یا خیر."""
    now = datetime.now()
    # روزهای هفته در پایتون: دوشنبه=۰, یکشنبه=۶
    # ارسال فقط در روزهای کاری (شنبه تا چهارشنبه)
    if now.weekday() in [4, 5]:  # پنج‌شنبه و جمعه
        print(f"⏸️ امروز {now.strftime('%A')} است. ارسال متوقف شد.")
        return False
    # ارسال فقط در ساعات کاری (۸ صبح تا ۸ شب)
    if not 8 <= now.hour < 20:
        print(f"⏸️ ساعت فعلی {now.hour} خارج از بازه زمانی مجاز است.")
        return False
    return True

def load_articles():
    """مقالات را از فایل articles.json بارگذاری می‌کند."""
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        articles = data.get('articles', [])
        print(f"✅ {len(articles)} مقاله بارگذاری شد.")
        return articles
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ خطا در بارگذاری مقالات: {e}")
        return []

def select_random_article(articles):
    """یک مقاله تصادفی که قبلاً پست نشده را انتخاب می‌کند."""
    return random.choice(articles) if articles else None

def login_to_blogfa(driver):
    """وارد مدیریت وبلاگ بلاگفا می‌شود."""
    print("\n🔗 در حال اتصال به بلاگفا...")
    try:
        driver.get('https://blogfa.com/desktop/login.aspx')
        wait = WebDriverWait(driver, 30)

        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='usrid']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='ups']")

        username_field.clear()
        username_field.send_keys(BLOGFA_USERNAME)
        print(f"  - نام کاربری: {BLOGFA_USERNAME}")

        password_field.clear()
        password_field.send_keys(BLOGFA_PASSWORD)
        print("  - رمز عبور وارد شد.")

        login_button = driver.find_element(By.CSS_SELECTOR, "input[name='btnSubmit']")
        login_button.click()

        wait.until(EC.url_contains('/desktop/Main.aspx'))
        print("✅ ورود موفق!")
        return True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ خطا در فرآیند ورود: {e.__class__.__name__}")
        driver.save_screenshot('login_error_screenshot.png')
        with open('login_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        return False

def post_html_article(driver, article):
    """یک مقاله با محتوای HTML در بلاگفا ارسال می‌کند."""
    print("\n📝 در حال ارسال مقاله به صورت HTML...")
    try:
        driver.get('https://blogfa.com/desktop/Post.aspx?action=new')
        wait = WebDriverWait(driver, 20)

        title_input = wait.until(EC.presence_of_element_located((By.ID, 'Title')))
        title_input.clear()
        title_input.send_keys(article['title'])
        print(f"  - عنوان: {article['title'][:60]}...")

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'Body_ifr')))
        editor_body = driver.find_element(By.TAG_NAME, 'body')

        driver.execute_script("arguments[0].innerHTML = arguments[1];", editor_body, article['html_content'])
        print(f"  - محتوای HTML با حجم {len(article['html_content'])} بایت با موفقیت تزریق شد.")

        driver.switch_to.default_content()

        keywords_input = driver.find_element(By.ID, 'Tags')
        keywords_input.clear()
        keywords_input.send_keys(article['keywords'])
        print(f"  - کلمات کلیدی: {article['keywords']}")

        publish_button = driver.find_element(By.ID, 'btnSubmit')
        publish_button.click()

        wait.until(EC.url_contains('/desktop/Posts.aspx'))
        print("\n✅✅✅ مقاله با موفقیت منتشر شد!")
        return True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"❌ خطا در ارسال مقاله: {e.__class__.__name__}")
        driver.save_screenshot('post_error_screenshot.png')
        print("  - اسکرین‌شات خطا در 'post_error_screenshot.png' ذخیره شد.")
        return False

def main():
    """تابع اصلی برای اجرای کل فرآیند."""
    print("\n" + "="*60)
    print("🚀 سیستم خودکار ارسال مقالات HTML به بلاگفا")
    print("="*60)
    print(f"⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if not should_post_now():
        return

    if not all([BLOGFA_USERNAME, BLOGFA_PASSWORD]):
        print("❌ خطا: نام کاربری یا رمز عبور در فایل config.env تنظیم نشده است.")
        return

    articles = load_articles()
    if not articles:
        print("❌ هیچ مقاله‌ای برای ارسال وجود ندارد.")
        return

    article_to_post = select_random_article(articles)
    if not article_to_post:
        print("❌ خطای داخلی: مقاله‌ای انتخاب نشد.")
        return

    print(f"🎲 مقاله انتخابی: {article_to_post['title']}")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        if login_to_blogfa(driver):
            post_html_article(driver, article_to_post)

    except Exception as e:
        print(f"❌ یک خطای غیرمنتظره رخ داد: {e}")

    finally:
        if driver:
            driver.quit()
        print("\n" + "="*60)
        print("✅ عملیات به پایان رسید.")
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
