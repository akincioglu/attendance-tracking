from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {
            "refresh_token": str(refresh),
            "access_token": access_token,
            "user_id": user.id,
            "role": user.role,  # Role can be used later to differentiate between admin and employee
        }
