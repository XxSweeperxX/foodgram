from django.contrib import admin

from recipes.models import(
    Tag, Ingredient, Recipe, RecipeIngredient,
    RecipeTag, Shopping, Favourite
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'color')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measurement_unit')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'time', 'description')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)


admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(Shopping)
admin.site.register(Favourite)
