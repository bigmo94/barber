from django.utils.translation import ugettext_lazy as _

SUCCESS_MESSAGE_READ = 2001
SUCCESS_RESET_CODE_WAS_SENT = 2002
SUCCESS_WORKING_TIME_WAS_RECORDED = 2003

SUCCESS_MESSAGE_CODES = {
    SUCCESS_MESSAGE_READ: _("The message was read"),
    SUCCESS_RESET_CODE_WAS_SENT: _('The reset code was sent'),
    SUCCESS_WORKING_TIME_WAS_RECORDED: _('The working time was recorded')
}

ERROR_UNKNOWN = 4000
ERROR_WRONG_VERIFY_CODE = 4001
ERROR_TOKEN_IS_NOT_VALID = 4002
ERROR_BIRTHDAY_FIELD_IS_NOT_VALID = 4003
ERROR_NOT_FOUND_ANY_USER_BY_THIS_USERNAME = 4004
ERROR_DUPLICATE_VALUE = 4005
ERROR_INVALID_AUTHORIZATION_HEADER = 4006
ERROR_STORE_NOF_FOUND = 4007
ERROR_STORE_IS_INACTIVE = 4008


ERROR_MESSAGE_CODES = {
    ERROR_UNKNOWN: _("Some error happened. please call administrator."),
    ERROR_WRONG_VERIFY_CODE: _("Wrong verify code"),
    ERROR_TOKEN_IS_NOT_VALID: _("Token is not valid."),
    ERROR_DUPLICATE_VALUE: _("Values are duplicated"),
    ERROR_BIRTHDAY_FIELD_IS_NOT_VALID: _('Birthday field is not valid'),
    ERROR_NOT_FOUND_ANY_USER_BY_THIS_USERNAME: _('Not found any user by this username'),
    ERROR_INVALID_AUTHORIZATION_HEADER: _("Invalid authorization header. No credentials provided."),
    ERROR_STORE_NOF_FOUND: _('Store not found.'),
    ERROR_STORE_IS_INACTIVE: _("Store is inactive."),
}

MESSAGE_CODES = {**ERROR_MESSAGE_CODES, **SUCCESS_MESSAGE_CODES}
