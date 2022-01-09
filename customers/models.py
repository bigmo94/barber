import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=False)
    is_employee = models.BooleanField(verbose_name=_('is employee'), default=False)
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

    service = models.ManyToManyField(to='services.Service', verbose_name=_('service'))
    name = models.CharField(verbose_name=_('name'), max_length=255)
    logo = models.ImageField(verbose_name=_('logo'), upload_to='customers/store/logo', blank=True, null=True)
    address = models.TextField(verbose_name=_('address'))
    phone = models.CharField(verbose_name=_('phone number'), max_length=50, unique=True)
    store_type = models.IntegerField(verbose_name=_('store type'), choices=TYPE_CHOICES, default=FOR_EVERYONE)
    client_id = models.UUIDField(verbose_name=_('API KEY'),
                                 max_length=50,
                                 unique=True,
                                 db_index=True,
                                 default=uuid.uuid4)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=False)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.ForeignKey(to='User', verbose_name=_('user'), related_name='users', on_delete=models.PROTECT)
    store = models.ForeignKey(to='Store', verbose_name=_('store'), related_name='stores', on_delete=models.PROTECT)
    service = models.ManyToManyField(to='services.Service', verbose_name=_('service'))
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def __str__(self):
        return self.user.get_full_name()
