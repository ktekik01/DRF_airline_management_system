# apps/flight/serializers.py

from rest_framework import serializers
from .models import Flight
from datetime import timedelta

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Flight
        fields = [
            'id',
            'flight_number',
            'departure',
            'destination',
            'departure_time',
            'arrival_time',
            'airplane',
        ]

    def validate(self, data):
        # On PATCH, some keys may be missing—fall back to instance values
        dep = data.get(
            'departure_time',
            getattr(self.instance, 'departure_time', None)
        )
        arr = data.get(
            'arrival_time',
            getattr(self.instance, 'arrival_time', None)
        )

        # Both must exist now
        if dep is None or arr is None:
            raise serializers.ValidationError(
                "Both departure_time and arrival_time are required."
            )

        # 1) Arrival after departure
        if dep >= arr:
            raise serializers.ValidationError({
                'arrival_time': 'Must be after departure_time.'
            })

        # 2) Conflict check
        airplane = data.get(
            'airplane',
            getattr(self.instance, 'airplane', None)
        )
        if airplane is None:
            # Shouldn’t happen—airplane is required on create
            raise serializers.ValidationError({
                'airplane': 'Airplane must be set.'
            })

        # Build the comparison queryset
        qs = Flight.objects.filter(airplane=airplane)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        # Ensure no overlap with ±1h buffer
        for other in qs:
            # A flight is “blocked” from other.arrival_time+1h to other.departure_time-1h
            start_buffer = other.arrival_time + timedelta(hours=1)
            end_buffer   = other.departure_time - timedelta(hours=1)
            # They conflict if [dep, arr] overlaps that blocked zone
            if not (arr <= end_buffer or dep >= start_buffer):
                raise serializers.ValidationError(
                    'This flight conflicts with another flight on the same airplane '
                    '– you need at least a 1‑hour gap.'
                )

        return data
