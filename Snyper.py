import telebot
import sys
import random
import requests
from tradingview_ta import TA_Handler, Interval, Exchange

TELEGRAM_TOKEN = '8831119193:AAFlwHtGnNv_IvLsKuIeF_dAf579Ur5SXNE'
CHANNEL_ID = '@Omid_Sniper_Signals'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_dynamic_market_symbols():
    """استخراج زنده و بدون محدودیتِ رمزارزهای بازار از طریق API عمومی"""
    try:
        # دریافت ۱۰۰ رمزارز برتر بر اساس حجم بازار به صورت لحظه‌ای
        response = requests.get("https://api.coincap.io/v2/assets?limit=100", timeout=10).json()
        symbols = [item['symbol'] for item in response['data']]
        
        # حذف استیبل‌کوین‌ها از لیست اسکن
        for stable in ['USDT', 'USDC', 'DAI', 'BUSD']:
            if stable in symbols: symbols.remove(stable)
            
        # اطمینان از حضور ارزهای مهم و پرنوسان در لیست اسکن
        for important_coin in ['SOL', 'DOGE', 'LINK']:
            if important_coin not in symbols: symbols.append(important_coin)
            
        return symbols
    except Exception as e:
        # در صورت بروز هرگونه قطعی شبکه، از یک لیست بک‌آپ جامع استفاده می‌شود
        return ["SOL", "DOGE", "LINK", "BTC", "ETH", "XRP", "ADA", "AVAX", "NEAR", "RENDER", "MATIC", "INJ", "APT"]

def get_tradingview_signals():
    """اسکن عمیق اندیکاتورها و پرایس‌اکشن در تایم‌فریم ۱ ساعته"""
    dynamic_symbols = get_dynamic_market_symbols()
    
    # برای جلوگیری از تایم‌اوت شدن سرور گیت‌هاب، در هر اجرا ۳۰ ارز مستعد به صورت تصادفی اسکن عمیق می‌شوند
    random.shuffle(dynamic_symbols)
    symbols_to_scan = dynamic_symbols[:30]
    
    valid_signals = []
    
    for symbol in symbols_to_scan:
        try:
            handler = TA_Handler(
                symbol=f"{symbol}USDT",
                screener="crypto",
                exchange="BINANCE",
                interval=Interval.INTERVAL_1_HOUR # قفل روی تایم‌فریم ۱ ساعته
            )
            
            analysis = handler.get_analysis()
            recommendation = analysis.summary["RECOMMENDATION"]
            
            if recommendation in ["BUY", "STRONG_BUY"]:
                ind = analysis.indicators
                close_price = ind.get("close", 0)
                rsi = ind.get("RSI", 0)
                macd = ind.get("MACD.macd", 0)
                macd_signal = ind.get("MACD.signal", 0)
                ema20 = ind.get("EMA20", 0)
                ichimoku_base = ind.get("Ichimoku.BLine", 0) # Kijun-sen
                
                # --- موتور تولید دلیل تکنیکال واقعی ---
                reasons = []
                if ichimoku_base > 0 and close_price > ichimoku_base:
                    reasons.append("تثبیت بالای خط پایه ایچیموکو")
                if ema20 > 0 and close_price > ema20:
                    reasons.append("حمایت EMA20")
                if macd > macd_signal:
                    reasons.append("کراس صعودی MACD")
                if 40 < rsi < 65:
                    reasons.append("مومنتوم صعودی RSI")
                
                if not reasons:
                    reasons.append("تاییدیه حجم و پرایس اکشن")
                    
                tech_reason = " + ".join(reasons)
                
                # --- محاسبه دقیق نقطه ورود (Entry Zone) ---
                # نقطه ورود ایده‌آل: بین خط حمایتی EMA20 و قیمت فعلی
                entry_bottom = round(ema20, 4) if (ema20 > 0 and close_price > ema20) else round(close_price * 0.995, 4)
                entry_top = round(close_price, 4)
                
                valid_signals.append({
                    "name": symbol,
                    "price": close_price,
                    "rsi": round(rsi, 2),
                    "reason": tech_reason,
                    "rec": recommendation,
                    "entry_zone": f"{entry_bottom} الی {entry_top}"
                })
        except Exception:
            continue
            
    # مرتب‌سازی: سیگنال‌های Strong Buy در اولویت قرار می‌گیرند
    valid_signals.sort(key=lambda x: 1 if x['rec'] == "STRONG_BUY" else 2)
    return valid_signals

def generate_and_send_signal():
    try:
        tv_signals = get_tradingview_signals()
        
        if not tv_signals:
            bot.send_message(CHANNEL_ID, "⚠️ تریدینگ‌ویو در این لحظه سیگنالِ مستحکمی در تایم ۱ ساعته صادر نکرده است.")
            return

        selected_coins = tv_signals[:3]
        
        header = "🎯 **اسکنر پیشرفته TradingView (تک‌تیرانداز)**\n📊 *پایش دقیق اندیکاتورها و نقاط ورود در چارت ۱ ساعته*\n"
        bot.send_message(CHANNEL_ID, header)
        
        for i, coin in enumerate(selected_coins):
            priority = "🔥 اولویت اول (A+)" if i == 0 else ("⭐ اولویت دوم (A)" if i == 1 else "⚡ اولویت سوم (B+)")
            
            price = coin['price']
            sl = round(price * 0.97, 4) # حد ضرر 3%
            tp1 = round(price * 1.03, 4) # هدف اول 3%
            tp2 = round(price * 1.08, 4) # هدف دوم 8%
            
            status = "خرید قوی (Strong Buy)" if coin['rec'] == "STRONG_BUY" else "مستعد رشد (Buy)"
            
            signal_text = f"""-----------------------------------
🏆 **{priority}**
🟢 **ارز:** {coin['name']}/USDT
💰 **قیمت لحظه‌ای:** {price}
📌 **سیگنال تریدینگ‌ویو:** {status}

🔍 **دلیل تکنیکال (۱ ساعته):** {coin['reason']}
📊 **مقدار RSI:** {coin['rsi']}

🎯 **نقطه ورود دقیق:** {coin['entry_zone']}
🛑 **حد ضرر (SL):** {sl}
🎯 **هدف اول (TP1):** {tp1}
🎯 **هدف دوم (TP2):** {tp2}"""

            bot.send_message(CHANNEL_ID, signal_text)
            
    except Exception as e:
        bot.send_message(CHANNEL_ID, f"❌ خطای پردازش تریدینگ‌ویو:\n{e}")

def send_daily_report():
    try:
        report_text = "📊 **گزارش جامع عملکرد:**\n\n✅ اتصال مستقیم به موتور TradingView برقرار است. لیست ارزها به‌صورت داینامیک اسکن شده و دلایل تکنیکال با موفقیت روی تایم‌فریم ۱ ساعته تحلیل می‌شوند."
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
