
import requests
import json
from datetime import datetime
import pandas as pd
import os

def fetch_binance_p2p_price():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "asset": "USDT",
        "fiat": "AED",
        "merchantCheck": False,
        "page": 1,
        "rows": 5,
        "tradeType": "SELL"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    prices = []
    for item in data.get("data", []):
        price = float(item["adv"]["price"])
        prices.append(price)

    if not prices:
        return None, None

    avg_price = sum(prices) / len(prices)
    spot = 3.6725
    premium = (avg_price - spot) / spot
    return avg_price, premium

# Prepare CSV path
output_file = "uae_ndf_p2p_history.csv"

# Fetch today's price and premium
price, premium = fetch_binance_p2p_price()

if price is not None:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    new_row = pd.DataFrame([{
        "date": today,
        "usdt_aed_avg": price,
        "ndf_premium_p2p": premium
    }])

    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.drop_duplicates(subset=["date"], keep="last", inplace=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Data saved for {today}: price={price}, premium={premium:.6f}")
else:
    print("⚠️ Failed to fetch data from Binance P2P")
