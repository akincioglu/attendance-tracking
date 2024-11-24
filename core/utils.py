from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AuthenticationFailed("Authorization header is missing.")

    token = auth_header.split(" ")[1]
    try:
        payload = JWTAuthentication().get_validated_token(token)
        user_id = payload["user_id"]
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        raise AuthenticationFailed("User not found or invalid token.")
