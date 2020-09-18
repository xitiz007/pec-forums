from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username= None, email= None, password= None, **kwargs):
        user = None
        try:
            user = User.objects.get(email= email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username= username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
            
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk= user_id)
        except User.DoesNotExist:
            return None