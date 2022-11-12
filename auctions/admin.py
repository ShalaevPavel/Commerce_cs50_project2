from django.contrib import admin
from auctions.models import User, AuctionListing, Comments, Bid, AuctionUser

# Register your models here.


admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Comments)
admin.site.register(Bid)
admin.site.register(AuctionUser)
