from rest_framework.reverse import reverse

from mixer.backend.django import mixer

from articles.models import Article, Like
from blog.tests import BaseAPITest
from categories.models import Category


class TestArticleAPIView(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.category = mixer.blend(Category)
        self.article = mixer.blend(Article, user=self.user, category=self.category)

        self.data = {
            'title': 'Test',
            'text': 'test',
            'category_id': self.category.id
        }

    def test_list(self):
        resp = self.client.get(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data), Article.objects.all().count())
        self.assertEqual(resp.data[0]["id"], self.article.id)
        self.assertEqual(resp.data[0]['category']['id'], self.category.id)

    def test_retrieve(self):
        resp = self.client.get(reverse('v1:articles:articles-detail', args=(self.article.id,)))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.article.id)

    def test_create(self):
        resp = self.client.post(reverse('v1:articles:articles-list'), data=self.data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], self.data['title'])
        self.assertEqual(resp.data['text'], self.data['text'])

        obj = Article.objects.get(title=self.data['title'], user=self.user)
        self.assertEqual(obj.text, self.data['text'])
        self.assertEqual(obj.category, self.category)

    def test_create_no_category_present(self):
        self.article.category = None
        self.article.save()

        del self.data['category_id']

        resp = self.client.post(reverse('v1:articles:articles-list'), data=self.data)

        self.assertEqual(resp.status_code, 201)

        obj = Article.objects.get(title=self.data['title'], user=self.user)
        self.assertIsNone(obj.category)

    def test_create_category_id_is_wrong(self):
        self.data['category_id'] = 0

        resp = self.client.post(reverse('v1:articles:articles-list'), data=self.data)

        self.assertEqual(resp.status_code, 400)

    def test_create_no_category_is_null(self):
        self.data['category_id'] = None

        resp = self.client.post(reverse('v1:articles:articles-list'), data=self.data)

        self.assertEqual(resp.status_code, 201)

        obj = Article.objects.get(title=self.data['title'], user=self.user)
        self.assertIsNone(obj.category)

    def test_create_validation_error(self):
        self.data['title'] = None
        resp = self.client.post(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 400)

    def test_update(self):
        resp = self.client.put(reverse('v1:articles:articles-detail', args=(self.article.id,)), data=self.data)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.data['title'], self.data['title'])
        self.assertEqual(resp.data['text'], self.data['text'])

        self.article.refresh_from_db()
        self.assertEqual(self.article.title, self.data['title'])

    def test_update_other_user(self):
        self.user2 = self.create('wruwehru2332@mail.com')
        self.article.user = self.user2
        self.article.save()

        resp = self.client.put(reverse('v1:articles:articles-detail', args=(self.article.id,)), data=self.data)

        self.assertEqual(resp.status_code, 403)

    def test_delete(self):
        self.fail("write later")

    def test_delete_other_user(self):
        self.fail("write later")

    def test_toggle_like_add_like(self):
        resp = self.client.post(reverse('v1:articles:articles-toggle-like', args=(self.article.id,)))

        self.assertEqual(resp.status_code, 204)
        self.assertTrue(Like.objects.filter(article=self.article, user=self.user).exists())

    def test_toggle_like_remove_like(self):
        Like.objects.create(article=self.article, user=self.user)

        resp = self.client.post(reverse('v1:articles:articles-toggle-like', args=(self.article.id,)))

        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Like.objects.filter(article=self.article, user=self.user).exists())

    def test_non_authenticated(self):
        self.logout()
        resp = self.client.get(reverse('v1:articles:articles-list'))

        self.assertEqual(resp.status_code, 401)
