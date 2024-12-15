"""
URL configuration for moviehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import UserViewSet, GenreViewSet, MovieViewSet, FavoriteViewSet, RatingViewSet, FilteredMoviesView, FilteredFavoritesView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('genres', GenreViewSet)
router.register('movies', MovieViewSet, basename='movie')
router.register('favorites', FavoriteViewSet)
router.register('ratings', RatingViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/filtered-movies/', FilteredMoviesView.as_view(), name='filtered-movies'),
    path('api/filtered-favorites/', FilteredFavoritesView.as_view(), name='filtered-favorites'),

]
