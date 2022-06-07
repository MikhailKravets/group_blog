# Serializer: Model <-> JSON object
from django.db import transaction
from rest_framework import serializers

from articles.models import Article
from authentication.serializers import SignUpSerializer


class ArticleSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')
