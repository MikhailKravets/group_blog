from django.urls import reverse

from mixer.backend.django import mixer

from articles.models import Author, Article
from blog.tests import BaseTest


class TestArticleListView(BaseTest):

    def setUp(self) -> None:
        author = mixer.blend(Author)
        self.article = mixer.blend(Article, author=author)
        self.create_and_login("test@test.com", "test")

    def test_list(self):
        resp = self.client.get(reverse('articles'))

        self.assertEqual(resp.status_code, 200)

        data = resp.content.decode('utf-8')
        self.assertIn(self.article.title, data)

    def test_unauthorized(self):
        self.logout()

        resp = self.client.get(reverse('articles'))
        self.assertRedirects(resp, reverse('login'))


class TestArticleCreateView(BaseTest):

    def setUp(self) -> None:
        self.create_and_login("test@test.com", "test")

        self.data = {
            'title': 'Test title',
            'text': 'Test text',
            'author': mixer.blend(Author).pk
        }

    def test_create(self):
        resp = self.client.post(reverse('articles-create'), data=self.data)
        self.assertRedirects(resp, reverse('articles'))

        article = Article.objects.get(title=self.data['title'].upper())
        self.assertEqual(article.text, self.data['text'])
        self.assertEqual(article.author.pk, self.data['author'])

    def test_create_without_author(self):
        self.fail("Write later")

    def test_unauthorized(self):
        self.logout()

        resp = self.client.get(reverse('articles-create'))
        self.assertRedirects(resp, reverse('login'))