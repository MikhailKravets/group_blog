from rest_framework import serializers

from authentication.models import User
from authentication.validators import normalize_email


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'birth_year')
        extra_kwargs = {
            'email': {'validators': [normalize_email]},
        }


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'birth_year', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }
