# DAO Treasury Monitor Telegram Bot

This bot monitors Ethereum DAO treasury addresses and forwards activity notifications to Telegram using Alchemy webhooks.

## Telegram Bot Setup

1. **Create a Telegram Bot**:
   - Message @BotFather on Telegram
   - Send `/newbot` command
   - Follow prompts to name your bot and get:
     - `TELEGRAM_BOT_TOKEN` (API key)
     - Bot username (ends with _bot)

2. **Get Chat ID**:
   - Start a chat with your new bot
   - Visit this URL in browser (replace with your token):
     ```
     https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates
     ```
   - Look for `"chat":{"id":123456789}` in the JSON response
   - This is your `TELEGRAM_CHAT_ID`

## Alchemy Webhook Setup

1. Go to Alchemy Dashboard:
   ```
   https://dashboard.alchemy.com/webhooks
   ```

2. Create new webhook:
   - Select "Ethereum" network
   - Choose "Address Activity" type
   - Add the DAO addresses to monitor
   - Set webhook URL to your Replit URL:
     ```
     https://your-repl-url.webhook
     ```
   - (Optional) Set webhook secret

3. Configure notifications:
   - Select only token transfers
   - Filter for assets: ETH, WETH, wstETH, cbBTC

## Monitoring Addresses

The bot monitors these DAO treasury addresses:
- 3 Beras Capital: 0xdda04ab22bd06ef490621eace04219798dd71bfd
- Alameda Research V2: 0x767e095f6549050b4e9a3bcce18aadd28bef486f
- AicroStrategy: 0xddc23d34ea2f6920d15995607d00def9478ded6d
- DR3AM FUND: 0xb8745dec73f81ea366d7cc672438053c0e97de51

## Monitored Assets
- ETH
- WETH
- wstETH
- cbBTC

## Replit Deployment

1. Create a new Python Repl on Replit.com
2. Upload these files:
   - main.py (main application)
   - keep_alive.py (keep-alive server)

3. Set up environment variables in Replit:
   - Click on the "Secrets" tab (lock icon)
   - Add these required secrets:
     * TELEGRAM_BOT_TOKEN - Your Telegram bot token
     * TELEGRAM_CHAT_ID - Your Telegram chat ID
   - Optional secret:
     * WEBHOOK_SECRET - For webhook verification

4. Required Packages:
   - The .replit file automatically installs:
     * flask
     * requests
     * python-dotenv
     * waitress

5. Run the Repl:
   - The application will start automatically
   - Access it via the Replit-provided URL
   - The server runs on port 8080

6. Configure Alchemy webhook to send POST requests to:
   `https://your-repl-url.webhook`
