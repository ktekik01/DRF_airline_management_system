from django.db import models
import random, string
from apps.flight.models import Flight

class Reservation(models.Model):
    passenger_name   = models.CharField(max_length=100)
    passenger_email  = models.EmailField()
    reservation_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )
    flight           = models.ForeignKey(
        Flight,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    status           = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            # Generate a 6‑character alphanumeric code
            self.reservation_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reservation_code} – {self.passenger_name}"
