import os
import logging
from flask import Flask, request, jsonify
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or CHAT_ID environment variables")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Telegram API error: {e}")
        raise

def format_signal(data: dict) -> str:
    direction = data.get("direction", "LONG")
    emoji = "🟢" if direction == "LONG" else "🔴"
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S EST')
    
    return f"""{emoji} *FUTURES SIGNAL* {emoji}

*Symbol:* `{data.get('symbol', 'N/A')}`
*Direction:* {direction}
*Setup:* {data.get('setup', 'ICT Confluence')}
*Confidence:* {data.get('confidence', 'N/A')}%

📍 *Entry:* `{data.get('entry', 'N/A')}`
🎯 *TP1:* `{data.get('tp1', 'N/A')}`
🎯 *TP2:* `{data.get('tp2', 'N/A')}`
🛡 *SL:* `{data.get('sl', 'N/A')}`

⏰ *Time (EST):* {est_time}

⚠️ *Risk Management:*
• Risk 1-2% per trade
• Move SL to breakeven after TP1
• Partial close at TP1, hold remainder for TP2"""

@app.route('/')
def home():
    return "Webhook server is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        logger.info(f"Received webhook: {data}")
        
        required = ['symbol', 'direction', 'entry', 'sl', 'tp1', 'tp2']
        missing = [k for k in required if k not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400
        
        confidence = float(data.get('confidence', 0))
        if confidence < 75:
            return jsonify({"status": "ignored", "reason": "confidence below threshold"}), 200
        
        message = format_signal(data)
        send_telegram_message(message)
        
        logger.info(f"Signal sent: {data.get('symbol')} {data.get('direction')}")
        return jsonify({"status": "sent"}), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
