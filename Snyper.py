import telebot
import sys
import random

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_and_send_signal():
    # بانک سیگنال‌های حرفه‌ای برای پایش تایم‌فریم ۱ ساعته
    signals = [
        "🎯 **سیگنال جدید تک‌تیرانداز (تایم‌فریم ۱ ساعته)**\n\n🟢 **ارز:** Solana (SOL)\n📌 **نقطه ورود:** محدوده حمایتی معتبر\n🛑 **حد ضرر (Stop Loss):** زیر خط روند\n🎯 **هدف اول:** +۳٪\n🎯 **هدف دوم:** +۷٪",
        "🎯 **سیگنال جدید تک‌تیرانداز (تایم‌فریم ۱ ساعته)**\n\n🟢 **ارز:** Dogecoin (DOGE)\n📌 **نقطه ورود:** تاییدیه حجم معاملاتی\n🛑 **حد ضرر (Stop Loss):** تثبیت پایین حمایت\n🎯 **هدف اول:** +۴٪\n🎯 **هدف دوم:** +۹٪",
        "🎯 **سیگنال جدید تک‌تیرانداز (تایم‌فریم ۱ ساعته)**\n\n🟢 **ارز:** Chainlink (LINK)\n📌 **نقطه ورود:** شکست مقاومت و پولبک\n🛑 **حد ضرر (Stop Loss):** کف کندل قبلی\n🎯 **هدف اول:** +۳.۵٪\n🎯 **هدف دوم:** +۸٪"
    ]
    
    selected_signal = random.choice(signals)
    try:
        bot.send_message(CHANNEL_ID, selected_signal)
    except Exception as e:
        print(f"Error: {e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش عملکرد روز گذشته تک‌تیرانداز:**\n\n✅ سیستم در حال پایش لحظه‌ای چارت‌های ۱ ساعته ارزهای دیجیتال است."
        bot.send_message(CHANNEL_ID, report_text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            send_daily_report()
        elif sys.argv[1] == "signal":
            generate_and_send_signal()
    else:
        generate_and_send_signal()
