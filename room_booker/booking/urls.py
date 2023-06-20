from django.urls import path

from . import views


urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='rooms-list'),
    path('rooms/<int:room_id>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/availability/', views.RoomAvailabilityView.as_view(), name='room-availability'),
    path('rooms/<int:room_id>/book/', views.RoomBookingView.as_view(), name='room-booking')
]