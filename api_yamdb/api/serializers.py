from rest_framework import serializers

from reviews.models import Category, Genre, Title
from user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        # exclude = ('id', )


class TitleGetSerializer(serializers.ModelSerializer):
    """Получение."""

    category = CatSerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    """Запись."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False,

    )

    class Meta:
        fields = '__all__'
        model = Title


class ISerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
