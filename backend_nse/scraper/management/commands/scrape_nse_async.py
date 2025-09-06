from django.core.management.base import BaseCommand
from scraper.async_scraper import scrape_all_symbols
import datetime
import asyncio
import time

class Command(BaseCommand):
    help = 'Scrape NSE option chain asynchronously every minute during market hours'

    def handle(self, *args, **kwargs):
        print("Starting async NSE scraper...")
        comand = True
        while True:
            now = datetime.datetime.now()
            # Market hours: 9:14 → 15:10
            if comand: # (now.hour == 9 and now.minute >= 14) or (10 <= now.hour <= 14) or (now.hour == 15 and now.minute <= 10):
                asyncio.run(scrape_all_symbols())
            else:
                print(f"[{now}] Market closed, waiting...")
            time.sleep(60)
