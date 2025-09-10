import django_filters
from .models import Flight

class FlightFilter(django_filters.FilterSet):
    departure_date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date')
    arrival_date   = django_filters.DateFilter(field_name='arrival_time',   lookup_expr='date')

    class Meta:
        model  = Flight
        fields = {
            'departure':   ['exact'],    # ?departure=Heathrow
            'destination': ['exact'],    # ?destination=Istanbul
        }
