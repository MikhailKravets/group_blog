from mixer.backend.django import mixer

from authentication.models import User
from blog.tests import BaseAPITest


class TestUserViewSet(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.u2 = mixer.blend(User, is_active=True)

    def test_list(self):
        pass

    def test_list_only_active_users(self):
        pass

    def test_retrieve(self):
        pass

    def test_retrieve_user_not_exist(self):
        pass

    def test_retrieve_non_active_user(self):
        pass

    def test_unauthorized(self):
        pass
