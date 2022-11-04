from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       UserViewSet,
                       ReviewViewSet,
                       CommentViewSet)


router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/token/', token.as_view()),
    # path('v1/auth/signup/', auth.as_view()),
]
