# Generated by Django 4.2.13 on 2024-05-30 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar_alter_user_email_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]