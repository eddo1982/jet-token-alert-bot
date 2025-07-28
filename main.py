import requests
import time
import os
from telegram import Bot

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
bot = Bot(token=bot_token)

seen_pairs = set()

while True:
    try:
        response = requests.get("https://api.dexscreener.com/latest/dex/pairs/abstract")
        data = response.json()

        for pair in data["pairs"]:
            pair_address = pair["pairAddress"]
            if pair_address not in seen_pairs:
                seen_pairs.add(pair_address)

                # Filter
                volume_usd = float(pair.get("volume", {}).get("h24", 0))
                market_cap = float(pair.get("fdv", 0))
                liquidity = float(pair.get("liquidity", {}).get("usd", 0))
                if market_cap <= 100000 and liquidity / market_cap >= 0.05 and volume_usd > 1000:

                    name = pair.get("baseToken", {}).get("name", "Unknown")
                    symbol = pair.get("baseToken", {}).get("symbol", "")
                    link = pair.get("url", "")

                    message = f"🆕 *New Token Detected!*\n\n🪙 *{name}* ({symbol})\n💰 Volume: ${int(volume_usd):,}\n💎 MC: ${int(market_cap):,}\n💧 Liquidity: ${int(liquidity):,}\n🔗 [View on Dexscreener]({link})"

                    bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
