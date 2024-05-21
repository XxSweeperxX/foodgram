from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Ingredient, Tag, Recipe
)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class UploadedBase64ImageSerializer(serializers.Serializer):
    file = Base64ImageField(required=False)
    created = serializers.DateTimeField()


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=False)

    class Meta:
        model = Recipe
        fields = '__all__'
