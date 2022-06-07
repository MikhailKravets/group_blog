from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from user_profile.serializers import ProfileSerializer, ChangePasswordSerializer


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    @action(methods=['PUT'], detail=True)
    def change_password(self, *args, **kwargs):
        ser = ChangePasswordSerializer(data=self.request.data, instance=self.get_object())
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(ser.data)
