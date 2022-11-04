from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
from user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    def validate_username(self, data):
        if data.lower() == 'me':
            raise serializers.ValidationError('Запрещено использовать "me" в'
                                              ' качестве имени пользователя!')
        return data

    class Meta:
        fields = ('username', 'email',)
        model = CustomUser


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class MeSerializer(serializers.ModelSerializer):
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

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleRWSerializer(serializers.ModelSerializer):
    """Основной метод записи информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleROSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Ошибка. Ваш отзыв уже добавлен.')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
