from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django  import forms
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Category, Comment, Watchlist


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'imageURL']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label='Comment')


def index(request):
    return render(request, "auctions/index.html", {
        'auction': Listing.objects.filter(active=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    return render(request, 'auctions/categories.html', {
        "categories": Category.objects.all()
    })
 
def categorylistings(request, category_id):
    listings = Listing.objects.filter(category_id=category_id, active=True)
    return render(request, "auctions/categorylistings.html", {
        'category': get_object_or_404(Category, id=category_id),
        'listings': listings
    })

def listing_detail(request, id):
    item = get_object_or_404(Listing, id=id)
    user = request.user
    in_watchlist = user.watchlist.filter(listing=item).exists()
    
    return render(request, 'auctions/listing.html', {
        'item': item,
        'in_watchlist': in_watchlist,
    })

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        f = AuctionForm(request.POST)
        if f.is_valid():
            title = f.cleaned_data['title']
            description = f.cleaned_data['description']
            starting_bid = f.cleaned_data['starting_bid']
            category = f.cleaned_data['category']
            imageURL = f.cleaned_data['imageURL']

            listing = Listing(user=request.user, title=title, description=description, starting_bid=starting_bid, category=category, imageURL=imageURL)
            listing.save() 

            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            message = "Form was invalid."
            return render(request, 'auctions/create.html', {
                'form': f,
                'message': message,
                'categories': Category.objects.all()
            })
    else:
        f = AuctionForm()
        return render(request, "auctions/create.html", {
            'form': f
        })


@login_required(login_url='login')
def watchlist(request):
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    listings = []
    if not created:
        listings = user_watchlist.listing.all()
    return render(request, "auctions/watchlist.html", {
        'watchlist': listings
    })

@login_required(login_url='login')
def watchlistAdd(request, id): 
    listing = get_object_or_404(Listing, id=id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listing.add(listing)
    watchlist.save()
    return HttpResponseRedirect(reverse('auctions:watchlist'))

@login_required(login_url='login')
def watchlistDelete(request, id): 
    listing = get_object_or_404(Listing, id=id)
    request.user.watchlist.remove(listing)
    request.user.save()
    return HttpResponseRedirect(reverse('auctions:watchlist'))


@login_required(login_url='login')
def bid(request, id):
    auction = get_object_or_404(Listing, id=id)
    price = float(request.POST['bid_amount'])
    #bid = Bid.objects.filter(user=request.user, listing=auction).first()

    #if not bid or price > bid.bid:
    #    bid.bid = price
    #   bid.save()
    if price > auction.price:
        auction.price = price
        auction.save()
        return HttpResponseRedirect(reverse('auctions:index'))
    else:
        raise ValueError('Your bid is lower than the current highest bid.')

@login_required(login_url='login')
def close_bid(request, id):
    auction = get_object_or_404(Listing, id=id)
    auction.active = False
    auction.winner = request.user.username
    auction.save()
    return HttpResponseRedirect(reverse('auctions:listing_detail', args=(id,)))


@login_required(login_url='login')
def comment(request, id):
    f = CommentForm(request.POST)
    if f.is_valid():
        comment = Comment(user=request.user, listing=get_object_or_404(Listing, id=id))
        comment.save()
        return HttpResponseRedirect(reverse('listing', id=id))
    
