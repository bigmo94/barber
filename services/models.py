import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .utils import truncate_number


class Service(models.Model):
    TYPE_HAIRCUT = 1
    TYPE_HAIR_STYLE = 2
    TYPE_BEARD_STYLE = 3
    TYPE_HAIR_KERATIN = 4
    TYPE_HAIR_COLORING = 5
    TYPE_SOLARIUM = 6
    TYPE_SKIN_CLEANING = 7

    SERVICES = (
        (TYPE_HAIRCUT, _('Haircut')),
        (TYPE_HAIR_STYLE, _('Hairstyle')),
        (TYPE_BEARD_STYLE, _('Beard Style')),
        (TYPE_HAIR_KERATIN, _('Hair keratin')),
        (TYPE_HAIR_COLORING, _('Hair coloring')),
        (TYPE_SOLARIUM, _('Solarium')),
        (TYPE_SKIN_CLEANING, _('Skin Cleaning')),
    )
    service_type = models.IntegerField(verbose_name=_('service type'), choices=SERVICES)
    price = models.IntegerField(verbose_name=_('Price'))
    discount = models.DecimalField(verbose_name=_('discount'), max_digits=5, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    duration = models.DurationField(verbose_name=_('duration'), default=datetime.timedelta(hours=1))
    description = models.CharField(verbose_name=_('Descriptions'), max_length=256, blank=True, null=True)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateField(verbose_name=_('updated time'), auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.get_service_type_display(), self.price)

    def save(self, *args, **kwargs):
        self.discount = self.discount or 0
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        calculate_discount = self.calculate_discount(self.price, self.discount)
        return truncate_number(number=calculate_discount, digits=2)

    @staticmethod
    def calculate_discount(price, discount):
        return price - ((price * discount) / 100)


class Reservation(models.Model):
    STATUS_PENDING = 1
    STATUS_IN_PROGRESS = 2
    STATUS_ACCEPT = 3

    STATUS_TYPE = (
        (STATUS_PENDING, _('pending')),
        (STATUS_IN_PROGRESS, _('in progress')),
        (STATUS_ACCEPT, _('accepted'))
    )

    user = models.ForeignKey(to='customers.User', verbose_name=_('user'), related_name='reservations',
                             on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(to='Service', verbose_name=_('service'), related_name='reservations',
                                on_delete=models.PROTECT)
    employee = models.ForeignKey(to='customers.Employee', verbose_name=_('employee'), related_name='reservations',
                                 on_delete=models.PROTECT)
    date = models.DateField(verbose_name='date')
    started_time = models.TimeField(verbose_name=_('started time'), default=datetime.time(hour=10, minute=0))
    ended_time = models.TimeField(verbose_name=_('ended_time'), default=datetime.time(hour=11, minute=0))
    status = models.IntegerField(verbose_name='status', choices=STATUS_TYPE, default=STATUS_PENDING)
    is_available = models.BooleanField(verbose_name=_('is available'), default=True)
    description = models.TextField(_('Descriptions'), blank=True, null=True)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)

    def __str__(self):
        return "{} - {} - {}".format(self.date, self.started_time, self.ended_time)


class EmployeeWorkingTime(models.Model):
    employee = models.ForeignKey(to='customers.Employee', verbose_name=_('employee'), on_delete=models.CASCADE)
    date = models.DateField(verbose_name='date')
    started_time = models.TimeField(verbose_name=_('started time'), default=datetime.time(hour=10, minute=0))
    ended_time = models.TimeField(verbose_name=_('ended_time'), default=datetime.time(hour=22, minute=0))

    def __str__(self):
        return self.employee.user.get_full_name()
