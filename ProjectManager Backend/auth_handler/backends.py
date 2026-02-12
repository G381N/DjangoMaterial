from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from auth_handler.models import User


class MongoJWTAuthentication(JWTAuthentication):
    user_id_claim = "user_id"

    def get_user(self, validated_token):
        # Extract user id claim from token (default 'user_id')
        user_id = validated_token.get(self.user_id_claim)
        if not user_id:
            raise AuthenticationFailed("Token contained no user identification")

        # Lookup MongoEngine User by id
        user = User.objects(id=user_id).first()
        if user is None:
            raise AuthenticationFailed("User not found for given token")

        return user
