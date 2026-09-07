import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "No JSON payload 
received"}), 400

    action = data.get("action", "LONG").upper()
    symbol = data.get("symbol", "MNQ1!")
    price_str = data.get("price", "0.0")
    
    try:
        entry_price = float(price_str)
    except ValueError:
        entry_price = 0.0

    if action == "LONG" or action == "BUY":
        direction_text = "LONG"
        tp1 = entry_price + 60.0
        tp2 = entry_price + 150.0
        sl = entry_price - 40.0
        confidence = "85%"
    else:
        direction_text = "SHORT"
        tp1 = entry_price - 60.0
        tp2 = entry_price - 150.0
        sl = entry_price + 40.0
        confidence = "85%"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")

    formatted_message = (
        f"Canary          admin\n"
        f"🟢 **FUTURES SIGNAL** 🟢\n\n"
        f"**Symbol:** {symbol}\n"
        f"**Direction:** {direction_text}\n"
        f"**Setup:** ICT Confluence\n"
        f"**Confidence:** {confidence}\n\n"
        f"📍 **Entry:** {entry_price:.1f}\n"
        f"🎯 **TP1:** {tp1:.1f}\n"
        f"🎯 **TP2:** {tp2:.1f}\n"
        f"🛡️ **SL:** {sl:.1f}\n\n"
        f"⏰ **Time (EST):**\n"
        f"{current_time}\n\n"
        f"⚠️ **Risk Management:**\n"
        f"• Risk 1-2% per trade\n"
        f"• Move SL to breakeven after TP1\n"
        f"• Partial close at TP1, hold remainder for TP2"
    )
    
    send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "No JSON payload 
received"}), 400

    action = data.get("action", "LONG").upper()
    symbol = data.get("symbol", "MNQ1!")
    price_str = data.get("price", "0.0")
    
    try:
        entry_price = float(price_str)
    except ValueError:
        entry_price = 0.0

    if action == "LONG" or action == "BUY":
        direction_text = "LONG"
        tp1 = entry_price + 60.0
        tp2 = entry_price + 150.0
        sl = entry_price - 40.0
        confidence = "85%"
    else:
        direction_text = "SHORT"
        tp1 = entry_price - 60.0
        tp2 = entry_price - 150.0
        sl = entry_price + 40.0
        confidence = "85%"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")

    formatted_message = (
        f"Canary          admin\n"
        f"🟢 **FUTURES SIGNAL** 🟢\n\n"
        f"**Symbol:** {symbol}\n"
        f"**Direction:** {direction_text}\n"
        f"**Setup:** ICT Confluence\n"
        f"**Confidence:** {confidence}\n\n"
        f"📍 **Entry:** {entry_price:.1f}\n"
        f"🎯 **TP1:** {tp1:.1f}\n"
        f"🎯 **TP2:** {tp2:.1f}\n"
        f"🛡️ **SL:** {sl:.1f}\n\n"
        f"⏰ **Time (EST):**\n"
        f"{current_time}\n\n"
        f"⚠️ **Risk Management:**\n"
        f"• Risk 1-2% per trade\n"
        f"• Move SL to breakeven after TP1\n"
        f"• Partial close at TP1, hold remainder for TP2"
    )
    
    send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
