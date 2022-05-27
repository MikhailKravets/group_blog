from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from articles.models import Article
from articles.permissions import HasArticleUpdate
from articles.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    list:
    Get list of articles

    ## Get detailed information about articles

    The code

    ```python
    a = [1, 2, 3]
    ```

    list

    * 1
    * 2

    retrieve:
    Retrieve article

    Retrieve article

    create:
    Create new article

    Create new article and attach to auth user
    """
    permission_classes = (IsAuthenticated, HasArticleUpdate)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
