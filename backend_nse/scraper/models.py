# options/models.py
from django.db import models

class OptionChain(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=20)
    current_price = models.FloatField()

    # CE Columns
    CE_open_interest = models.BigIntegerField(default=0)
    CE_change_in_oi = models.BigIntegerField(default=0)
    CE_last_price = models.FloatField(default=0.0)
    CE_bid_qty = models.BigIntegerField(default=0)
    CE_bid_price = models.FloatField(default=0.0)
    CE_ask_price = models.FloatField(default=0.0)
    CE_ask_qty = models.BigIntegerField(default=0)
    strike_price = models.FloatField()
    # PE Columns
    PE_open_interest = models.BigIntegerField(default=0)
    PE_change_in_oi = models.BigIntegerField(default=0)
    PE_last_price = models.FloatField(default=0.0)
    PE_bid_qty = models.BigIntegerField(default=0)
    PE_bid_price = models.FloatField(default=0.0)
    PE_ask_price = models.FloatField(default=0.0)
    PE_ask_qty = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.strike_price} @ {self.timestamp}"
