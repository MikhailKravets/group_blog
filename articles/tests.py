from rest_framework.reverse import reverse

from mixer.backend.django import mixer

from articles.models import Article, Author
from blog.tests import BaseAPITest


class TestArticleAPIView(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.author = mixer.blend(Author)
        self.article = mixer.blend(Article, author=self.author)

    def test_list(self):
        # API_version_namespace:app_name:name_of_url
        resp = self.client.get(reverse('v1:articles-list'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data), Article.objects.all().count())
        self.assertEqual(resp.data[0]["id"], self.article.id)

    def test_non_authenticated(self):
        self.logout()
        resp = self.client.get(reverse('v1:articles-list'))

        self.assertEqual(resp.status_code, 401)
