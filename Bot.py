import time
import requests
import os
import websocket
import json
import threading
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv() 



# Configuration from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Validate required environment variables
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")
if not FINNHUB_API_KEY:
    raise ValueError("FINNHUB_API_KEY environment variable is required")

STOCK_LIST = [ "TSLA", "AAPL", "GOOGL", "AMZN", 
               "META", "NVDA", "NFLX", "INTC", 
                "ORCL", "CSCO", "SAP", "ADBE",
                "PYPL", "UBER", "LYFT", "SNAP", 
                "SHOP","SPOT", "ROKU", "IBM",
                "ABNB", "DASH", "JPM", "MSFT",]

CRYPTO_LIST = [ "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:XRPUSDT", "BINANCE:LTCUSDT", "BINANCE:BCHUSDT","BINANCE:BNBUSDT",  "BINANCE:DOGEUSDT", "BINANCE:SOLUSDT" ]
last_prices = {}          # Stores baseline prices for comparison
latest_prices = {}        # Stores the most recent prices
baseline_prices = {}      # Stores prices when alerts were last sent


def finnhub_on_message(ws, message):
    data = json.loads(message)
    if "data" in data:
        for update in data["data"]:
            symbol = update["s"]
            price = update["p"]
            check_and_alert(symbol, price)

def finnhub_on_open(ws):
    print("🔗 Connected to Finnhub")
    
    # Subscribe to stock symbols
    for symbol in STOCK_LIST:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))
    
    # Subscribe to crypto symbols
    for symbol in CRYPTO_LIST:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))
    
    print(f"📊 Subscribed to {len(STOCK_LIST)} stocks and {len(CRYPTO_LIST)} crypto pairs")

def run_finnhub_ws():
    ws = websocket.WebSocketApp(
        url=f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}",
        on_message=finnhub_on_message,
        on_open=finnhub_on_open,
    )
    ws.run_forever()



def check_and_alert(symbol, new_price, asset_type="STOCK"):
    asset_type = "Stock" if symbol in STOCK_LIST else "Crypto" if symbol in CRYPTO_LIST else "Asset"
    
    # Initialize baseline price if this is the first time seeing this symbol
    if symbol not in baseline_prices:
        baseline_prices[symbol] = new_price
        latest_prices[symbol] = new_price
        return
    
    # Calculate change from baseline (last alert point)
    baseline_price = baseline_prices[symbol]
    if baseline_price == 0:
        return
        
    change = ((new_price - baseline_price) / baseline_price) * 100
    
    # Send alert and update baseline if significant change detected
    
    # Different thresholds for stocks vs crypto
    if symbol in STOCK_LIST:
        # Stock threshold: ±1.0%
        if abs(change) >= 1.0:
            if change >= 1.0:
                send_discord_alert(f"📈 {asset_type} {symbol} up {change:.2f}% ({baseline_price:.2f} -> {new_price:.2f})")
            elif change <= -1.0:
                send_discord_alert(f"📉 {asset_type} {symbol} down {change:.2f}% ({baseline_price:.2f} -> {new_price:.2f})")
            baseline_prices[symbol] = new_price  # Reset baseline after alert
    
    elif symbol in CRYPTO_LIST:
        # Crypto threshold: ±0.5% (more sensitive due to volatility)
        if abs(change) >= 0.5:
            if change >= 0.5:
                send_discord_alert(f"📈 {asset_type} {symbol} up {change:.2f}% ({baseline_price:.2f} -> {new_price:.2f})")
            elif change <= -0.5:
                send_discord_alert(f"📉 {asset_type} {symbol} down {change:.2f}% ({baseline_price:.2f} -> {new_price:.2f})")
            baseline_prices[symbol] = new_price 

    
    # Always update the latest price for tracking
    latest_prices[symbol] = new_price

   

def send_discord_alert(message):
    try: 
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"Sent alert: {message}")
    except Exception as e:
        print(f"Error sending alert: {e}")


# --- Main loop ---
if __name__ == "__main__":
    threading.Thread(target=run_finnhub_ws, daemon = True).start()
    

    while True:
        time.sleep(1)
