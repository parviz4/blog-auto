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
from webdriver_manager.chrome import ChromeDriverManager

# بارگذاری متغیرهای محیطی
try:
    load_dotenv('config.env')
except:
    pass

BLOGFA_USERNAME = os.getenv('BLOGFA_USERNAME', 'perplex@rasta4u')
BLOGFA_PASSWORD = os.getenv('BLOGFA_PASSWORD', '123456789')

def load_articles():
    """بارگذاری مقالات از فایل JSON"""
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {len(data['articles'])} مقاله بارگذاری شد")
        return data['articles']
    except Exception as e:
        print(f"❌ خطا در بارگذاری مقالات: {e}")
        return []

def select_random_article(articles):
    """انتخاب یک مقالهٔ تصادفی"""
    if not articles:
        return None
    return random.choice(articles)

def login_to_blogfa(driver):
    """ورود به blogfa"""
    print("\n🔗 اتصال به blogfa...")
    try:
        driver.get('https://blogfa.com/desktop/login.aspx')
        time.sleep(3)
        
        # یافتن فیلدهای ورود
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
        )
        
        if len(username_field) >= 2:
            username_field[0].clear()
            username_field[0].send_keys(BLOGFA_USERNAME)
            print(f"✅ نام کاربری: {BLOGFA_USERNAME}")
            
            # رمز عبور
            username_field[1].clear()
            username_field[1].send_keys(BLOGFA_PASSWORD)
            print("✅ رمز عبور وارد شد")
        else:
            print("❌ خطا: فیلدهای ورود پیدا نشد")
            return False
        
        # کلیک بر دکمهٔ ورود
        time.sleep(1)
        login_buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in login_buttons:
            if "ورود" in btn.text or "login" in btn.text.lower():
                btn.click()
                break
        
        time.sleep(5)
        print("✅ ورود موفق!")
        return True
        
    except Exception as e:
        print(f"❌ خطا در ورود: {e}")
        return False

def post_article(driver, article):
    """ارسال مقاله به blogfa"""
    print("\n📝 ارسال مقاله...")
    try:
        driver.get('https://blogfa.com/desktop/Post.aspx?action=new')
        time.sleep(3)
        
        # عنوان
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='عنوان'], input[placeholder*='title']"))
        )
        title_input.clear()
        title_input.send_keys(article['title'])
        print(f"✅ عنوان: {article['title'][:50]}...")
        
        # متن - بررسی textarea
        content_fields = driver.find_elements(By.TAG_NAME, "textarea")
        if content_fields:
            content_fields[0].clear()
            content_fields[0].send_keys(article['content'])
            print(f"✅ متن ({len(article['content'])} کاراکتر)")
        
        # کلمات کلیدی
        keyword_inputs = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='کلید'], input[placeholder*='keyword']")
        if keyword_inputs:
            keyword_inputs[0].clear()
            keyword_inputs[0].send_keys(article['keywords'])
            print(f"✅ کلمات کلیدی")
        
        # انتشار
        time.sleep(2)
        publish_buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in publish_buttons:
            if "انتشار" in btn.text or "publish" in btn.text.lower():
                btn.click()
                break
        
        time.sleep(3)
        print("✅✅✅ مقاله با موفقیت منتشر شد!")
        return True
        
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")
        import traceback
        traceback.print_exc()
        return False

def should_post_now():
    """بررسی زمان مناسب"""
    now = datetime.now()
    
    # فقط شنبه تا چهارشنبه (روزهای 1-5 در Python: 0=دوشنبه)
    if now.weekday() > 4:  # جمعه یا شنبه
        print(f"⏸ امروز جمعه یا شنبه - منتشر نمی‌شود")
        return False
    
    # فقط 8 صبح تا 8 شب
    if now.hour < 8 or now.hour >= 20:
        print(f"⏸ ساعت {now.hour} - فقط 8 صبح تا 8 شب")
        return False
    
    return True

def main():
    """تابع اصلی"""
    print("\n" + "="*60)
    print("🚀 سیستم خودکار ارسال مقالات blogfa")
    print("="*60)
    print(f"⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # بررسی زمان
    if not should_post_now():
        print("\n❌ زمان مناسب نیست\n")
        return
    
    # بارگذاری مقالات
    articles = load_articles()
    if not articles:
        print("❌ هیچ مقاله‌ای موجود نیست!")
        return
    
    # انتخاب مقالهٔ تصادفی
    article = select_random_article(articles)
    if not article:
        print("❌ خطا در انتخاب مقاله")
        return
    
    print(f"🎲 انتخاب تصادفی: {article['title']}")
    
    # اتصال و ارسال
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        if login_to_blogfa(driver):
            post_article(driver, article)
    finally:
        driver.quit()
    
    print("\n" + "="*60)
    print("✅ کار تمام شد!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

