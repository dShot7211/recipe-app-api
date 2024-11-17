"""Views for the recipe api's"""

from rest_framework import (
    viewsets,
    mixins,
    status,
    )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

""""import model and serializer"""
from core.models import (
    Recipe,
    Tag,
    Ingredient,
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new reipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin, 
                            mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
        """Base view set for recipe attributes."""

        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
             """Filter queryset to authenticated user"""
             return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):           
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    """we give the model name here in the viewset"""
    queryset = Ingredient.objects.all()





