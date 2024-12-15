from django.contrib import admin
from .models import User, Genre, Movie, Favorite, Rating

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Favorite)
admin.site.register(Rating)