from django.urls import path

from articles import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='articles'),
    path('create/', views.ArticleCreateView.as_view(), name='articles-create'),
]


