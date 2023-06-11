from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import Request, APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Room, Renter, Resident
from .serializers import (
    RoomSerializer,
)


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class RoomDetailView(APIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self, room_id):
        queryset = self.queryset
        try:
            
            return queryset.get(pk=room_id)
        except Room.DoesNotExist:
            raise Http404
        
    def get(self, request, room_id, format=None):
        room = self.get_object(room_id)
        serializer = self.serializer_class(room)
        return Response(serializer.data)
