import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    print("Webhook received successfully!")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    action = data.get("action", "ALERT")
    symbol = data.get("symbol", "UNKNOWN")
    price = data.get("price", "N/A")

    text = f"🚨 Signal 🚨\nAction: {action}\nSymbol: {symbol}\nPrice: {price}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        res = requests.post(url, json=payload, timeout=3)
        print(f"Telegram response: {res.status_code} {res.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
