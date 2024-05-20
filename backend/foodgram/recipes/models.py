from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

TAG_CHOICES = (
    ('Breakfast', 'Завтрак'),
    ('Lunch', 'Обед'),
    ('Diner', 'Ужин')
)


class Tag(models.TextChoices):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'

    title = models.TextField(
        max_length=15,
        unique=True
    )
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=7,
        unique=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Ingridient(models.Model):
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
        verbose_name='Автор'
    )
    tag = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        choices=Tag.choices
    )
    time = models.DurationField(
        verbose_name='Время приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingridient,
        through='RecipeIngredient'
    )
    description = models.TextField(
        verbose_name='Описание рецепта'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images'
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'recipes'
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
        verbose_name = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_favourite_recipe'
            )
        )


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
        verbose_name = 'Корзина покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_shop_recipe'
            )
        )


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.tag}, {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
