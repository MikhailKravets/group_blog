from blog.tests import BaseAPITest


class TestSignUpAPIView(BaseAPITest):

    def setUp(self):
        self.data = {
            'email': None,
            'password': None
        }

    def test_sign_up(self):
        pass

    def test_email_already_exists(self):
        pass
