from rest_framework.routers import SimpleRouter

from articles import views

router = SimpleRouter(trailing_slash=True)
router.register('', views.ArticleViewSet, basename='articles')

#   List routes      |    Detail routes
#   <basename>-list  |    <basename>-detail

# Custom @action
# <basename>-<action name>

urlpatterns = [

] + router.urls
