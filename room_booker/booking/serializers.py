from rest_framework import serializers

from .models import Room, Renter, Resident, ROOM_TYPES


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RenterSerializer(serializers.ModelSerializer):
    class Meta:
        model: Renter
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = '__all__'


class BookingSerializer(serializers.Serializer):
    resident = ResidentSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
