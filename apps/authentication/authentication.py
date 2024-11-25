from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = request.headers.get("Authorization")

        # Authorization header'ını kontrol et
        if header is None or not header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header is missing or invalid.")

        raw_token = header[7:]

        try:
            # Token doğrulamasını yap
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token.")

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        """
        Özelleştirilmiş kullanıcı modelini kullanarak token doğrulaması yapıyoruz.
        """
        try:
            # Token'dan kullanıcı kimliğini al
            user_id = validated_token["user_id"]
        except KeyError:
            raise AuthenticationFailed("Token'da kullanıcı kimliği bulunamadı.")

        try:
            # Kullanıcıyı al
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("Kullanıcı bulunamadı.")

        return user
