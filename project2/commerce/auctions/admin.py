from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_item)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Notification)
