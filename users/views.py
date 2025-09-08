from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer


User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
