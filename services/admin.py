from django.contrib import admin
from .models import Service, Reservation, EmployeeWorkingTime


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'price', 'discount', 'duration']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['service', 'employee', 'user', 'date', 'started_time', 'ended_time', 'status', 'is_available']


@admin.register(EmployeeWorkingTime)
class EmployeeWorkingTimeAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'started_time', 'ended_time']
