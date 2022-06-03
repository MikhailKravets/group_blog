from mixer.backend.django import mixer

from authentication.models import User
from blog.tests import BaseAPITest


class TesProfileViewSet(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.u2 = mixer.blend(User, is_active=True)

    def test_retrieve(self):
        pass

    def test_unauthorized(self):
        pass
