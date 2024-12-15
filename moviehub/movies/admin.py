from django.contrib import admin
from .models import User, Genre, Movie, Favorite, Rating
from import_export.admin import ExportMixin
from .resources import MovieResource
class GenreInline(admin.TabularInline):  # Встроенные жанры для фильма
    model = Movie.genres.through  # Отображаем связь M2M
    extra = 1  # Показываем одну пустую строку для добавления нового жанра

class FavoriteInline(admin.TabularInline):  # Встроенные избранные для фильма
    model = Favorite
    extra = 0
    fields = ('user',)
    readonly_fields = ('user',)
class MovieAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = MovieResource  # Подключаем ресурс для экспорта

    list_display = ('id', 'title', 'release_date', 'created_by_link', 'genre_list')  
    list_display_links = ('title',)  # Гиперссылка на редактирование фильма
    search_fields = ('title', 'description')  # Поиск по названию и описанию
    list_filter = ('release_date', 'genres')  # Фильтры по дате выхода и жанрам
    ordering = ('-release_date',)  # Сортировка по дате выхода (по убыванию)
    
    # Кастомизация отображения полей при редактировании
    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'description', 'release_date', 'created_by')
        }),
        ("Связи и доп. информация", {
            'fields': ('genres',),
        }),
    )
    inlines = [GenreInline, FavoriteInline]  # Встроенные списки жанров и избранного

    # Отображение полей только для чтения
    readonly_fields = ('created_by',)  

    def created_by_link(self, obj):
        """Гиперссылка на пользователя, создавшего фильм"""
        if obj.created_by:
            url = f"/admin/auth/user/{obj.created_by.id}/change/"
            return f'<a href="{url}">{obj.created_by.username}</a>'
        return "Не указано"
    created_by_link.allow_tags = True
    created_by_link.short_description = "Создатель (ссылка)"

    def genre_list(self, obj):
        """Список жанров в удобном формате"""
        return ", ".join([genre.name for genre in obj.genres.all()])
    genre_list.short_description = "Жанры"
    
# Настройка админки для жанров
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

# Настройка админки для избранных
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'movie_link')
    search_fields = ('user__username', 'movie__title')

    def user_link(self, obj):
        """Гиперссылка на пользователя"""
        if obj.user:
            url = f"/admin/auth/user/{obj.user.id}/change/"
            return f'<a href="{url}">{obj.user.username}</a>'
        return "Не указано"
    user_link.allow_tags = True
    user_link.short_description = "Пользователь"

    def movie_link(self, obj):
        """Гиперссылка на фильм"""
        if obj.movie:
            url = f"/admin/movies/movie/{obj.movie.id}/change/"
            return f'<a href="{url}">{obj.movie.title}</a>'
        return "Не указано"
    movie_link.allow_tags = True
    movie_link.short_description = "Фильм"
    
    
    
admin.site.register(Movie, MovieAdmin)
admin.site.register(User)
admin.site.register(Rating)