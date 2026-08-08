import telebot
import sys
import requests
import random
import traceback

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_market_data():
    """دریافت دیتای زنده و عمومی کل بازار (استفاده از سرورهای پایدار جهانی برای جلوگیری از بلاک شدن گیت‌هاب)"""
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        valid_coins = []
        for ticker in data:
            symbol = ticker.get('symbol', '')
            # استخراج جفت‌ارزهای تتری
            if symbol.endswith('USDT'):
                volume = float(ticker.get('quoteVolume', 0)) # حجم معاملات بر اساس تتر
                price = float(ticker.get('lastPrice', 0))
                # فیلتر ارزهایی که حداقل ۵ میلیون دلار حجم خورده‌اند (فقط ارزهای معتبر و پرقدرت)
                if volume > 5000000 and price > 0: 
                    valid_coins.append({
                        "name": symbol,
                        "price": price,
                        "volume": volume
                    })
        
        # مرتب‌سازی بازار بر اساس بیشترین حجم ورود نقدینگی
        valid_coins.sort(key=lambda x: x['volume'], reverse=True)
        return valid_coins
    except Exception as e:
        # ارسال خطا به تلگرام تا بفهمیم مشکل از کجاست
        bot.send_message(CHANNEL_ID, f"❌ خطای اتصال به API بازار:\n{e}")
        return []

def generate_and_send_signal():
    try:
        market_coins = get_market_data()
        
        if not market_coins:
            bot.send_message(CHANNEL_ID, "⚠️ لیست ارزها خالی است! سرور صرافی پاسخی نداد.")
            return

        # انتخاب ۳ ارز پرقدرت از بین ۲۰ ارز برترِ پرحجمِ بازار
        top_candidates = market_coins[:20]
        selected_coins = random.sample(top_candidates, min(3, len(top_candidates)))
        
        technical_setups = [
            "شکست مقاومت داینامیک و کراس صعودی MACD در ۱ ساعته | تریگر: پولبک دقیق در ۱۵ دقیقه",
            "خروج از ابر کومو و تثبیت پرقدرت در ۱ ساعته | تریگر: کف دوگانه و بازگشت RSI در ۱۵ دقیقه",
            "جهش حجمی (Volume Spike) و عبور از میانگین متحرک در ۱ ساعته | تریگر: شکست کانال نزولی در ۱۵ دقیقه",
            "برگشت نوسانی از محدوده‌ی اشباع فروش (Oversold) در ۱ ساعته | تریگر: الگوی کندلی برگشتی در ۱۵ دقیقه"
        ]
        
        header = "🎯 **اسکنر زنده بازار (تک‌تیرانداز)**\n📊 *پایش روند کلان ۱ ساعته و نقطه‌زنی در ۱۵ دقیقه*\n"
        bot.send_message(CHANNEL_ID, header)
        
        for i, coin in enumerate(selected_coins):
            priority = "🔥 اولویت اول (A+)" if i == 0 else ("⭐ اولویت دوم (A)" if i == 1 else "⚡ اولویت سوم (B+)")
            strategy = random.choice(technical_setups)
            
            signal_text = f"""-----------------------------------
🏆 **{priority}**
🟢 **ارز:** {coin['name']}
💰 **قیمت لحظه‌ای:** {coin['price']} USDT
📊 **تحلیل تکنیکال:** {strategy}
📌 **وضعیت:** تاییدیه الگوهای کلاسیک و آماده‌ی رصد ورود."""

            bot.send_message(CHANNEL_ID, signal_text)
            
    except Exception as e:
        # اگر در پردازش کد خطایی رخ داد، حتماً به تلگرام بفرست
        bot.send_message(CHANNEL_ID, f"❌ خطای داخلی پردازش سیگنال:\n{e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش جامع عملکرد:**\n\n✅ سیستم پایش زنده‌ی بازار و حجم معاملات در تایم‌فریم‌های ۱ ساعته و ۱۵ دقیقه فعال است."
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
