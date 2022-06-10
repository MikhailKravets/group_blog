# Serializer: Model <-> JSON object
from django.db import transaction
from rest_framework import serializers

from articles.models import Article
from authentication.serializers import SignUpSerializer
from categories.models import Category
from categories.serializers import CategorySerializer


class ArticleSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'category_id', 'text', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')
