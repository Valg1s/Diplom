from .models import CustomUser


class EmailAuthBackend:
    """
    Custom authentication backend.

    Allows users to log in using their email address.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Overrides the authenticate method to allow users to log in using their email address.
        """
        user = CustomUser.objects.get(email=username)
        if user:
            if user.check_password(password):
                return user
            return None
        else:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        return CustomUser.objects.get(user_id=user_id)