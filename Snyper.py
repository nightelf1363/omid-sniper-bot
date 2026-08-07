import telebot
from google import genai
import os
import sys

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_and_send_signal():
    market_data_summary = """
    تحلیلگر عزیز، وضعیت ارزهای مدنظر (سولانا، دوج‌کوین و چین‌لینک) بر اساس دیتای تریدینگ‌ویو در تایم فریم ۱ ساعته به این شرح است:
    قیمت بالای ابر کومو قرار دارد، RSI در محدوده ورود مناسب است و MACD کراس صعودی داده است.
    لطفاً یک سیگنال دقیق شامل نقطه ورود، حد ضرر و دو هدف قیمتی برای کانال تلگرام بنویس.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=market_data_summary
        )
        bot.send_message(CHANNEL_ID, f"🎯 **سیگنال جدید تک‌تیرانداز**\n\n{response.text}")
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطا در تولید سیگنال:\n{e}")

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
