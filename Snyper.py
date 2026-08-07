import telebot
import google.generativeai as genai
import sys

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
GEMINI_API_KEY = 'AQ.Ab8RN6L_lvnaOD7jf6O3e9vgew7z6Bigg4oYE7LZGLgEszWttA'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def generate_and_send_signal():
    market_data_summary = """
    تحلیلگر عزیز، وضعیت ارزهای مدنظر (سولانا، دوج‌کوین و چین‌لینک) بر اساس دیتای پلتفرم تریدینگ‌ویو (TradingView) به این شرح است:
    تایم فریم ۱ ساعته: قیمت بالای ابر کومو قرار دارد، RSI در محدوده ورود مناسبی است و مکدی (MACD) کراس صعودی داده است. همچنین ساختار چارت شبیه به یک الگوی پرچم صعودی است.
    لطفاً بر اساس این داده‌ها، یک سیگنال دقیق شامل نقطه ورود، حد ضرر و دو هدف قیمتی برای کانال تلگرام بنویس.
    در انتهای تحلیل، فقط نقطه ورود، تی‌پی ۱ و استاپ رو به صورت اعدادِ خالص تو سه خط جداگانه بنویس.
    """
    try:
        response = model.generate_content(market_data_summary)
        bot.send_message(CHANNEL_ID, f"🎯 **سیگنال جدید تک‌تیرانداز**\n\n{response.text}")
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطا در تولید سیگنال:\n{e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش عملکرد روز گذشته تک‌تیرانداز:**\n\n✅ سیستم در حال آماده‌سازی برای پایش لحظه‌ای و ثبت نتایج سیگنال‌های TradingView است."
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
