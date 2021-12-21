import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from services.models import EmployeeWorkingTime, Reservation


@receiver(post_save, sender=EmployeeWorkingTime)
def create_reserves_time(sender, instance, created, **kwargs):
    start = instance.started_time.hour
    end = instance.ended_time.hour
    partition_time = end - start

    if created:
        reserves = []
        for i in range(partition_time):
            reserves.append(
                Reservation(date=instance.date, service=instance.service,
                            started_time=datetime.time(hour=start + i),
                            ended_time=datetime.time(hour=start + i + 1)))
        Reservation.objects.bulk_create(reserves)
