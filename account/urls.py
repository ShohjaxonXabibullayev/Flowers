from django.urls import path
from .views import *

urlpatterns = [
    path('regis/', RegisterApi.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('profile/', ProfileAPI.as_view())
]
