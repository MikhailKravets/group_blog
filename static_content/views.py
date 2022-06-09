from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from static_content.parsers import ImageUploadParser
from static_content.serializers import ImageUploadSerializer
from static_content.utils import resize_image, bytes_from_image, bytes_to_mb


class ImageUploadView(APIView):
    """
    Upload image to server

    Upload image into S3 bucket, returning its `name` and `url`.
    You need to specify `Content-Type` header to `image/*` value, i. e. `image/jpeg`.

    Image is finally rescaled to have max width defined in settings (right now it's 600px).
    """
    parser_classes = (ImageUploadParser, )
    serializer_class = ImageUploadSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema('Image', 'image binary', type=openapi.TYPE_FILE, format=openapi.FORMAT_BINARY),
        responses={201: ImageUploadSerializer}
    )
    def post(self, request):
        file: UploadedFile = request.data['file']

        with default_storage.open(file.name, 'wb') as f:
            f.write(self.preprocess_image(file))
        url = default_storage.url(file.name)
        serializer = self.serializer_class({'name': file.name, 'url': url})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def preprocess_image(self, file):
        """Preload image by Pillow, validate for image size limit
        and resize before uploading on S3.

        :param file: image file in jpeg format; class TemporaryUploadedFile
        :return: return status code 400 if the image size exceeds the
        maximum image size limit determined in settings; and return resized image otherwise
        """
        im_size = file.size
        if im_size > settings.IMAGE_SIZE_LIMIT:
            raise ValidationError(
                f"File is too large. Image size should not exceed {bytes_to_mb(settings.IMAGE_SIZE_LIMIT)} MB."
            )
        im = resize_image(file)
        return bytes_from_image(im, settings.IMAGE_DEFAULT_EXTENSION)
