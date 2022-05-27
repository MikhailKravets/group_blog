from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, response, status

from articles.models import Article, Like
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

    toggle_like:
    Toggle like

    Toggle like
    """
    permission_classes = (IsAuthenticated, HasArticleUpdate)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Default actions of ViewSet
    # list() - list
    # retrieve() - detailed
    # create() - list
    # update() - detailed
    # partial_update() - detailed
    # destroy() - detailed
    @action(methods=['POST'], detail=True, url_path='toggle-like', url_name='toggle-like')
    def toggle_like(self, *args, **kwargs):
        # detail=True: /v1/articles/{id}/toggle-like/
        # detail=False: /v1/articles/toggle-like/
        article = self.get_object()

        try:
            like = Like.objects.get(article=article, user=self.request.user)
            like.delete()
        except Like.DoesNotExist:
            Like.objects.create(article=article, user=self.request.user)

        return response.Response(status=status.HTTP_204_NO_CONTENT)
