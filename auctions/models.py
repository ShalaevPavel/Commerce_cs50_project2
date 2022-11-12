from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_active = models.BooleanField(default=True)


class AuctionListing(models.Model):
    listing_name = models.CharField(max_length=64)
    listing_url = models.TextField(blank=True)
    listing_description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64, blank=True)
    creator = models.CharField(max_length=64, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing_name} {self.listing_description} starting bid is {self.starting_bid}"


class AuctionUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(AuctionListing, blank=True, related_name="auction_users")

    def __str__(self):
        return self.user.username


class Comments(models.Model):
    related_to = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment")
    comment_itself = models.TextField()
    person_who_commented = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.comment_itself


class Bid(models.Model):
    related_to_auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="related_bid")
    current_bid = models.IntegerField()
    person_who_bid = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.current_bid

