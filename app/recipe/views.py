"""Views for the recipe api's"""

from rest_framework import (
    viewsets,
    mixins,
    )
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

""""import model and serializer"""
from core.models import (
    Recipe,
    Tag,
    )
from recipe import serializers

"""Define class"""

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe API's"""

    """give a serializer class to tell which serializer to  user"""
    serializer_class = serializers.RecipeDetailSerializer

    """which model set to use"""
    queryset = Recipe.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """overide the default get method"""
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""

        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""

        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new reipe"""
        serializer.save(user=self.request.user)

class TagViewSet(
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin, 
                 mixins.ListModelMixin, 
                 viewsets.GenericViewSet):
                 
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


