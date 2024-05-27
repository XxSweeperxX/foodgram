from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import AdminOrReadOnly, AuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer, IngredientSerializer, MyUserSerializer,
    UserAvatarSerializer, RecipeFullSerializer, RecipePartialSerializer,
    RecipeSerializer, ShoppingCartSerializer, SubscriptionSerializer,
    TagSerializer, UserSubscriptionSerializer, ShortLinkSerializer
)
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (
    Favorite, Ingredient, Recipe, RecipeIngredient,
    ShoppingCart, Subscription, Tag
)
from shortener.models import ShortLink

User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeFullSerializer
    permission_classes = (AuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(FavoriteSerializer, request, pk)
        return self.delete_from(Favorite, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCartSerializer, request, pk)
        return self.delete_from(ShoppingCart, request, pk)

    @staticmethod
    def ingredients_to_txt(ingredients):
        shopping_list = ''
        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['ingredient__name']}  - "
                f"{ingredient['sum']}"
                f"({ingredient['ingredient__measurement_unit']})\n"
            )
        return shopping_list

    @staticmethod
    def add_to(current_serializer, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise BadRequest()
        serializer = current_serializer(
            data={
                'user': request.user.id,
                'recipe': recipe.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        final_serializer = RecipePartialSerializer(recipe)
        return Response(
            final_serializer.data, status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete_from(model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            current_object = model.objects.get(
                user=request.user,
                recipe=recipe
            )
        except model.DoesNotExist:
            raise BadRequest()
        current_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        shopping_list = self.ingredients_to_txt(ingredients)
        return HttpResponse(shopping_list, content_type='text/plain')

    @action(
        methods=['get'],
        detail=True,
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        self.get_object()

        path = request.build_absolute_uri().replace(
            'get-link/', '').replace('api/', '')
        s = ShortLink.objects.filter(full_url=path).first()

        if not s:
            s = ShortLink.objects.create(
                full_url=path
            )

        serializer = ShortLinkSerializer(
            data={'short_link': s.short_path},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {'short-link': serializer.data['short_link']},
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeFullSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method in ['PATCH']:
            serializer = MyUserSerializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MyUserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me/avatar',
    )
    def avatar(self, request):
        data = request.data
        if 'avatar' not in data:
            if request.method == 'PUT':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data = {'avatar': None}
        instance = self.get_instance()
        serializer = UserAvatarSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.method == 'DELETE':
            return Response(
                serializer.data,
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={'follower': request.user.id,
                      'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = UserSubscriptionSerializer(
                author,
                context={'request': request}
            )
            return Response(
                author_serializer.data, status=status.HTTP_201_CREATED
            )
        try:
            subscription = Subscription.objects.get(
                follower=request.user,
                author=author
            )
        except Subscription.DoesNotExist:
            raise BadRequest()
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        authors = User.objects.filter(author__follower=request.user)
        result_pages = self.paginate_queryset(
            queryset=authors
        )
        serializer = UserSubscriptionSerializer(
            result_pages,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
