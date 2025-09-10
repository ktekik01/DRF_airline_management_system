from django.urls import path
from .views import ReservationListCreate, ReservationDetail

urlpatterns = [
    path('reservations/',             ReservationListCreate.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/',    ReservationDetail.as_view(),      name='reservation-detail'),
]
