from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Comments, AuctionUser, Bid
from .forms import AuctionListingForm


def index(request):
    list_nings = AuctionListing.objects.all()
    id_ = request.user.pk

    return render(request, "auctions/index.html", {"listnings": list_nings, "id": id_})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        # user = authenticate(request, username=username, password=password)
        # user = authenticate(request, username="Jack", password="12345678")
        user = authenticate(request, username=username, password=password)

        #user = User.objects.get(username=username, password=password)


        # Check if authentication successful
        if user is not None:
            login(request, user)

            if not AuctionUser.objects.filter(user=user).exists():
                au_user = AuctionUser(user=user)
                au_user.save()


            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        if not AuctionUser.objects.filter(user=user).exists():
            au_user = AuctionUser(user=user)
            au_user.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        tmp = AuctionListing(creator=request.user.username)
        auction_listing_form = AuctionListingForm(request.POST, request.FILES, instance=tmp
                                                  )
        # initial={"creator": request.user.username})
        if auction_listing_form.is_valid():
            auction_listing_form.save()

            return HttpResponseRedirect(reverse("index"))

    auction_listing_form = AuctionListingForm()
    return render(request, "auctions/create_listing.html", {"listing_form": auction_listing_form})


@login_required
def display_listing_info(request, name_of_listing):
    listning_ = AuctionListing.objects.get(listing_name=name_of_listing)
    current_user = request.user.username

    if request.method == "POST":
        if AuctionUser.objects.filter(user=request.user).exists():
            # au_user = AuctionUser.objects.get(pk=request.user.pk + 5)
            au_user = AuctionUser.objects.get(user=request.user)
            au_user.listing.add(listning_)
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            return HttpResponse("Not found")
    check_id = AuctionUser.objects.all()
    related_comment = listning_.comment.all()
    related_bid = None

    if listning_.related_bid.all().exists():
        related_bid = listning_.related_bid.all().last()

    return render(request, "auctions/distinct_listing.html", {
        "related": related_comment,
        "listing_object": listning_,
        "related_bid": related_bid,
        "check": check_id,
        "current_user": current_user

    })


@login_required
def watchlist(request):
    listing_watch = AuctionUser.objects.get(user=request.user).listing.all()

    return render(request, "auctions/watchlist.html", {"watch_listing": listing_watch})


def categories(request):
    categories_listing = AuctionListing.objects.all()
    list_of_categories = []
    for category_ in categories_listing:
        list_of_categories.append(category_.category)
    listings_for_categories = AuctionListing.objects.all()
    res = [*set(list_of_categories)]

    return render(request, "auctions/categories.html", {"categories": res, "listings_cat": listings_for_categories})


def category(request, category_):
    categories_list = AuctionListing.objects.filter(category=category_)
    return render(request, "auctions/distinct_category.html", {"objects": categories_list})


def remove_from_watchlist(request, listing_to_delete):
    to_delete = AuctionListing.objects.get(listing_name=listing_to_delete)
    au_user = AuctionUser.objects.get(user=request.user)
    au_user.listing.remove(to_delete)

    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def create_bid(request, for_listing):
    tmp = ""
    if request.method == "POST":
        number_bid = request.POST["new_bid"]
        if int(number_bid) <= AuctionListing.objects.get(pk=int(for_listing)).starting_bid:
            return HttpResponse("Bid should be more than given!")
        else:
            bid_ = Bid(related_to_auction=AuctionListing.objects.get(pk=int(for_listing)), current_bid=number_bid,
                       person_who_bid=request.user.username)
            bid_.save()
            tmp = AuctionListing.objects.get(pk=int(for_listing))
            tmp.starting_bid = number_bid
            tmp.save()
    return HttpResponseRedirect(reverse("goto_listning", kwargs={"name_of_listing": tmp.listing_name}))


@login_required
def create_comment(request, for_listing):
    if request.method == "POST":
        comment_ = request.POST["add_comment"]

        bid_ = Comments(related_to=AuctionListing.objects.get(pk=int(for_listing)), comment_itself=comment_,
                        person_who_commented=request.user.username)
        bid_.save()

    return HttpResponseRedirect(
        reverse("goto_listning",
                kwargs={"name_of_listing": AuctionListing.objects.get(pk=int(for_listing)).listing_name}))


def close_item(request, item_id):
    if request.method == "POST":
        auction_object = AuctionListing.objects.get(pk=int(item_id))
        auction_object.status = False
        auction_object.save()
    return HttpResponseRedirect(
        reverse("goto_listning", kwargs={"name_of_listing": AuctionListing.objects.get(pk=int(item_id)).listing_name}))
