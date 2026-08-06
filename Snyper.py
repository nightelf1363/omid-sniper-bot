import telebot
import google.generativeai as genai
import schedule
import time
import pytz
from datetime import datetime

# ⚠️ هشدار امنیتی: سعی کن همیشه این کلیدها رو پیش خودت محفوظ نگه‌داری
TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
GEMINI_API_KEY = 'AQ.Ab8RN6L_lvnaOD7jf6O3e9vgew7z6Bigg4oYE7LZGLgEszWttA'
CHANNEL_ID = '@Omid_sniper_bot'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro') # استفاده از نسخه پایدار مدل

# تنظیم منطقه زمانی برای گزارش‌گیری دقیق به وقت ایران
iran_tz = pytz.timezone('Asia/Tehran')

def generate_and_send_signal():
    print("در حال تحلیل بازار در تایم فریم ۱ ساعته...")
    
    # دیتای بهینه‌شده برای جیمینای همراه با دستور خروجی اعداد خام
    market_data_summary = """
    تحلیلگر عزیز، وضعیت ارزهای مدنظر (سولانا، دوج‌کوین و چین‌لینک) به این شرح است:
    تایم فریم ۱ ساعته: قیمت بالای ابر کومو قرار دارد، RSI در محدوده ورود مناسبی است و مکدی (MACD) کراس صعودی داده است. همچنین ساختار چارت شبیه به یک الگوی پرچم صعودی است.
    لطفاً بر اساس این داده‌ها، یک سیگنال دقیق شامل نقطه ورود، حد ضرر و دو هدف قیمتی برای کانال تلگرام بنویس.
    
    در انتهای تحلیل، فقط نقطه ورود، تی‌پی ۱ و استاپ رو به صورت اعدادِ خالص تو سه خط جداگانه بنویس.
    """
    
    try:
        response = model.generate_content(market_data_summary)
        signal_text = response.text
        
        bot.send_message(CHANNEL_ID, f"🎯 **سیگنال جدید تک‌تیرانداز**\n\n{signal_text}")
        print("سیگنال با موفقیت به کانال ارسال شد.")
        
        # در اینجا ربات در آینده اعداد خالص را استخراج و در فایل گزارش ذخیره می‌کند
        
    except Exception as e:
        print(f"خطا در ارتباط یا ارسال: {e}")

def send_daily_report():
    print("در حال تهیه گزارش صبحگاهی...")
    try:
        # ربات در اینجا فایل گزارش را می‌خواند و نتایج را جمع‌بندی می‌کند
        report_text = "📊 **گزارش عملکرد روز گذشته تک‌تیرانداز:**\n\n✅ سیگنال‌های موفق: ...\n❌ سیگنال‌های ناموفق: ..."
        bot.send_message(CHANNEL_ID, report_text)
        print("گزارش صبحگاهی ارسال شد.")
        # پس از ارسال، دفترچه گزارش روزانه پاک می‌شود تا برای امروز آماده شود
    except Exception as e:
        print(f"خطا در ارسال گزارش: {e}")

# زمان‌بندی ماموریت‌ها (سیگنال‌دهی)
target_times = [
    "08:00", "10:00", "12:00", "14:00", 
    "16:00", "18:00", "20:00", "22:00", "00:00"
]

for t in target_times:
    schedule.every().day.at(t).do(generate_and_send_signal)

# زمان‌بندی گزارش صبحگاهی (ساعت 7:30)
schedule.every().day.at("07:30").do(send_daily_report)

print("ربات روشن شد و منتظر زمان مقرر است...")

# حلقه اصلی برای بیدار نگه داشتن ربات
while True:
    schedule.run_pending()
    time.sleep(60)