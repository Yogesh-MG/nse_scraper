import aiohttp
import asyncio
from asgiref.sync import sync_to_async
import datetime
from nsepython import nse_optionchain_scrapper, nsesymbolpurify
from .models import OptionChain

SYMBOLS = ["BANKNIFTY", "NIFTY", "FINNIFTY", "MIDCPNIFTY"]
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

async def fetch_option_chain(symbol, session):
    symbol = nsesymbolpurify(symbol)
    loop = asyncio.get_event_loop()
    try:
        print(f"[{datetime.datetime.now()}] 📡 Fetching data for {symbol}")
        data = await loop.run_in_executor(None, nse_optionchain_scrapper, symbol)
        if not data or "records" not in data:
            print(f"[{datetime.datetime.now()}] ⚠️ Invalid or empty data for {symbol}: {data}")
            return symbol, None
        print(f"[{datetime.datetime.now()}] ✅ Fetched data for {symbol}")
        return symbol, data
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ❌ Fetch error for {symbol}: {e}")
        return symbol, None

async def store_data(symbol, data):
    """Store option chain in Django ORM"""
    if not data or "records" not in data:
        print(f"[{datetime.datetime.now()}] ⚠️ No valid data to store for {symbol}")
        return

    timestamp = datetime.datetime.now()
    record_count = 0

    try:
        for record in data["filtered"]["data"]:
            strikePrice = record.get("strikePrice")
            expiryDate = record.get("expiryDate")
            if not strikePrice or not expiryDate:
                print(f"[{datetime.datetime.now()}] ⚠️ Missing strikePrice or expiryDate for {symbol}: {record}")
                continue

            ce_data = record.get("CE", {})
            pe_data = record.get("PE", {})

            try:
                await sync_to_async(OptionChain.objects.create)(
                    timestamp=timestamp,
                    symbol=symbol,
                    expiry_date=expiryDate,
                    strike_price=strikePrice,
                    CE_open_interest=ce_data.get("openInterest", 0),
                    CE_change_in_oi=ce_data.get("changeinOpenInterest", 0),
                    CE_last_price=ce_data.get("lastPrice", 0.0),
                    CE_bid_qty=ce_data.get("bidQty", 0),
                    CE_bid_price=ce_data.get("bidPrice", 0.0),
                    CE_ask_price=ce_data.get("askPrice", 0.0),
                    CE_ask_qty=ce_data.get("askQty", 0),
                    PE_open_interest=pe_data.get("openInterest", 0),
                    PE_change_in_oi=pe_data.get("changeinOpenInterest", 0),
                    PE_last_price=pe_data.get("lastPrice", 0.0),
                    PE_bid_qty=pe_data.get("bidQty", 0),
                    PE_bid_price=pe_data.get("bidPrice", 0.0),
                    PE_ask_price=pe_data.get("askPrice", 0.0),
                    PE_ask_qty=pe_data.get("askQty", 0),
                )
                record_count += 1
            except Exception as e:
                print(f"[{datetime.datetime.now()}] ❌ Error storing record for {symbol} (strike: {strikePrice}, expiry: {expiryDate}): {e}")
                continue

        print(f"[{datetime.datetime.now()}] ✅ Stored {record_count} records for {symbol}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ❌ Error processing records for {symbol}: {e}")

async def scrape_all_symbols():
    """Scrape all symbols concurrently"""
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [fetch_option_chain(sym, session) for sym in SYMBOLS]
        print(f"[{datetime.datetime.now()}] 📋 Starting tasks for symbols: {SYMBOLS}")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for symbol, data in results:
            if isinstance(data, Exception):
                print(f"[{datetime.datetime.now()}] ❌ Task failed for {symbol}: {data}")
                continue
            await store_data(symbol, data)
            if data:
                print(f"[{datetime.datetime.now()}] ✅ Completed processing for {symbol}")
            else:
                print(f"[{datetime.datetime.now()}] ⚠️ No data processed for {symbol}")

# Example to run the scraper
if __name__ == "__main__":
    asyncio.run(scrape_all_symbols())