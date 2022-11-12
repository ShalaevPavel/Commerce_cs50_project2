from django.forms import forms
from .models import AuctionListing
from django.forms import ModelForm


class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('listing_name',
                  'listing_url',
                  'listing_description',
                  'starting_bid',
                  'category')
