from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Ingredient, Favourite, Recipe, Shopping, Tag
)
from api.permissions import IsAdminOnly, IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOnly,)


def delete(request, model, pk):
    recipe = get_object_or_404(Recipe, id=pk)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, request, model, pk):
        recipe = get_object_or_404(
            Recipe, id=pk
        )
        serializer = RecipeSerializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        if model.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=request.user, recipe=recipe)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, model, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        get_object_or_404(model, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):

        if request.method == 'POST':
            return self.add(request, Shopping, pk)

    @shopping_cart.mapping.delete
    def delete_item_from_shopping_cart(self, request, pk):

        if request.method == 'DELETE':
            return self.delete(request, Shopping, pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        file_content = utils.get_shopping_list(user)
        file_name = f'{user.username}-shopping-cart.txt'
        response = HttpResponse(file_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
