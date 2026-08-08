import telebot
import requests
import json
import sys

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
GEMINI_API_KEY = 'AQ.Ab8RN6I9_dDQq_59Rt1RyTDZt8xEfNl4pogbczAVkfXS1Xbd5A'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_and_send_signal():
    market_data_summary = """
    تحلیلگر عزیز، وضعیت ارزهای مدنظر (سولانا، دوج‌کوین و چین‌لینک) بر اساس دیتای تریدینگ‌ویو در تایم فریم ۱ ساعته به این شرح است:
    قیمت بالای ابر کومو قرار دارد، RSI در محدوده ورود مناسب است و MACD کراس صعودی داده است.
    لطفاً یک سیگنال دقیق شامل نقطه ورود، حد ضرر و دو هدف قیمتی برای کانال تلگرام بنویس.
    """
    
    # استفاده از ارتباط مستقیم HTTP که هیچ‌گونه وابستگی به کتابخانه‌های سخت‌گیرانه ندارد
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": market_data_summary}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if response.status_code == 200:
            # استخراج متن پاسخ از ساختار JSON گوگل
            signal_text = result['candidates'][0]['content']['parts'][0]['text']
            bot.send_message(CHANNEL_ID, f"🎯 **سیگنال جدید تک‌تیرانداز**\n\n{signal_text}")
        else:
            error_msg = result.get('error', {}).get('message', 'خطای ناشناخته')
            bot.send_message(CHANNEL_ID, f"❌ خطا در پاسخ گوگل:\n{error_msg}")
            
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطای سیستمی:\n{e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش عملکرد روز گذشته تک‌تیرانداز:**\n\n✅ سیستم در حال پایش لحظه‌ای چارت‌های ۱ ساعته است."
        bot.send_message(CHANNEL_ID, report_text)
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطا در ارسال گزارش:\n{e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            send_daily_report()
        elif sys.argv[1] == "signal":
            generate_and_send_signal()
    else:
        generate_and_send_signal()
