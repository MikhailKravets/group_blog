# Serializer: Model <-> JSON object
from django.db import transaction
from rest_framework import serializers

from articles.models import Article, Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'email', 'name')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author')
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        author = validated_data.pop('author')
        author = Author.objects.create(**author)
        validated_data['author_id'] = author.id
        return super(ArticleSerializer, self).create(validated_data)

