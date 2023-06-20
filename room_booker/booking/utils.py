import datetime as d
from .models import Renter, Resident, Room
from django.utils import timezone


START_TIME = d.time(hour=9)  # 09:00
END_TIME = d.time(hour=22)  # 22:00


def create_datetime(date, time):
    return timezone.datetime(
        day=date.day,
        month=date.month,
        year=date.year,
        hour=time.hour,
        minute=time.minute
    )


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"[{self.start} - {self.end}]"

    def dict(self, date):
        res = {
            "start": create_datetime(date, self.start),
            "end": create_datetime(date, self.end),
        }
        return res


def gen_available_times(date: d.date, room: Room):
    renters = Renter.objects.filter(
        room=room,
        start__contains=date
    ).order_by('start')

    available_times = []
    busy_times = []

    for renter in renters:
        busy_time = Interval(renter.start.time(), renter.end.time())
        print(busy_time.__dict__)
        busy_times.append(busy_time)

    start_time = START_TIME
    for busy_time in busy_times:
        if busy_time.start > start_time:
            available = Interval(start_time, busy_time.start).dict(date)
            available_times.append(available)

            start_time = busy_time.end
        else:
            start_time = max(start_time, busy_time.end)

    if start_time < END_TIME:
        available = Interval(start_time, END_TIME).dict(date)
        available_times.append(available)

    return available_times


def booking(start: timezone.datetime, end: timezone.datetime, room, resident: Resident):
    date = start.date()

    start  = start.replace(tzinfo=timezone.tzinfo)
    end = end.replace(tzinfo=timezone.tzinfo)

    available_times = gen_available_times(date, room)

    for available in available_times:       
        if start >= available['start']:
            if end <= available['end']:
                Renter.objects.create(room=room, resident=resident, start=start, end=end)
                break
            else:
                continue
    else:
        return False
    
    return True


