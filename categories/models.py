import uuid

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    path = models.SlugField(unique=True)

    last_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'

    def save(self, *args, **kwargs):
        self.url = self._build_url() if self.id else f"rand:{uuid.uuid4()}"

        super().save(*args, **kwargs)

        if self.url.startswith("rand:"):
            self.url = self._build_url()
            self.save()

    def _build_url(self):
        return f"{self.id}-{slugify(self.name)}"
