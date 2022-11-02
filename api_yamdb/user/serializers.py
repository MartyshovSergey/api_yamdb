from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
