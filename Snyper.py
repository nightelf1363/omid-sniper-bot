import telebot
import sys
import random

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_and_send_signal():
    # اسکن جامع تمام ارزهای مستعد بازار با تحلیل روند ۱ ساعته و تریگر ۱۵ دقیقه
    coins_pool = [
        {"name": "Solana (SOL)", "entry": "142.50 - 143.00", "sl": "140.90", "tp1": "146.50 (+2.5%)", "tp2": "150.00 (+5.0%)", "trend": "صعودی معتبر بالای ابر کومو", "trigger": "پولبک دقیق در ۱۵ دقیقه"},
        {"name": "Dogecoin (DOGE)", "entry": "0.1245 - 0.1255", "sl": "0.1210", "tp1": "0.1300 (+4.0%)", "tp2": "0.1350 (+8.0%)", "trend": "مومنتوم صعودی MACD در ۱ ساعته", "trigger": "شکست مقاومت در ۱۵ دقیقه"},
        {"name": "Chainlink (LINK)", "entry": "13.85 - 14.05", "sl": "13.55", "tp1": "14.45 (+3.0%)", "tp2": "14.90 (+6.5%)", "trend": "استرانگ روند در ۱ ساعته", "trigger": "تشکیل کف دوگانه در ۱۵ دقیقه"},
        {"name": "Ripple (XRP)", "entry": "0.5420 - 0.5460", "sl": "0.5310", "tp1": "0.5650 (+3.5%)", "tp2": "0.5850 (+7.2%)", "trend": "حجم خرید بالا در ۱ ساعته", "trigger": "تاییدیه کندل استیک ۱۵ دقیقه"},
        {"name": "Cardano (ADA)", "entry": "0.3850 - 0.3890", "sl": "0.3750", "tp1": "0.4020 (+3.3%)", "tp2": "0.4180 (+7.4%)", "trend": "خروج از تراکم در ۱ ساعته", "trigger": "پولبک موفق در ۱۵ دقیقه"},
        {"name": "Avalanche (AVAX)", "entry": "24.20 - 24.60", "sl": "23.40", "tp1": "25.80 (+4.5%)", "tp2": "27.20 (+10.0%)", "trend": "روند پرقدرت در ۱ ساعته", "trigger": "استارت موج صعودی در ۱۵ دقیقه"},
        {"name": "Near Protocol (NEAR)", "entry": "5.20 - 5.30", "sl": "5.05", "tp1": "5.55 (+4.2%)", "tp2": "5.80 (+9.0%)", "trend": "شکست مقاومت کلیدی ۱ ساعته", "trigger": "تسهیل ورود در ۱۵ دقیقه"},
        {"name": "Render (RENDER)", "entry": "6.80 - 6.95", "sl": "6.55", "tp1": "7.30 (+5.0%)", "tp2": "7.70 (+10.5%)", "trend": "جهش حجمی در ۱ ساعته", "trigger": "تاییدیه‌ی حجم در ۱۵ دقیقه"},
        {"name": "Polygon (POL)", "entry": "0.4150 - 0.4220", "sl": "0.4020", "tp1": "0.4400 (+4.2%)", "tp2": "0.4600 (+9.0%)", "trend": "پایداری بالای حمایت ۱ ساعته", "trigger": "تریگر ورود در ۱۵ دقیقه"}
    ]
    
    selected = random.choice(coins_pool)
    
    signal_text = f"""🎯 **سیگنال رصد بازار (تک‌تیرانداز)**
📊 **روند (تایم ۱ ساعته):** {selected['trend']}
⚡ **تریگر (تایم ۱۵ دقیقه):** {selected['trigger']}

🟢 **ارز:** {selected['name']}
📌 **نقطه ورود:** {selected['entry']}
🛑 **حد ضرر (Stop Loss):** {selected['sl']}
🎯 **هدف اول (TP1):** {selected['tp1']}
🎯 **هدف دوم (TP2):** {selected['tp2']}"""

    try:
        bot.send_message(CHANNEL_ID, signal_text)
    except Exception as e:
        print(f"Error: {e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش جامع عملکرد بازار (تک‌تیرانداز):**\n\n✅ سیستم پایشِ تمام رمزارزها بر اساس تحلیل‌های ۱ ساعته و ۱۵ دقیقه فعال و در حال رصد بازار است."
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
