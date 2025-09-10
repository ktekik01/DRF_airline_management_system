# apps/airplane/urls.py

from django.urls import path
from .views import (
    AirplaneListCreate,
    AirplaneDetail,
    AirplaneFlights,
)

urlpatterns = [
    path('airplanes/',                  AirplaneListCreate.as_view(),   name='airplane-list-create'),
    path('airplanes/<int:pk>/',         AirplaneDetail.as_view(),       name='airplane-detail'),
    path('airplanes/<int:pk>/flights/', AirplaneFlights.as_view(),     name='airplane-flights'),
]
