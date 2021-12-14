from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .utils import truncate_number

User = get_user_model()


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
    service_type = models.IntegerField(verbose_name=_('service type'), choices=SERVICES, unique=True)
    price = models.IntegerField(verbose_name=_('Price'))
    discount = models.DecimalField(verbose_name=_('discount'), max_digits=5, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField(verbose_name=_('Descriptions'), max_length=256, blank=True, null=True)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateField(verbose_name=_('updated time'), auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.service_type, self.price)

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


class ServiceLog(models.Model):
    user = models.ForeignKey(to=User, verbose_name=_('user'), related_name='service_logs', on_delete=models.PROTECT)
    service = models.ForeignKey(to=Service, verbose_name=_('service'), related_name='service_logs', on_delete=models.PROTECT)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.service)


class Reservation(models.Model):
    user = models.ForeignKey(to=User, verbose_name=_('user'), related_name='reservations', on_delete=models.PROTECT)
    service = models.ForeignKey(to=Service, verbose_name=_('service'), related_name='reservations',
                                on_delete=models.PROTECT)
    reserve_time = models.DateTimeField(verbose_name=_('reserve time'), unique=True)
    description = models.TextField(_('Descriptions'), blank=True, null=True)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.service, self.reserve_time)
