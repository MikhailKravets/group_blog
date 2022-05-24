from django.contrib import admin

from articles import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
