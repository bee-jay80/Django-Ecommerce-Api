from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


class CustomJWTCookieAuthentication(BaseAuthentication):
    """
    Custom JWT authentication that checks for the access token in cookies,
    mimicking the behavior of rest_framework_simplejwt.authentication.JWTAuthentication
    but using cookies instead of the Authorization header.
    """

    def authenticate(self, request):
        # Get the access token from the 'access_token' cookie
        token = request.COOKIES.get('access_token')
        if not token:
            return None  # No token provided, proceed to next authentication method

        User = get_user_model()
        try:
            # Validate the token using simplejwt's AccessToken
            access_token = AccessToken(token)
            # Get the user ID from the token payload
            user_id = access_token.payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Token contains no user identification')
            # Retrieve the user
            user = User.objects.get(id=user_id)
            return (user, access_token)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            raise AuthenticationFailed('Invalid token')