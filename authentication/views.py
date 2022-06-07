from rest_framework.generics import CreateAPIView

from authentication.models import User
from authentication.serializers import SignUpSerializer


class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
