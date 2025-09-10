from rest_framework import generics
from apps.flight.models import Flight
from apps.flight.serializers import FlightSerializer
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.flight.filters import FlightFilter

# GET /api/flights/      POST /api/flights/
class FlightListCreate(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

# GET /api/flights/{id}/  PATCH, DELETE
class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

# GET /api/flights/{id}/reservations/
class FlightReservations(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(flight_id=self.kwargs['pk'])
