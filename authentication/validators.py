from rest_framework.validators import ValidationError

from authentication.models import User


def normalize_email(value: str):
    value = value.lower()

    if User.objects.filter(email=value).exists():
        raise ValidationError("User with the email already exists.")
