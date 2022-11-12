from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<name_of_listing>", views.display_listing_info, name="goto_listning"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.categories, name="category"),
    path("category/<category_>", views.category, name="goto_category"),
    path("remove/<listing_to_delete>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("create_bid/<for_listing>", views.create_bid, name="create_bid"),
    path("create_comment/<for_listing>", views.create_comment, name="create_comment"),
    path("close/<item_id>", views.close_item, name="close_item")

]
