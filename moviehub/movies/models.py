from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для обратной связи
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Уникальное имя для обратной связи
        blank=True,
    )

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title
