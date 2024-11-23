from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token_key = request.COOKIES.get('auth_token')

        if token_key:
            try:
                request.META['HTTP_AUTHORIZATION'] = f'Token {token_key}'
                return super().authenticate(request)
            except AuthenticationFailed:
                return None
        return None  
