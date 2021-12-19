from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from customers.utils import validate_birthday
from services.models import Service


class User(AbstractUser):
    MALE = True
    FEMALE = False

    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    email = models.EmailField(verbose_name=_('email address'), blank=True, null=True)
    phone = models.CharField(verbose_name=_('phone number'), max_length=50, unique=True,
                             validators=[RegexValidator(regex='^\+?[1-9]\d{1,14}$',
                                                        message=_('The phone number is not valid'),
                                                        code='invalid_phone_number')])
    birthday = models.DateField(verbose_name=_('birthday'), null=True, blank=True, validators=[validate_birthday])
    gender = models.BooleanField(verbose_name=_('gender'), choices=GENDER_CHOICES, null=True, blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, null=True, upload_to='customers/user/avatar')
    is_active = models.BooleanField(_('active'), default=False)
    created_time = models.DateField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


class Store(models.Model):
    FOR_MEN = 1
    FOR_WOMEN = 2
    FOR_EVERYONE = 3

    TYPE_CHOICES = (
        (FOR_MEN, _('for men')),
        (FOR_WOMEN, _('for women')),
        (FOR_EVERYONE, _('for everyone')),
    )

    service = models.ForeignKey(to='services.Service', verbose_name=_('service'), related_name='stores',
                                on_delete=models.PROTECT)
    name = models.CharField(verbose_name=_('name'), max_length=255)
    logo = models.ImageField(verbose_name=_('logo'), upload_to='customers/store/logo', blank=True, null=True)
    address = models.TextField(verbose_name=_('address'))
    phone = models.CharField(verbose_name=_('phone number'), max_length=50, unique=True)
    store_type = models.IntegerField(verbose_name=_('store type'), choices=TYPE_CHOICES, default=FOR_EVERYONE)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)
    rate = models.DecimalField(verbose_name=_('rate'), max_digits=5, decimal_places=2, null=True, blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(verbose_name=_('active'), default=False)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        ordering = ('rate', )

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(verbose_name='name', max_length=120)
    store = models.ForeignKey(to='Store', verbose_name='store', related_name='stores', on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name='is active', default=True)

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def __str__(self):
        return self.name

