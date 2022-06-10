from rest_framework.routers import SimpleRouter

from categories import views

router = SimpleRouter()
router.register('', views.CategoryViewSet, basename='categories')

urlpatterns = [

] + router.urls
