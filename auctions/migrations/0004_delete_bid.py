# Generated by Django 4.1.2 on 2023-11-26 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_image_url_remove_user_watchlist_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
