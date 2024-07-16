from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q



class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

class ContactOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(contact=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
