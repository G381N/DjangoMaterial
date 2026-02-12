from rest_framework_mongoengine.serializers import DocumentSerializer
from auth_handler.models import User
from rest_framework.exceptions import ValidationError


# minimal user serializer (no password returned)
class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "created_at")


# minimal registration serializer using DocumentSerializer only
class RegisterSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        pw = attrs.get("password")
        #self.initial_data can hold raw request payload as password_confirm does not exist
        pwc = self.initial_data.get("password_confirm")
        if not pw or pw != pwc:
            raise ValidationError("Passwords do not match")
        return attrs

    def validate_email(self, value):
        if User.objects(email=value).first():
            raise ValidationError("This email is already registered")
        return value

    def validate_username(self, value):
        if User.objects(username=value).first():
            raise ValidationError("This username is already taken")
        return value

    def create(self, validated_data):
        # ensure confirmation isn't saved if present
        validated_data.pop("password_confirm", None)
        # create user and hash password via model helper
        raw_password = validated_data.pop("password", None)
        user = User(**validated_data)
        if raw_password:
            user.set_password(raw_password)
        user.save()
        return user

# Notes:
# - Call sequence in views: serializer = RegisterSerializer(data=request.data);
#   serializer.is_valid(raise_exception=True) -> runs validate()/validate_<field>()
#   user = serializer.save() -> runs create()
# - Use ValidationError in serializers so DRF returns HTTP 400 responses.
