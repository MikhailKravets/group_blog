from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from authentication.models import User
from blog.paginators import ResultSetPagination
from users.serializers import UserSerializer


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    pagination_class = ResultSetPagination
