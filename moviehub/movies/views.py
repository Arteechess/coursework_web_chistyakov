from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Genre, Movie, Favorite, Rating
from .serializers import UserSerializer, GenreSerializer, MovieSerializer, FavoriteSerializer, RatingSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .pagination import CustomPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    @action(methods=['GET'], detail=False)
    def filter_by_genre(self, request):
        genre_name = request.query_params.get('genre', None)
        if not genre_name:
            return Response({"error": "Genre parameter is required."}, status=400)
        movies = Movie.objects.filter(
            Q(genres__name__icontains=genre_name)
        ).distinct()
        
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    @action(methods=['POST'], detail=True)
    def add_to_favorites(self, request, pk=None):
        user = request.user  # Текущий пользователь
        movie = self.get_object()  # Конкретный фильм
        
        # Проверяем, существует ли уже запись в избранном
        if Favorite.objects.filter(user=user, movie=movie).exists():
            return Response({"error": "Movie is already in favorites."}, status=400)
        
        # Создаем запись в избранном
        favorite = Favorite.objects.create(user=user, movie=movie)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=201)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class FilteredMoviesView(ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination  # Указываем пагинацию

    def get_queryset(self):
        return Movie.objects.filter(
            (Q(genres__name="Action") | Q(genres__name="Adventure")) &  # OR
            Q(release_date__gt="2020-01-01") &  # AND
            ~Q(created_by__role="admin")  # NOT
        ).distinct()


class FilteredFavoritesView(ListAPIView):
    serializer_class = FavoriteSerializer
    pagination_class = CustomPagination  # Указываем пагинацию

    def get_queryset(self):
        return Favorite.objects.filter(
            (Q(user_id=2) | Q(movie__ratings__score__gt=4)) &  # OR
            Q(movie__genres__name="Drama") &  # AND
            ~Q(movie__title__icontains="Horror")  # NOT
        ).distinct()