from django.contrib import admin

from .models import Room, Renter, Resident


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity')
    list_editable = ('type', 'capacity')

@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('resident', 'room', 'start', 'end')
    list_editable = ('room', 'start', 'end')


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name',)
