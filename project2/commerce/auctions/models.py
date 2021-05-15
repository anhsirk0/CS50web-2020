from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


def get_time():
    now = datetime.now()
    now_str = now.strftime("%d/%m/%Y %H:%M:%S")
    return now_str


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Auction_item(models.Model):
    categories = [
        ("books", "books"),
        ("clothing", "clothing"),
        ("electronics", "electronics"),
        ("home", "home"),
        ("toys", "toys"),
        ("other", "other"),
    ]
    name = models.CharField(max_length=64)
    about = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(
        User, related_name="item", on_delete=models.CASCADE)
    imgurl = models.CharField(max_length=64)
    category = models.CharField(
        max_length=64, choices=categories, default="other")
    created_on = models.CharField(default=get_time(), max_length=64)
    # helpers
    max_bid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    active = models.BooleanField(default=True, null=True)
    winner = models.ForeignKey(
        User, related_name="won_item", on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{self.name}, {self.price} $, ({self.owner.username}) , [{self.category}]"


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, related_name="bid", on_delete=models.CASCADE)
    item = models.ForeignKey(
        Auction_item, related_name="bids", on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.bid} $ on {self.item} by {self.bidder}"


class Comment(models.Model):
    text = models.CharField(max_length=64)
    commented_by = models.ForeignKey(
        User, related_name="comment", on_delete=models.CASCADE)
    item = models.ForeignKey(
        Auction_item, related_name="comment", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} by {self.commented_by}"


class Watchlist(models.Model):
    owner = models.ForeignKey(
        User, related_name="watchlist", on_delete=models.CASCADE)
    item = models.ManyToManyField(
        Auction_item, related_name="watchlist", blank=True)

    def __str__(self):
        return f"of {self.owner}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    item = models.ForeignKey(
        Auction_item, related_name="item", on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    type = models.CharField(max_length=32)
    color = models.CharField(max_length=32, default="orange")
    time = models.CharField(max_length=64, default=get_time())

    def __str__(self):
        return f"{self.text} seen-{self.seen}"
