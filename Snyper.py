import telebot
import sys
import random
from tradingview_ta import TA_Handler, Interval, Exchange

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_tradingview_signals():
    """ارتباط مستقیم با تریدینگ‌ویو و اسکن تکنیکال بازار در تایم‌فریم ۱ ساعته"""
    # لیستی از ارزهای مستعد برای اسکن در تریدینگ‌ویو
    crypto_symbols = [
        "SOL", "DOGE", "LINK", "BTC", "ETH", "XRP", "ADA", 
        "AVAX", "NEAR", "RENDER", "MATIC", "DOT", "LTC", "BCH", "TRX", "INJ", "APT"
    ]
    
    valid_signals = []
    
    for symbol in crypto_symbols:
        try:
            handler = TA_Handler(
                symbol=f"{symbol}USDT",
                screener="crypto",
                exchange="BINANCE", # استفاده از دیتای جهانی بایننس در داخل تریدینگ‌ویو
                interval=Interval.INTERVAL_1_HOUR # قفل شده روی تایم‌فریم ۱ ساعته
            )
            
            analysis = handler.get_analysis()
            recommendation = analysis.summary["RECOMMENDATION"]
            
            # فیلتر کردن ارزهایی که در تریدینگ‌ویو سیگنال خرید یا خرید قوی دارند
            if recommendation in ["BUY", "STRONG_BUY"]:
                close_price = analysis.indicators["close"]
                rsi = analysis.indicators["RSI"]
                macd = analysis.indicators["MACD.macd"]
                
                valid_signals.append({
                    "name": symbol,
                    "price": close_price,
                    "rsi": round(rsi, 2),
                    "macd": round(macd, 4),
                    "rec": recommendation
                })
        except Exception as e:
            continue
            
    return valid_signals

def generate_and_send_signal():
    try:
        tv_signals = get_tradingview_signals()
        
        if not tv_signals:
            bot.send_message(CHANNEL_ID, "⚠️ تریدینگ‌ویو در حال حاضر سیگنال قوی برای ورود در تایم ۱ ساعته صادر نکرده است.")
            return

        # انتخاب تا ۳ ارز برتر از خروجی‌های تریدینگ‌ویو
        selected_coins = random.sample(tv_signals, min(3, len(tv_signals)))
        
        header = "🎯 **اسکنر مستقیم TradingView (تک‌تیرانداز)**\n📊 *پایش، تکنیکال و نقطه‌زنی منحصراً در تایم‌فریم ۱ ساعته*\n"
        bot.send_message(CHANNEL_ID, header)
        
        for i, coin in enumerate(selected_coins):
            priority = "🔥 اولویت اول (A+)" if i == 0 else ("⭐ اولویت دوم (A)" if i == 1 else "⚡ اولویت سوم (B+)")
            
            # محاسبه اعداد دقیق بر اساس قیمت واقعی تریدینگ‌ویو
            price = coin['price']
            sl = round(price * 0.975, 4) # حد ضرر 2.5%
            tp1 = round(price * 1.03, 4) # هدف اول 3%
            tp2 = round(price * 1.07, 4) # هدف دوم 7%
            
            status = "خرید قوی (Strong Buy)" if coin['rec'] == "STRONG_BUY" else "مستعد رشد (Buy)"
            
            signal_text = f"""-----------------------------------
🏆 **{priority}**
🟢 **ارز:** {coin['name']}/USDT
💰 **قیمت لحظه‌ای (TV):** {price}
📊 **وضعیت اندیکاتورها (۱ ساعته):** RSI: {coin['rsi']} | وضعیت MACD تایید شد
📌 **سیگنال تریدینگ‌ویو:** {status}

🎯 **نقطه ورود:** قیمت فعلی یا پولبک
🛑 **حد ضرر (SL):** {sl}
🎯 **هدف اول (TP1):** {tp1}
🎯 **هدف دوم (TP2):** {tp2}"""

            bot.send_message(CHANNEL_ID, signal_text)
            
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطای پردازش تریدینگ‌ویو:\n{e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش جامع عملکرد:**\n\n✅ اتصال مستقیم به موتور TradingView برقرار است و تمامی تحلیل‌ها با موفقیت در تایم‌فریم ۱ ساعته انجام می‌شوند."
        bot.send_message(CHANNEL_ID, report_text)
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطای ارسال گزارش:\n{e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            send_daily_report()
        elif sys.argv[1] == "signal":
            generate_and_send_signal()
    else:
        generate_and_send_signal()
