from rest_framework import generics
from apps.reservation.models import Reservation
from apps.reservation.serializers import ReservationSerializer
from django.core.mail import send_mail
from django.conf import settings


# GET /api/reservations/    POST /api/reservations/
class ReservationListCreate(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # 1. Save the reservation (runs your occupancy check + code generation)
        reservation = serializer.save()

        # 2. Compose & send confirmation email
        subject = f"Your Reservation {reservation.reservation_code} is Confirmed"
        message = (
            f"Hello {reservation.passenger_name},\n\n"
            f"Your reservation (code: {reservation.reservation_code}) for flight "
            f"{reservation.flight.flight_number} from {reservation.flight.departure} "
            f"to {reservation.flight.destination} on "
            f"{reservation.flight.departure_time:%Y-%m-%d %H:%M} has been confirmed.\n\n"
            "Thank you for choosing us!"
        )
        recipient = [reservation.passenger_email]

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient,
            fail_silently=False,
        )

# GET /api/reservations/{id}/  PATCH, DELETE
class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
