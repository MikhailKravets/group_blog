# Serializer: Model <-> JSON object
from django.db import transaction
from rest_framework import serializers

from articles.models import Article
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'birth_year')


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')
