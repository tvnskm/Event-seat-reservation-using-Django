# models.py

from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Seat(models.Model):
    row = models.IntegerField(null=True)  # Row number
    number = models.IntegerField(null=True)  # Seat number
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    is_booked = models.BooleanField(default=False)  # Track if the seat is booked
    booked_by = models.CharField(max_length=255, null=True, blank=True)  # Store customer's name

    def __str__(self):
        return f"Row {self.row}, Seat {self.number}, Booked by {self.booked_by if self.booked_by else 'Available'}"
