from django.contrib.auth import get_user_model
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator
)
from django.db import models

from recipes.constants import (
    MIN_VALUE,
    MAX_VALUE,
    MAX_LENGTH_BIG
)

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_BIG,
        verbose_name='Название',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_BIG,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_BIG,
        verbose_name='Название',
        unique=True,
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_BIG,
        null=True,
        verbose_name='Slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message=(
                'Недопустимое название Slug! '
                'Слаг может содержать только целые числа, '
                'буквы или подчеркивания.'
            )
        )]
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_BIG,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes_images/',
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин.',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message='Минимальное время приготовления '
                        f'- {MIN_VALUE} мин.'
            ),
            MaxValueValidator(
                MAX_VALUE,
                message='Максимальное время приготовления '
                        f'- {MAX_VALUE} мин.'
            )
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                message=f'Рецепт должен состоять минимум из {MIN_VALUE} '
                        'ингридиента(-ов).'
            ),
            MaxValueValidator(
                MAX_VALUE,
                message=f'Рецепт должен состоять максимум из {MAX_VALUE} '
                        'ингридиентов.'
            )
        ]
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в рецепте "{self.recipe}"'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'рецепт из избранного'
        verbose_name_plural = 'Рецепты из избранного'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'Избранный рецепт "{self.recipe}" у {self.user}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            ),
        )

    def __str__(self):
        return f'У {self.user} рецепт "{self.recipe}" в списке покупок'


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follover',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'follower'),
                name='unique_author_follower'
            ),
        )

    def __str__(self):
        return f'Подписчик {self.follower} у автора {self.author}'
