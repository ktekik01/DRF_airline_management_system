from django.shortcuts import render

from rest_framework import generics
from apps.airplane.models import Airplane
from apps.airplane.serializers import AirplaneSerializer
from apps.flight.models import Flight
from apps.flight.serializers import FlightSerializer
from apps.reservation.models import Reservation

# GET  /api/airplanes/       POST /api/airplanes/
class AirplaneListCreate(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

# GET /api/airplanes/{id}/   PATCH, DELETE
class AirplaneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


    def perform_update(self, serializer):
        # 1) Save the updated airplane
        airplane = serializer.save()

        # 2) If its status was turned off, deactivate all its reservations
        #    (we look up reservations via flight__airplane=...)
        if 'status' in serializer.validated_data and not serializer.validated_data['status']:
            Reservation.objects.filter(
                flight__airplane=airplane
            ).update(status=False)

# GET /api/airplanes/{id}/flights/
class AirplaneFlights(generics.ListAPIView):
    serializer_class = FlightSerializer

    def get_queryset(self):
        return Flight.objects.filter(airplane_id=self.kwargs['pk'])
