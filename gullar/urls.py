from django.urls import path
from .views import *

urlpatterns = [
    path('', ListCreateAPI.as_view(), name='list'),
    path('flowers/<int:pk>/', DetailUpdateDeleteApi.as_view(), name='CRUD')
]
