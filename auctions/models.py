from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    imageURL = models.URLField(blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    active = models.BooleanField(default=True) 
    winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.title}: made by {self.user.username}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctioner')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} bids {self.bid} on {self.listing.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'[{self.listing.title}]{self.user}: {self.text}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ManyToManyField('Listing')

    def __str__(self):
        return f"{self.user}'s Watchlist "
