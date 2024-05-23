# Generated by Django 4.2.13 on 2024-05-22 15:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Рецепт должен состоять минимум из 1 ингридиента(-ов).')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Недопустимое название Slug! Слаг может содержать только целые числа, буквы или подчеркивания.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Slug'),
        ),
    ]