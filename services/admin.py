from django.contrib import admin
from services.models import Service, Reservation


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'price', 'discount', 'duration', 'store']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['service', 'employee', 'user', 'date', 'started_time', 'ended_time', 'status', 'is_available']

