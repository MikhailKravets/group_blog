from rest_framework.reverse import reverse

from mixer.backend.django import mixer

from articles.models import Article
from blog.tests import BaseAPITest


class TestArticleAPIView(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.article = mixer.blend(Article, user=self.user)

    def test_list(self):
        resp = self.client.get(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data), Article.objects.all().count())
        self.assertEqual(resp.data[0]["id"], self.article.id)

    def test_non_authenticated(self):
        self.logout()
        resp = self.client.get(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 401)
