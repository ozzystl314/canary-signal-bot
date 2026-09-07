from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
import pytz

app = Flask(__name__)

TELEGRAM_TOKEN = "8929353444:AAGauKvtR9RrEQCkaVMQz9tA3QCtUU3cggQ"
CHAT_ID = "-1002361104032"
THREAD_ID = 489
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def format_signal(data: dict) -> str:
    direction = data.get("direction", "LONG")
    emoji = "🟢" if direction == "LONG" else "🔴"
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S EST')
    
    return f"""{emoji} *FUTURES SIGNAL* {emoji}

*Symbol:* `{data.get('symbol', 'N/A')}`
*Direction:* {direction}
*Setup:* {data.get('setup', 'ICT Confluence')}
*Confidence:* {data.get('confidence', '0')}%

📍 *Entry:* `{data.get('entry', 'N/A')}`
🎯 *TP1:* `{data.get('tp1', 'N/A')}`
🎯 *TP2:* `{data.get('tp2', 'N/A')}`
🛡 *SL:* `{data.get('sl', 'N/A')}`

⏰ *Time (EST):* {est_time}

⚠️ *Risk Management:*
• Risk 1-2% per trade
• Move SL to breakeven after TP1
• Partial close at TP1, hold remainder for TP2"""

def send_telegram(message: str):
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(TELEGRAM_API, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print(f"📩 Received: {data}")

        required = ['symbol', 'direction', 'entry', 'sl', 'tp1', 'tp2']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        confidence = float(data.get('confidence', 0))
        if confidence < 75:
            return jsonify({"status": "ignored", "reason": f"Confidence {confidence}% too low"}), 200

        message = format_signal(data)
        result = send_telegram(message)

        if result and result.get("ok"):
            return jsonify({"status": "sent"}), 200
        else:
            return jsonify({"error": "Telegram API failed", "details": result}), 500

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "✅ Signal bot is running", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
