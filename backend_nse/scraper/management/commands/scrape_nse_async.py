from django.core.management.base import BaseCommand
from scraper.async_scraper import scrape_all_symbols
import asyncio
import time
from datetime import datetime
import pytz

# Get current time in IST

class Command(BaseCommand):
    help = 'Scrape NSE option chain asynchronously every minute during market hours'

    def handle(self, *args, **kwargs):
        print("Starting async NSE scraper...")
        while True:
            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            # Market hours: 9:14 → 15:10
            if  (now.hour == 9 and now.minute >= 14) or (10 <= now.hour <= 14) or (now.hour == 15 and now.minute <= 10):
                asyncio.run(scrape_all_symbols())
            else:
                print(f"[{now}] Market closed, waiting...")
            time.sleep(60)
