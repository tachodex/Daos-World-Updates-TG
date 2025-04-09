import os
from flask import Flask, request, jsonify
import requests
from threading import Thread
from keep_alive import keep_alive

app = Flask(__name__)

# Configuration - uses Replit secrets
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '')  # Optional

# DAO addresses to monitor (normalized to lowercase)
DAO_ADDRESSES = {
    '0xdda04ab22bd06ef490621eace04219798dd71bfd': '3 Beras Capital',
    '0x767e095f6549050b4e9a3bcce18aadd28bef486f': 'Alameda Research V2',
    '0xddc23d34ea2f6920d15995607d00def9478ded6d': 'AicroStrategy',
    '0xb8745dec73f81ea366d7cc672438053c0e97de51': 'DR3AM FUND'
}

# Assets to monitor (case insensitive)
MONITORED_ASSETS = {'ETH', 'WETH', 'wstETH', 'cbBTC'}

def send_telegram_message(message):
    """Send message to Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    return response.json()

def format_activity_message(dao_name, activity):
    """Format activity message for Telegram"""
    asset = activity['asset']
    value = activity.get('value', 'N/A')
    direction = 'OUT' if activity['toAddress'].lower() in DAO_ADDRESSES else 'IN'
    tx_hash = activity['hash']
    
    return (
        f"🚨 <b>{dao_name} Activity</b> 🚨\n"
        f"• Asset: {asset}\n"
        f"• Amount: {value}\n" 
        f"• Direction: {direction}\n"
        f"• Tx Hash: <code>{tx_hash}</code>\n"
        f"• Explorer: https://etherscan.io/tx/{tx_hash}"
    )

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Optional webhook secret verification
    if WEBHOOK_SECRET:
        if request.headers.get('X-Webhook-Secret') != WEBHOOK_SECRET:
            return jsonify({'status': 'error', 'message': 'Invalid secret'}), 401
    
    data = request.json
    
    # Handle test notifications
    if data.get('type') == 'TEST':
        send_telegram_message("✅ <b>Test notification received</b> ✅")
        return jsonify({'status': 'success'})
    
    # Process address activity
    if data.get('type') == 'ADDRESS_ACTIVITY':
        for activity in data['event']['activity']:
            # Check if activity involves our DAO addresses
            from_address = activity['fromAddress'].lower()
            to_address = activity['toAddress'].lower()
            
            # Find which DAO is involved
            dao_address = from_address if from_address in DAO_ADDRESSES else to_address
            if dao_address in DAO_ADDRESSES and activity['asset'].upper() in MONITORED_ASSETS:
                dao_name = DAO_ADDRESSES[dao_address]
                message = format_activity_message(dao_name, activity)
                send_telegram_message(message)
    
    return jsonify({'status': 'success'})

# Start keep-alive server in a separate thread
keep_alive()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
