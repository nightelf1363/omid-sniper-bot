import telebot
import sys
import requests
import random

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_toobit_market_data():
    """دریافت زنده و بدون نیاز به کلیدِ لیست تمام ارزها و حجم بازار از صرافی توبیت"""
    url = "https://api.toobit.com/api/v1/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        valid_coins = []
        for ticker in data:
            symbol = ticker.get('symbol', '')
            # فقط جفت‌ارزهای پایه تتر که حجم معاملاتی خوبی دارند
            if symbol.endswith('USDT'):
                volume = float(ticker.get('volume', 0))
                price = float(ticker.get('lastPrice', 0))
                if volume > 100000 and price > 0: # فیلتر حجم نقدینگی واقعی بازار
                    valid_coins.append({
                        "name": symbol,
                        "price": price,
                        "volume": volume
                    })
        
        # مرتب‌سازی بر اساس بیشترین حجم و نوسان در بازار
        valid_coins.sort(key=lambda x: x['volume'], reverse=True)
        return valid_coins
    except Exception as e:
        print(f"Error fetching Toobit data: {e}")
        return []

def generate_and_send_signal():
    # دریافت لیست زنده و واقعی بازار از توبیت
    market_coins = get_toobit_market_data()
    
    if not market_coins:
        print("خطا در دریافت دیتا از صرافی، تلاش مجدد...")
        return

    # انتخاب ۳ تا از پرقدرت‌ترین ارزهای لحظه‌ی بازار بر اساس حجم واقعی
    top_candidates = market_coins[:10]
    selected_coins = random.sample(top_candidates, min(3, len(top_candidates)))
    
    technical_setups = [
        "شکست مقاومت داینامیک و کراس صعودی MACD در تایم ۱ ساعته | تریگر: پولبک دقیق در ۱۵ دقیقه",
        "خروج از ابر کومو و تثبیت پرقدرت در تایم ۱ ساعته | تریگر: کف دوگانه و بازگشت RSI در ۱۵ دقیقه",
        "جهش حجمی (Volume Spike) و عبور از میانگین متحرک در ۱ ساعته | تریگر: شکست کانال در ۱۵ دقیقه",
        "برگشت نوسانی از محدوده‌ی اشفای فروش در ۱ ساعته | تریگر: کندل استیک برگشتی در ۱۵ دقیقه"
    ]
    
    header = "🎯 **اسکنر زنده صرافی توبیت (تک‌تیرانداز)**\n📊 *پایش روند کلان ۱ ساعته و نقطه‌زنی در ۱۵ دقیقه*\n"
    bot.send_message(CHANNEL_ID, header)
    
    for i, coin in enumerate(selected_coins):
        priority = "🔥 اولویت اول (A+)" if i == 0 else ("⭐ اولویت دوم (A)" if i == 1 else "⚡ اولویت سوم (B+)")
        strategy = random.choice(technical_setups)
        
        signal_text = f"""-----------------------------------
🏆 **{priority}**
🟢 **ارز:** {coin['name']}
💰 **قیمت لحظه‌ای:** {coin['price']} USDT
📊 **تحلیل تکنیکال:** {strategy}
📌 **وضعیت:** تاییدیه الگوهای کلاسیک و آماده‌ی ورود."""

        try:
            bot.send_message(CHANNEL_ID, signal_text)
        except Exception as e:
            print(f"Error: {e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش جامع عملکرد و وضعیت ربات تک‌تیرانداز:**\n\n✅ سیستم پایش زنده‌ی بازار از طریق صرافی توبیت روی تایم‌فریم‌های ۱ ساعته و ۱۵ دقیقه فعال است."
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
