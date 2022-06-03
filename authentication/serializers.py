from rest_framework import serializers
from rest_framework.validators import ValidationError

from authentication.models import User
from authentication.validators import normalize_email


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'birth_year')
        read_only_fields = ('id',)
        extra_kwargs = {
            'email': {'validators': [normalize_email]},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.birth_year = validated_data['birth_year']
        user.is_active = True
        user.save()

        return user
