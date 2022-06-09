import io

from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.test import override_settings
from rest_framework.reverse import reverse

from blog.tests import BaseAPITest


class APITestImageUpload(BaseAPITest):

    def setUp(self):
        self.create_and_login()

        image = Image.new('RGB', (500, 500))
        with io.BytesIO() as output:
            image.save(output, format='jpeg')
            output.seek(0)
            self.file = output.getvalue()

    def test_send_image_binary(self):
        resp = self.client.post(reverse('v1:static_content:image-upload'), content_type='image/jpeg',
                                data=self.file)
        with default_storage.open(resp.data['name']) as f:
            f.read()
        default_storage.delete(resp.data['name'])
        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp.data['name'])
        self.assertIsNotNone(resp.data['url'])

    def test_send_wrong_data(self):
        resp = self.client.post(reverse('v1:static_content:image-upload'), content_type='image/jpeg',
                                data=b'fsdewrw')
        self.assertEqual(resp.status_code, 400)

    def test_upload_image_with_resize(self):
        resp = self.client.post(reverse('v1:static_content:image-upload'), content_type='image/jpeg',
                                data=self.file)
        self.assertEqual(resp.status_code, 201)

        with default_storage.open(resp.data['name']) as f:
            im = Image.open(f)
            w, h = im.size
            self.assertLessEqual(w, settings.IMAGE_MAX_SIZE)
        default_storage.delete(resp.data['name'])

    @override_settings(IMAGE_SIZE_LIMIT=10)
    def test_upload_large_image(self):
        Image.MAX_IMAGE_PIXELS = None
        image_large = Image.new('RGB', (500, 500))

        with io.BytesIO() as output2:
            image_large.save(output2, format='jpeg')
            output2.seek(0)
            self.file_large = output2.getvalue()

        resp = self.client.post(reverse('v1:static_content:image-upload'), content_type='image/jpeg',
                                data=self.file_large)
        self.assertEqual(resp.status_code, 400)
