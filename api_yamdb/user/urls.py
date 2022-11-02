from django.urls import path

from user.views import registrations_request

urlpatterns = [
    path('v1/auth/signup/', registrations_request, name='register'),
]
