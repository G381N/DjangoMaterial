from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken

from auth_handler.models import User
from auth_handler.serializers import UserSerializer


def validate_keys(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return Response(
            {
                "message": "There is a Missing Field ...",
                "missing_fields": missing_keys,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None

#Register a new user and return JWT tokens.

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        # Variables---------------------------------------------------------------------------------------------------
        data = request.data or {}
        username = data.get("username", None)
        email = (data.get("email") or "").strip().lower()
        password = data.get("password", None)
        password_confirm = data.get("password_confirm", None)
        # Checking if any field is empty------------------------------------------------------------------------------
        req = ("username", "email", "password", "password_confirm") #RequiredList
        missing_response = validate_keys(data, req)
        # if there is any field missing missing_response wont be empty and will print the response
        if missing_response:
            return missing_response
        # Other validations--------------------------------------------------------------------------------------------
        if password != password_confirm:
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects(username=username).first():
            return Response({"detail": "User with that username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects(email=email).first():
            return Response({"detail": "User with that email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # all validations passed now we create user object and save once-----------------------------------------------
        user = User()
        try:
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
        except Exception:
            return Response({"detail": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST)
        # JWT is getting created---------------------------------------------------------------------------------------
        refresh = RefreshToken.for_user(user)
        response ={}
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message":"User Created Succesfully ..."
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """Authenticate user and return JWT tokens."""

    permission_classes = (AllowAny,)

    def post(self, request):
        # Variables---------------------------------------------------------------------------------------------------
        data = request.data or {}

        # Checking if any field is empty------------------------------------------------------------------------------
        req = ("first_credential", "password")  #RequiredList
        missing_resp = validate_keys(data, req)
        # if there is any field missing missing_response wont be empty and will print the response
        if missing_resp:
            return missing_resp

        first_credential = (data.get("first_credential") or "").strip().lower()
        password = data.get("password")

        # empty value checks------------------------------------------------------------------------------------------
        if not first_credential:
            return Response({"detail": "first_credential is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"detail": "password is required"}, status=status.HTTP_400_BAD_REQUEST)

        # first_credential could be email or username, try email first then username----------------------------------
        user = User.objects(email=first_credential).first()
        if not user:
            user = User.objects(username=first_credential).first()

        if not user or not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # JWT is getting created--------------------------------------------------------------------------------------
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data, 
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


# Refresh an expired access token using a valid refresh token.

class TokenRefreshAPIView(APIView):
    """
    Takes a valid refresh token and returns a new access token.
    The refresh token itself remains valid until it expires (7 days).
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        # Variables---------------------------------------------------------------------------------------------------
        data = request.data or {}

        # Checking if refresh token is provided----------------------------------------------------------------------
        refresh_token = data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Attempting to generate new access token from the refresh token---------------------------------------------
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
        except TokenError as e:
            return Response(
                {"detail": "Invalid or expired refresh token", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "access": new_access,
                "message": "Token refreshed successfully ..."
            },
            status=status.HTTP_200_OK,
        )


# Verify if a given token (access or refresh) is still valid.

class TokenVerifyAPIView(APIView):
    """
    Takes a token and returns whether it is valid.
    Useful for the frontend to check before making API calls.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        # Variables---------------------------------------------------------------------------------------------------
        data = request.data or {}
        token = data.get("token")

        if not token:
            return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to decode the token to check validity------------------------------------------------------------------
        try:
            AccessToken(token)
            return Response({"valid": True, "message": "Token is valid"}, status=status.HTTP_200_OK)
        except TokenError:
            pass

        # If not a valid access token, try as refresh token----------------------------------------------------------
        try:
            RefreshToken(token)
            return Response({"valid": True, "message": "Token is valid"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                {"valid": False, "detail": "Token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# Get current logged-in user information.

class MeAPIView(APIView):
    """
    Returns the profile of the currently authenticated user.
    Requires a valid access token in the Authorization header.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response(
            {
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

