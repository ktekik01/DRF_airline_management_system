from django.urls import path
from .views import FlightListCreate, FlightDetail, FlightReservations

urlpatterns = [
    path('flights/',                  FlightListCreate.as_view(),    name='flight-list-create'),
    path('flights/<int:pk>/',         FlightDetail.as_view(),        name='flight-detail'),
    path('flights/<int:pk>/reservations/', FlightReservations.as_view(), name='flight-reservations'),
]
