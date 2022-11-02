from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from user.models import CustomUser
from user.permission import (IsAdmin, )
from user.serializers import (CustomUserSerializer,
                              JWTTokenSerializer,
                              UserRegistrationSerializer, )


class CustomViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    search_fields = ['user__username']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def registrations_request(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(CustomUserSerializer,
                             username=serializer.validated_data['username'], )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Регистрация в YaMDb',
              message=f'Ваш код подтверждения: {confirmation_code}',
              from_email=None,
              recipient_list=[user.email], )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    code = serializer.data['confirmation_code']
    user = get_object_or_404(CustomUserSerializer, email=email)

    if default_token_generator.check_token(user, code):
        access_token = AccessToken.for_user(user)
        return Response({'token': f'{access_token}'},
                        status=status.HTTP_200_OK,
                        )
    return Response(
        {'token': 'Недействительный токен авторизации.'},
        status=status.HTTP_400_BAD_REQUEST,
    )
