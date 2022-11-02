from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from .permissions import (IsAdminOrReadOnly,
                         IsAdminOrOwner,
                         IsAuthorOrReadOnly)
from .serializers import (CatSerializer,
                          CustomUserSerializer,
                          ISerializer,
                          GenreSerializer,
                          TitleGetSerializer,
                          TitlePostSerializer)
from reviews.models import Title, Category, Genre
from user.models import CustomUser


class MainViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]


class CategoryViewSet(MainViewSet):
    queryset = Category.objects.all()
    serializer_class = CatSerializer


class GenreViewSet(MainViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlePostSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filterset_class = 'фильтр'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminOrOwner, )
    search_fields = ('username', )
    # filter_backends =
    # filterset_fields =


    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = ISerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = ISerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
