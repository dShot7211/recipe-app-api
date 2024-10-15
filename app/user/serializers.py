"""
Serializers for the user API View
"""

from django.contrib.auth import (get_user_model, authenticate)
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer for the user object
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs= {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """  Create and return a use with encrypted password.
        """
        return get_user_model().objects.create_user(**validated_data)
    
        """

        Now we will create a view that uses this serializer
        """

    def update(self, instance, validated_data):
        """Update and return user"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token..
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user.

             the below gets the password and email that is passed in the request
        """
        email = attrs.get('email')
        password= attrs.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        """Return the user here if everything works and the user is used in the view"""        
        attrs['user'] = user
        return attrs