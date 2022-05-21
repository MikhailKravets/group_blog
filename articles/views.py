from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleVieSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
