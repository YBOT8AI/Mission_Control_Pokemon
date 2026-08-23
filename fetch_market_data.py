#!/usr/bin/env python3
"""
fetch_market_data.py
Fetches LIVE market data (crypto, stocks, metals, commodities) + news headlines,
writes market.json for the Mission Control dashboard.

Run: python3 fetch_market_data.py
Output: /Users/ybot/Mission_Control_Pokemon/market.json

Data sources (all live, no training-data fallback):
- Crypto: CoinGecko (BTC, ETH, SOL)
- FX: exchangerate-api (USD→HKD)
- Metals: gold-api.com (XAU, XAG)
- Stocks/commodities: yfinance (VOO, ^GSPC, SPCX, CL=F, NG=F)
- News: BBC World RSS + Google News RSS (aggregated, deduped)
"""

import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
REPO_DIR = "/Users/ybot/Mission_Control_Pokemon"
OUT_FILE = os.path.join(REPO_DIR, "market.json")

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
FX_URL = "https://api.exchangerate-api.com/v4/latest/USD"
GOLD_URL = "https://api.gold-api.com/price/XAU"
SILVER_URL = "https://api.gold-api.com/price/XAG"

# News RSS feeds (wire services + aggregators)
RSS_FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("Google News Top", "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"),
    ("Google News HK", "https://news.google.com/rss?hl=en-HK&gl=HK&ceid=HK:en"),
]


def fetch_json(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {}


def fetch_rss(url, timeout=12):
    """Fetch and parse an RSS feed, return list of {title, link, source, time}."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode("utf-8", errors="ignore")
        root = ET.fromstring(data)
        items = []
        for item in root.iter("item"):
            title = link = pub = ""
            for child in item:
                tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if tag == "title":
                    title = (child.text or "").strip()
                elif tag == "link":
                    link = (child.text or "").strip()
                elif tag == "pubDate":
                    pub = (child.text or "").strip()
            if title:
                items.append({"title": title, "link": link, "pubDate": pub})
        return items
    except Exception:
        return []


def fetch_stock(symbol):
    try:
        import yfinance as yf
        t = yf.Ticker(symbol)
        fi = t.fast_info
        price = getattr(fi, "last_price", None)
        prev = getattr(fi, "regular_market_previous_close", None)
        chg = ((price - prev) / prev * 100) if price and prev and prev != 0 else None
        return {"price": price, "changePct": chg}
    except Exception:
        return None


def parse_rss_date(s):
    """Parse common RSS date formats to ISO."""
    if not s:
        return None
    from email.utils import parsedate_to_datetime
    try:
        return parsedate_to_datetime(s).astimezone(HKT).isoformat()
    except Exception:
        return None


def main():
    print("📈 Fetching live market data...")
    now = datetime.now(HKT).isoformat()

    # FX rate
    fx = fetch_json(FX_URL)
    hkd_rate = fx.get("rates", {}).get("HKD", 7.84)
    print(f"  💱 USD/HKD: {hkd_rate}")

    # Crypto
    crypto_raw = fetch_json(COINGECKO_URL)
    crypto = {}
    for name, cid in [("BTC", "bitcoin"), ("ETH", "ethereum"), ("SOL", "solana")]:
        c = crypto_raw.get(cid, {})
        usd = c.get("usd")
        chg = c.get("usd_24h_change")
        crypto[name] = {
            "priceHkd": round(usd * hkd_rate, 2) if usd else None,
            "changePct": round(chg, 2) if chg is not None else None,
        }
    print(f"  ₿ BTC: HK${crypto['BTC']['priceHkd']:,} ({crypto['BTC']['changePct']}%)")

    # Stocks
    stocks = {}
    for name, sym in [("VOO", "VOO"), ("SPX", "^GSPC"), ("SPCX", "SPCX")]:
        d = fetch_stock(sym)
        if d and d["price"]:
            stocks[name] = {
                "priceHkd": round(d["price"] * hkd_rate, 2),
                "changePct": round(d["changePct"], 2) if d["changePct"] is not None else None,
            }
        else:
            stocks[name] = {"priceHkd": None, "changePct": None}
    print(f"  📊 VOO: HK${stocks['VOO']['priceHkd']:,}")

    # Metals (gold-api returns USD per troy ounce)
    gold = fetch_json(GOLD_URL)
    silver = fetch_json(SILVER_URL)
    metals = {}
    # Gold price per gram in HKD: (USD/oz) / 31.1035 * HKD
    if gold.get("price"):
        gold_usd_oz = gold["price"]
        metals["Gold"] = {
            "priceHkdPerGram": round(gold_usd_oz / 31.1035 * hkd_rate, 2),
            "priceUsdOz": round(gold_usd_oz, 2),
        }
    else:
        metals["Gold"] = {"priceHkdPerGram": None, "priceUsdOz": None}
    if silver.get("price"):
        silver_usd_oz = silver["price"]
        metals["Silver"] = {
            "priceHkdPerGram": round(silver_usd_oz / 31.1035 * hkd_rate, 2),
            "priceUsdOz": round(silver_usd_oz, 2),
        }
    else:
        metals["Silver"] = {"priceHkdPerGram": None, "priceUsdOz": None}
    print(f"  🥇 Gold: HK${metals['Gold']['priceHkdPerGram']}/g")

    # Commodities
    commodities = {}
    for name, sym in [("Crude Oil", "CL=F"), ("Natural Gas", "NG=F")]:
        d = fetch_stock(sym)
        if d and d["price"]:
            commodities[name] = {
                "priceHkd": round(d["price"] * hkd_rate, 2),
                "changePct": round(d["changePct"], 2) if d["changePct"] is not None else None,
            }
        else:
            commodities[name] = {"priceHkd": None, "changePct": None}
    print(f"  🛢️ Crude: HK${commodities['Crude Oil']['priceHkd']}/bbl")

    # News
    print("  📰 Fetching news headlines...")
    news_items = []
    seen_titles = set()
    for source, url in RSS_FEEDS:
        items = fetch_rss(url)
        for it in items:
            title = it["title"]
            # Dedupe by normalized title
            key = title.lower()[:80]
            if key in seen_titles:
                continue
            seen_titles.add(key)
            news_items.append({
                "title": title,
                "link": it["link"],
                "source": source,
                "time": parse_rss_date(it["pubDate"]),
            })
    # Sort by time (newest first), keep top 20
    news_items.sort(key=lambda x: x["time"] or "", reverse=True)
    news_items = news_items[:20]
    print(f"  📰 {len(news_items)} headlines aggregated")

    # Assemble
    market = {
        "generatedAt": now,
        "fx": {"usdHkd": hkd_rate},
        "crypto": crypto,
        "stocks": stocks,
        "metals": metals,
        "commodities": commodities,
        "news": news_items,
    }

    with open(OUT_FILE, "w") as f:
        json.dump(market, f, indent=2, ensure_ascii=False)

    print(f"\n✅ market.json written ({os.path.getsize(OUT_FILE)} bytes)")
    print(f"   Path: {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
