from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follower_following'
            )
        ]

    def clean(self):
        if self.follower == self.author:
            raise ValidationError('Нельзя подписаться на самого себя.')
        super().save(self)

    def __str__(self):
        return f'Пользователь {self.follower} подписался на {self.author}'
