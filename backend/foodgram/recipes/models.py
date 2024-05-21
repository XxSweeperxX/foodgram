from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):

    title = models.TextField(
        max_length=15,
        unique=True
    )
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message="Цвет должен быть задан в HEX-формате"
            )
        ]
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.TextField()
    measurement_unit = models.CharField(
        max_length=10
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.title}, {self.measurement_unit}'


class Recipe(models.Model):

    name = models.TextField(
        verbose_name='Название рецепта'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    time = models.DurationField(
        verbose_name='Время приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name='Ингридиенты'
    )
    description = models.TextField(
        verbose_name='Описание рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Изображение'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite_recipe'
    )

    class Meta:
        verbose_name = 'Список избранных рецептов'
        verbose_name_plural = 'Списки избранных рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_favourite_recipe'
            )
        ]


class Shopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe'
    )

    class Meta:
        verbose_name = 'Корзину покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_shop_recipe'
            )
        ]


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.tag}, {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Составы Рецептов'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
