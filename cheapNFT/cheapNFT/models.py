from django.db import models

class Auction(models.Model):
    id = models.IntegerField(primary_key=True)
    creator = models.CharField(max_length=42, default="")
    collection = models.CharField(max_length=42, default="")
    token_id = models.IntegerField()
    payment_token = models.CharField(max_length=42, default="")
    bidder_sig = models.CharField(max_length=132, default=None)
    amount = models.BigIntegerField(default=None)