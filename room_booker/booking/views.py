from collections import OrderedDict
from django.utils import timezone
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from room_booker.general.paginations import get_pagination
from room_booker.booking.utils import booking, gen_available_times
from .models import Resident, Room
from .serializers import RoomSerializer, BookingSerializer


date = openapi.Parameter(
    "date", openapi.IN_QUERY,
    description="Date. Format: 'dd-MM-YYYY'",
    type=openapi.TYPE_STRING,
    pattern='^\d{2}-\d{2}-\d{4}$',
)

page_size = openapi.Parameter(
    "page_size", openapi.IN_QUERY,
    description="page size",
    type=openapi.TYPE_INTEGER
)

type = openapi.Parameter(
    "type", openapi.IN_QUERY,
    description='Room type: Choices ["focus", "team", "conference"]',
    type=openapi.TYPE_STRING,
)


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = get_pagination()

    @swagger_auto_schema(manual_parameters=[page_size, type])
    def get(self, request, *args, **kwargs):
        page_size = request.GET.get('page_size', 10)
        type = request.GET.get('type', None)

        if type:
            self.queryset = self.queryset.filter(type=type)

        self.pagination_class = get_pagination(int(page_size))
        
        return super().get(request, *args, **kwargs)


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


class RoomAvailabilityView(APIView):
    @swagger_auto_schema(manual_parameters=[date])
    def get(self, request, room_id):
        date = request.GET.get('date', None)
        if not date:
            date = timezone.now().date()
        else:
            date = timezone.datetime.strptime(date, "%d-%m-%Y").date()

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"message": "Room does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        available_times = gen_available_times(date, room)

        return Response(available_times, status.HTTP_200_OK)

class RoomBookingView(APIView):
    @swagger_auto_schema(request_body=BookingSerializer)
    def post(self, request, room_id):
        serializer = BookingSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.error_messages)
            print(serializer.errors)
            return Response({"message": "Validation failed"}, status=status.HTTP_400_BAD_REQUEST)

        room = Room.objects.get_or_none(id=room_id)
        if not room:
            return Response({"message": "Room is not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]
        resident: OrderedDict = serializer.validated_data["resident"]
        resident, created =Resident.objects.get_or_create(name=resident["name"])

        is_booked = booking(start=start, end=end, room=room, resident=resident)

        if is_booked:
            return Response({"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "uzr, siz tanlagan vaqtda xona band"}, status=status.HTTP_410_GONE)
