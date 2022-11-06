from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

from user.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
