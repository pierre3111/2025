from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from main.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate using email and password.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # Validate password
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
