from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    path("listing/<int:id>", views.listing_detail, name="listing"), #had name=listing_detail instead of name=listing
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:id>", views.watchlistAdd, name="watchlistAdd"),
    path("watchlist/delete/<int:id>", views.watchlistDelete, name="watchlistDelete"),
    path("bid/<int:bid_id>/<int:id>", views.bid, name="bid"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("comments/<int:id>", views.comment, name="add_comment")
]
