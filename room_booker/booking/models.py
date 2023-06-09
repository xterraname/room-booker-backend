from django.db import models

from room_booker.general.models import CreatedModified, CustomModel


ROOM_TYPES = [
    ("focus", "Focus"),
    ("team", "Team"),
    ("conference", "Conference"),
]


class Resident(CreatedModified):
    name = models.CharField(max_length=100, unique=True)


class Room(CustomModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)

    capacity = models.PositiveIntegerField(default=1)


class Renter(CreatedModified):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="renters")
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="renters")

    start = models.DateTimeField()
    end = models.DateTimeField()
