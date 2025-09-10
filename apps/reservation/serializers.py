from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'passenger_name',
            'passenger_email',
            'reservation_code',  # read‑only (auto‑generated)
            'flight',
            'status',
            'created_at',        # read‑only
        ]
        read_only_fields = ('reservation_code', 'created_at')

    def validate(self, data):
        flight = data.get('flight')
        if flight and flight.reservations.count() >= flight.airplane.capacity:
            raise serializers.ValidationError(
                "Cannot book—this flight is already fully booked."
            )
        return data
