from rest_framework import authentication
from rest_framework import exceptions

from customers.models import Store
from message_handler import messages
from message_handler.handler import get_message


class StoreAuthentication(authentication.BaseAuthentication):

    @staticmethod
    def get_client_credentials(request):
        try:
            client_id = request.headers.get('API-KEY')
            if not client_id:
                raise exceptions.NotAuthenticated(get_message(messages.ERROR_INVALID_AUTHORIZATION_HEADER))
        except Exception as e:
            raise exceptions.NotAuthenticated(get_message(messages.ERROR_INVALID_AUTHORIZATION_HEADER))
        return client_id

    def authenticate(self, request):
        client_id = self.get_client_credentials(request)
        try:
            store_instance = Store.objects.get(client_id=client_id)
        except Store.DoesNotExist:
            raise exceptions.NotAuthenticated(get_message(messages.ERROR_STORE_NOF_FOUND))
        except Exception as e:
            raise exceptions.NotAuthenticated(get_message(messages.ERROR_INVALID_AUTHORIZATION_HEADER))
        if not store_instance.is_active:
            raise exceptions.NotAuthenticated(get_message(messages.ERROR_STORE_IS_INACTIVE))
        request.store = store_instance
        return None, None
