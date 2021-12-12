from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from customers.utils import validate_birthday


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

    def get_access(self):
        return str(RefreshToken.for_user(self).access_token)

    def get_refresh(self):
        return str(RefreshToken.for_user(self))

    def get_token(self):
        return {
            'access': self.get_access(),
            'refresh': self.get_refresh(),
        }
