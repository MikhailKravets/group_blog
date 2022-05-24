# Serializer: Model <-> JSON object
from django.db import transaction
from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'text',)
        read_only_fields = ('id',)

