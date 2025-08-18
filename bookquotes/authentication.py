from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookiesJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that reads access token from cookies.
    """
    def authenticate(self, request):
        # Get token from cookies
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None  # No cookie → let other authenticators run

        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
        except AuthenticationFailed:
            return None  # Invalid token → not authenticated

        return (user, validated_token)
