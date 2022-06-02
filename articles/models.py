from django.db import models


class Article(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255, help_text="Article's title")
    text = models.TextField(help_text="Article's content")

    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='+')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles'
        ordering = ('-title',)


class Like(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='+')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'likes'
