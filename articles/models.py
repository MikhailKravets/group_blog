from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, help_text="Author's name")
    email = models.EmailField(max_length=255, help_text="Author's email")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authors'

    def __str__(self):
        return f"{self.id}, {self.name}, {self.email}"


# class Tag(models.Model):
#     name = models.CharField(max_length=255, help_text="Tag's name")
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'tags'
#
#     def __str__(self):
#         return f"{self.id}, {self.name}"


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255, help_text="Article's title")
    text = models.TextField(help_text="Article's content")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles'
        ordering = ('-title',)


# obj = Author.objects.annotate(articles_count=models.Count('articles'))
